import json

import pandas as pd
import tqdm
from fire import Fire

from ontology import Ontology

ont = Ontology()
gsm8k_ontology_dict = ont.gsm8k()
human_eval_ontology_dict = ont.human_eval()


def gsm8k_to_json():
    df = pd.read_csv("csvs/gsm8k_gpt4.csv")
    dataset_list = []
    for i, o in df.iterrows():
        if o["dimension"] == "Original":
            continue
        original_q, original_a = o["original"].split("Answer:")
        p_type = o["dimension"]
        if p_type not in gsm8k_ontology_dict:
            continue

        category, dimension, domain, aspect = gsm8k_ontology_dict[p_type]
        new_p, new_a = o["rephrased_counterfactual"], o["answer"]
        item = dict(
            original_question=original_q,
            original_answer=original_a,
            math_category=p_type,
            category=category,
            dimension=dimension,
            domain=domain,
            aspect=aspect,
            perturbed_question=new_p,
            perturbed_answer=new_a,
        )
        dataset_list.append(item)

    dataset_list = [
        d for d in dataset_list if all(str(value) != "nan" for value in d.values())
    ]

    print(len(dataset_list))
    with open("gsm8k_problem.jsonl", "w") as file:
        json.dump(dataset_list, file, indent=4)

    return


def human_eval_to_json():
    df = pd.read_csv("csvs/human_eval.csv")
    dataset_list = []
    for i, o in df.iterrows():
        if o["dimension"] == "Original":
            continue
        original_function = o["original"]
        p_type = o["dimension"]
        if p_type not in human_eval_ontology_dict:
            continue
        category, dimension, domain, aspect = human_eval_ontology_dict[p_type]
        new_p, new_a = o["rephrased_counterfactual"], o["answer"]
        if str(new_p) == "nan":
            continue
        instruction = o["instruction"]
        test_input, test_output = o["test_input"], o["test_output"]
        if instruction == "Closed Question":
            instruction = (
                "Generate a python function that fulfills the requirement below."
            )
        item = dict(
            original_function=original_function,
            math_category=p_type,
            category=category,
            dimension=dimension,
            domain=domain,
            aspect=aspect,
            instruction=str(instruction),
            perturbed_question=str(new_p),
            perturbed_answer=str(new_a),
            test_input=str(test_input),
            test_output=str(test_output),
        )
        dataset_list.append(item)

    print(len(dataset_list))
    with open("human_eval_problem.jsonl", "w") as file:
        json.dump(dataset_list, file, indent=4)

    return


def print_dimension(filename: str):
    """
    filename: {gsm8k.csv, human_eval.csv}
    model_name: chatgpt gpt4...
    method: dp, cot, pot, consistency
    """
    print(locals())
    dataset_name = "gsm8k" if "gsm8k" in filename else "human_eval"

    df = pd.read_csv(filename)

    dimensions = []

    for i, o in tqdm(df.iterrows(), total=len(df)):
        dimensions.append(o["dimension"])
    print(list(set(dimensions)))


def split_test_cases(input_string):
    lines = input_string.split("\n")
    test_cases = []
    function = []

    for line in lines:
        if line.startswith("assert "):
            test_cases.append("\n".join(function) + "\n" + line)
        else:
            function.append(line)
    return test_cases


def check_nan(i):
    return i == "NA" or str(i) == "nan"


if __name__ == "__main__":
    Fire()
