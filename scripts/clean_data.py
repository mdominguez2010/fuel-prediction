import argparse
import csv
import json
import os
from typing import Dict
from typing import List

from fuel_prediction.utils.features import clean_data

def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train-data-path", type = str)
    parser.add_argument("--val-data-path", type = str)
    parser.add_argument("--test-data-path", type = str)
    parser.add_argument("--output-dir", type = str)
    return parser.parse_args()

def read_datapoints(datapath: str) -> List[Dict]:
    with open(datapath) as f:
        reader = csv.DictReader(
            f,
            delimeter = ',',
            fieldnames = [
                'period',
                'periodName',
                'value',
                'year',
                'date'
            ]
        )
        return [row for row in reader]

if __name__ == "__main__":
    args = read_args()
    # train_datapoints = read_datapoints(args.train_data_path)
    # val_datapoints = read_datapoints(args.val_data_path)
    # test_datapoints = read_datapoints(args.test_data_path)

    # train_datapoints = clean_data(train_datapoints)
    # val_datapoints = clean_data(val_datapoints)
    # test_datapoints = clean_data(test_datapoints)