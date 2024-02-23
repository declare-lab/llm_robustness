from collections import defaultdict

import pandas as pd
from fire import Fire
from ontology import gsm8k_ontology_dict, human_eval_ontology_dict


def correct_per_category_gsm8k(filename: str, level: int):
    """level: 0, 1, 2, 3"""
    print(filename)
    df = pd.read_csv(filename)
    total = defaultdict(int)
    correct = defaultdict(int)
    for i, o in df.iterrows():
        dimension, label = o["dimension"], o["label"]
        level_name = gsm8k_ontology_dict[dimension][level]
        if str(label) == "nan" or str(label) == "NA" or level_name == "NA":
            continue
        total[level_name] += 1
        if str(label).lower() == "true":
            correct[level_name] += 1
        elif str(label).lower() == "false":
            pass
        else:
            AssertionError
    macro = []
    total_correct = 0
    total_total = 0
    for key in total:
        perf = round(correct[key] / total[key], 4)
        macro += [perf]
        total_correct += correct[key]
        total_total += total[key]
        print(key, f"{correct[key]}/{total[key]}=", perf)
    print("micro:", round(total_correct / total_total, 4))
    print("macro:", round(sum(macro) / len(macro), 4))


def correct_per_category_human_eval(filename: str, level: int):
    """level: 0, 1, 2, 3"""
    print(filename)
    df = pd.read_csv(filename)
    total = defaultdict(int)
    correct = defaultdict(int)
    for i, o in df.iterrows():
        dimension, label = o["dimension"], o["label"]
        level_name = human_eval_ontology_dict[dimension][level]
        if str(label) == "nan" or str(label) == "NA":
            continue
        total[level_name] += 1
        correct[level_name] += label
    macro = []
    total_correct = 0
    total_total = 0
    for key in total:
        perf = round(correct[key] / total[key], 4)
        macro += [perf]
        total_correct += correct[key]
        total_total += total[key]
        print(key, f"{correct[key]}/{total[key]}=", perf, end=";\t")
    print("micro:", round(total_correct / total_total, 4))
    print("macro:", round(sum(macro) / len(macro), 4))


if __name__ == "__main__":
    Fire()
