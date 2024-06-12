import random
import re
import time
from collections import defaultdict
from copy import deepcopy

import pandas as pd
from fire import Fire
from tqdm import tqdm

from execution import easy_check
from helper import check_nan, split_test_cases
from modeling import select_model
from ontology import (
    Dataset,
    Ontology,
    PerturbTemplateGSM8K,
    PerturbTemplateHumanEval,
    PromptTemplate,
)


ontology = Ontology()
prompt_template = PromptTemplate()
perturb_gsm8k = PerturbTemplateGSM8K()
perturb_human_eval = PerturbTemplateHumanEval()
dataset = Dataset()


def get_requirement(string):
    if not string:
        return None
    for l in string.split("\n"):
        if l.lower().startswith("#rewrite requirement#"):
            return l
    return None


def gen_dataset_gsm8k():
    print(locals())
    model = select_model(model_name="gpt4", temperature=0.8).generate
    item_list = dataset.gsm8k_original()
    categories = ontology.gsm8k().keys()
    perturbed_items = []

    for item in tqdm(item_list):
        for category in tqdm(categories, leave=False):
            dimension = ontology.gsm8k()[category][1]
            perturbed_q, answer, prompt = perturb_gsm8k(
                dimension, deepcopy(item), category, model
            )
            requirement = get_requirement(prompt)
            if requirement:
                refined_perturbed_q = prompt_template.filter_refine_gsm8k(
                    item, perturbed_q, requirement, model
                )
            item_dict = dict(
                category=category,
                original_question=f"{item.context} {item.question}\n",
                original_answer=f"Answer:\n{item.chain_of_thought}\n{item.answer}",
                perturbed_question=perturbed_q,
                refined_perturbed_q=refined_perturbed_q,
                prompt=prompt,
            )
            perturbed_items.append(item_dict)

    df = pd.DataFrame(perturbed_items)
    df.to_csv("gsm8k_problem.csv", index=False)
    return df


def gen_dataset_human_eval():
    print(locals())
    model = select_model(model_name="gpt4", temperature=0.8).generate
    item_list = dataset.human_eval_original()
    categories = ontology.human_eval().keys()
    perturbed_items = []

    for item in tqdm(item_list):
        for category in tqdm(categories, leave=False):
            dimension = ontology.human_eval()[category][1]
            perturbed_q, answer, prompt = perturb_human_eval(
                dimension, deepcopy(item), category, model
            )
            requirement = get_requirement(prompt)
            if requirement:
                refined_perturbed_q = prompt_template.filter_refine_human_eval(
                    item, perturbed_q, requirement, model
                )
            item_dict = dict(
                category=category,
                original_question=f"{item.function_header}{item.docstring}{item.examples}\n",
                original_answer=f"Answer:\n{item.answer}",
                perturbed_question=perturbed_q,
                refined_perturbed_q=refined_perturbed_q,
                prompt=prompt,
            )
            perturbed_items.append(item_dict)

    df = pd.DataFrame(perturbed_items)
    df.to_csv("human_eval_problem.csv", index=False)
    return df


def gen_solution_gsm8k(
    filename: str = "gsm8k.csv", model_name="gpt4", print_output=False
):
    """
    Generate solution using chain of thought
    """
    print(locals())

    dataset_name = "gsm8k"
    df = pd.read_csv(filename)
    model = select_model(model_name)
    prompt_method = prompt_template.gsm8k_cot_prompt

    outputs = []
    for i, o in tqdm(df.iterrows(), total=len(df)):
        perturbed_question = o["perturbed_question"]
        if check_nan(perturbed_question):
            outputs.append("NA")
            continue
        prompt = prompt_method(perturbed_question=perturbed_question, model=model_name)

        output = model.generate(prompt)
        if print_output:
            print(prompt)
            print("-" * 20)
            print(output)
        outputs.append(output)
        time.sleep(2)

    df[f"{model_name}_output"] = outputs
    df.to_csv(f"{dataset_name}_{model_name}_cot.csv", index=False)
    return df


def gen_solution_human_eval(
    filename: str = "human_eval.csv", model_name="gpt4", print_output=False
):
    """
    Generate solution using chain of thought
    """
    print(locals())
    dataset_name = "human_eval"
    df = pd.read_csv(filename)
    model = select_model(model_name)
    prompt_method = prompt_template.human_eval_cot_prompt

    outputs = []
    for i, o in tqdm(df.iterrows(), total=len(df)):
        perturbed_question = o["perturbed_question"]
        if check_nan(perturbed_question):
            outputs.append("NA")
            continue
        # instruction = o["instruction"]
        # if instruction == "Closed Question":
        #     instruction = (
        #         "Generate a python function that fulfills the requirement below."
        #     )

        prompt = prompt_method(
            instruction=o["instruction"],
            perturbed_question=perturbed_question,
            model=model_name,
        )

        output = model.generate(prompt)
        if print_output:
            print(prompt)
            print("-" * 20)
            print(output)
        outputs.append(output)

    df["output"] = outputs
    df.to_csv(f"{dataset_name}_{model_name}_cot.csv", index=False)
    return df


def gen_solution_gsm8k_w_answer(filename: str, model_name="gpt4"):
    """
    Feed in prompt with orginal answer for logic alteration domain only
    """
    print(locals())
    df = pd.read_csv(filename)
    model = select_model(model_name)
    prompt_method = prompt_template.gsm8k_with_answer_prompt

    outputs = []
    keep_indices = []

    for i, o in tqdm(df.iterrows(), total=len(df)):
        perturbed_question = o["perturbed_question"]
        dimension = o["dimension"]
        if check_nan(
            perturbed_question
        ) or dimension not in ontology.logic_alteration_category("gsm8k"):
            outputs.append("NA")
            continue
        prompt = prompt_template.gsm8k_with_answer_prompt(
            perturbed_question=perturbed_question,
            original_question=o["original_question"],
            original_answer=o["original_answer"],
        )

        keep_indices.append(i)
        output = model.generate(prompt)
        print(prompt)
        print("-" * 20)
        print(output)
        outputs.append(output)

    df["output"] = outputs
    df = df.iloc[keep_indices]
    df.to_csv(f"gsm8k_w_answer_{model_name}.csv", index=False)
    return df


def gen_solution_human_eval_w_answer(filename: str, model_name="gpt4"):
    """
    Feed in prompt with orginal answer for logic alteration domain only
    """
    print(locals())
    df = pd.read_csv(filename)
    model = select_model(model_name)
    prompt_method = prompt_template.human_eval_with_answer_prompt
    outputs = []
    keep_indices = []

    for i, o in tqdm(df.iterrows(), total=len(df)):
        perturbed_question = o["perturbed_question"]
        dimension = o["dimension"]
        if check_nan(
            perturbed_question
        ) or dimension not in ontology.logic_alteration_category("human_eval"):
            outputs.append("NA")
            continue
        if instruction == "Closed Question":
            instruction = (
                "Generate a python function that fulfills the requirement below."
            )

        prompt = prompt_template.human_eval_with_answer_prompt(
            instruction=instruction,
            perturbed_question=perturbed_question,
            original_function=o["original_function"],
        )

        keep_indices.append(i)
        output = model.generate(prompt)
        print(prompt)
        print("-" * 20)
        print(output)
        outputs.append(output)

    df["output"] = outputs
    df = df.iloc[keep_indices]
    df.to_csv(f"human_eval_w_answer_{model_name}.csv", index=False)
    return df


def gen_solution_gsm8k_pot(
    filename: str = "gsm8k.csv", model_name="gpt4", print_output=False
):
    """
    Generate solution using Program of Thought(POT) for `logic alteration' domain only
    """
    print(locals())

    dataset_name = "gsm8k"
    df = pd.read_csv(filename)
    model = select_model(model_name)
    prompt_method = prompt_template.gsm8k_pot_prompt

    outputs = []
    for i, o in tqdm(df.iterrows(), total=len(df)):
        perturbed_question = o["perturbed_question"]
        if check_nan(perturbed_question):
            outputs.append("NA")
            continue
        prompt = prompt_method(
            perturbed_question=perturbed_question,
        )
        output = model.generate(prompt)
        if print_output:
            print(prompt)
            print("-" * 20)
            print(output)
        outputs.append(output)

    df["f{model_name}_output"] = outputs
    df.to_csv(f"{dataset_name}_{model_name}_pot.csv", index=False)
    return df


def run_pot_gsm8k(filename: str = "gsm8k.csv"):
    df = pd.read_csv(filename)

    pot_results = []
    for i, o in tqdm(df.iterrows(), total=len(df)):
        text = o["output"]
        pattern = r"```python(.*?)```"
        if """```python""" in text:
            code = re.findall(pattern, text, re.DOTALL)[-1].strip()
        else:
            code = text
        if "print" not in code and "return" not in code:
            variable = code.split("\n")[-1].strip()
            code += f"\nprint({variable})"
        try:
            local_vars = {}
            exec(code, globals(), local_vars)
            pot_results.append(local_vars)
        except Exception:
            pot_results.append("Code Error")

    df["pot_results"] = pot_results
    df.to_csv(filename, index=False)


def gen_solution_gsm8k_cons(filename: str, model_name="gpt4", index=0):
    """
    Generate solution using self-consistency prompting for `logic alteration' domain only
    """
    print(locals())

    dataset_name = "gsm8k"
    df = pd.read_csv(filename)
    model = select_model(model_name)
    prompt_method = prompt_template.gsm8k_consistency_prompt

    category_dict = defaultdict(list)
    for i, o in df.iterrows():
        question, answer = o["perturbed_question"], o["answer"]
        category_dict[o["dimension"]].append((i, question, answer))
    outputs = []
    prompts = []

    for i, o in tqdm(df.iterrows(), total=len(df)):
        if dataset_name == "gsm8k":
            perturbed_question = o["perturbed_question"]
            if check_nan(perturbed_question):
                outputs.append("NA")
                prompts.append("NA")
                continue
            pool = category_dict[o["dimension"]]
            pool = [poo for poo in pool if poo[0] != i]
            if len(pool) > 0:
                pick_qa = random.choice(pool)
                _, oneshot_question, oneshot_answer = pick_qa
                prompt = prompt_method(
                    oneshot_question=oneshot_question,
                    oneshot_answer=oneshot_answer,
                    perturbed_question=perturbed_question,
                )
            else:
                prompt = prompt_template.gsm8k_cot_prompt(
                    perturbed_question=perturbed_question, model=model_name
                )

        output = model.generate(prompt)
        outputs.append(output)
        prompts.append(prompt)

    df["output"] = outputs
    df["one_shot_prompt"] = prompts
    df.to_csv(f"gsm8k_{model_name}_cons_{index}.csv", index=False)
    return output


def summarize_solution_gsm8k_cons(model_name="gpt4", index=0):
    print(locals())
    df0 = pd.read_csv(f"gsm8k_{model_name}_cons_0.csv")
    df1 = pd.read_csv(f"gsm8k_{model_name}_cons_1.csv")
    df2 = pd.read_csv(f"gsm8k_{model_name}_cons_2.csv")
    model = select_model(model_name)
    prompt_method = prompt_template.gsm8k_summarize_consistency_prompt

    outputs = []
    for i, o in tqdm(df0.iterrows(), total=len(df0)):
        counterfactual = o["perturbed_question"]
        answer0 = df0.at[i, "output"]
        answer1 = df1.at[i, "output"]
        answer2 = df2.at[i, "output"]

        prompt = prompt_method(
            perturbed_question=counterfactual,
            answer0=answer0,
            answer1=answer1,
            answer2=answer2,
        )
        output = model.generate(prompt)
        outputs.append(output)

    df0["summarized_output"] = outputs
    df0.to_csv(f"gsm8k_{model_name}_consistency_{index}.csv", index=False)
    return output


# def compare_solution_gsm8k(
#     filename: str, eval_model_name="gpt4", output_column="output"
# ):
#     print(locals())
#     dataset_name = "gsm8k"

#     df = pd.read_csv(filename)
#     model = select_model(eval_model_name)
#     prompt_method = prompt_template.gsm8k_compare_prompt

#     gpt4_labels = []
#     for i, o in tqdm(df.iterrows(), total=len(df)):
#         perturbed_question = o["perturbed_question"]
#         generated = o[output_column]
#         gold = o["answer"]
#         prompt = prompt_method(
#             question=perturbed_question, generated_answer=generated, gold_answer=gold
#         )
#         label = model.generate(prompt)
#         gpt4_labels.append(label)

#     df["gpt4_label"] = gpt4_labels
#     df.to_csv(filename, index=False)


def gen_testcase_input_human_eval(filename: str = "human_eval.csv"):
    """
    filename: {human_eval.csv}
    model_name: chatgpt gpt4...
    """
    print(locals())
    """Some generated input test cases do not have [], and need human correction
    """

    df = pd.read_csv(filename)
    model = select_model("gpt4", temperature=0.8)
    prompt_method = prompt_template.testcase_input_prompt

    input_tests = []

    for i, o in tqdm(df.iterrows(), total=len(df)):
        counterfactual = o["perturbed_question"]
        instruction = o["instruction"]
        answer = o["answer"]
        reference = o["test_input_reference"]

        if (
            check_nan(counterfactual)
            or instruction != "Closed Question"
            or "gold_solution" not in answer
        ):
            input_tests.append("NA")
            continue

        input_prompt = prompt_method(
            perturbed_question=counterfactual, reference=reference
        )
        input_test = model.generate(input_prompt)
        input_tests.append(input_test)

    df["test_input"] = input_tests
    df.to_csv(filename, index=False)


def gen_testcase_output_human_eval(filename: str = "human_eval.csv"):
    """This do not need chatgpt"""
    print(locals())
    df = pd.read_csv(filename)
    prompt_method = prompt_template.testcase_output_prompt
    output_tests = []

    for i, o in tqdm(df.iterrows(), total=len(df)):
        answer = o["answer"]
        test_input = o["test_input"]

        if check_nan(answer) or check_nan(test_input) or "gold_solution" not in answer:
            output_tests.append("NA")
            continue

        output_test = prompt_method(test_input=test_input, answer=answer)
        output_tests.append(output_test)

    df["test_output"] = output_tests
    df.to_csv(filename, index=False)


def gen_testcode_human_eval(filename: str = "human_eval.csv", model_name="gpt4"):
    """
    filename: human_eval.csv
    model_name: chatgpt gpt4...
    """
    print(locals())
    dataset_name = "human_eval"

    df = pd.read_csv(filename)
    model = select_model(model_name, temperature=0.0)
    prompt_method = prompt_template.testcode_prompt

    testcodes = []
    for i, o in tqdm(df.iterrows(), total=len(df)):
        counterfactual = o["perturbed_question"]
        instruction = o["instruction"]
        test_input = o["test_input"]
        test_output = o["test_output"]
        generation = o["output"]

        if (
            check_nan(counterfactual)
            or instruction != "Closed Question"
            or str(test_output) == "nan"
        ):
            testcodes.append("NA")
            continue

        prompt = prompt_method(
            perturbed_question=counterfactual,
            test_input=test_input,
            test_output=test_output,
            generation=generation,
        )
        testcode = model.generate(prompt)
        testcodes.append(testcode)

    df["testcode"] = testcodes
    df.to_csv(filename, index=False)

    return df


def run_testcode_human_eval(filename: str = "human_eval.csv"):
    """
    filename: human_eval.csv
    """
    print(locals())

    df = pd.read_csv(filename)

    labels = []
    passes = []
    for i, o in tqdm(df.iterrows(), total=len(df)):
        counterfactual = o["perturbed_question"]
        instruction = o["instruction"]
        test_input = o["test_input"]
        test_output = o["test_output"]
        generation = o["output"]
        testcode = o["testcode"]

        if (
            check_nan(counterfactual)
            or instruction != "Closed Question"
            or str(testcode) == "nan"
        ):
            labels.append("NA")
            passes.append("NA")
            continue

        testcode = testcode.replace("```python", "").replace("```", "")
        testcodes = split_test_cases(testcode)
        label = ""
        passed = True
        for testcode in testcodes:
            return_dict = easy_check(test_program=testcode, timeout=5)
            label += return_dict["result"] + "\n"
            if "fail" in return_dict["result"]:
                passed = False
        labels.append(label)
        passes.append(passed)

    df["label"] = labels
    df["passed"] = passes
    df.to_csv(filename, index=False)


if __name__ == "__main__":
    Fire()
