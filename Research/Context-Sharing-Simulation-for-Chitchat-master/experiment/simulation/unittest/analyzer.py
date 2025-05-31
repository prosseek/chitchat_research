import json
from pprint import pprint


def load(filePath):
    with open(filePath) as data_file:
        return json.load(data_file)

if __name__ == "__main__":
    dict = load("results/result_smcho.SimpleShareLogic_b.json")
    print dict['hostToTuplesMap']['56']