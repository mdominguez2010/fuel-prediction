# export PYTHONPATH="${PYTHONPATH}:/home/md_ghsd/fuel-prediction"
from dataclasses import dataclass
import tensorflow as tf
import pandas as pd
import argparse
import pickle
import csv
import json
import os
from typing import Dict
from typing import List

from fuel_prediction.utils.features import clean_and_organize_data, windowed_dataset, train_test_val_split

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
            delimiter = ',',
            fieldnames = [
                'date',
                'value'
            ]
        )
        return [row for row in reader]

if __name__ == "__main__":
    # Load serialized object
    data_dict = pickle.load(open("../data/raw/fuel_prices.p", "rb"))

    # Clean/organize
    df = clean_and_organize_data(data_dict)

    @dataclass
    class G:
        SERIES = df
        WINDOW_SIZE = 20
        BATCH_SIZE = 5
        SHUFFLE_BUFFER_SIZE = 1000

    # Create dataset with time windows for tf model
    dataset = windowed_dataset(series = G.SERIES.value.values, window_size = G.WINDOW_SIZE, batch_size = G.BATCH_SIZE, shuffle_buffer = G.SHUFFLE_BUFFER_SIZE)
    pickle.dump(data_dict, open("../data/processed/cleaned_dataset.p", "wb"))

    # Train/val/test sets
    series_train, series_val, series_test = train_test_val_split(series = df)
    series_train.to_csv(path_or_buf="../data/raw/series_train.csv", index = False)
    series_val.to_csv(path_or_buf="../data/raw/series_val.csv", index = False)
    series_test.to_csv(path_or_buf="../data/raw/series_test.csv", index = False)

    # Ensures immutiblity
    args = read_args()
    train_datapoints = read_datapoints(args.train_data_path)
    val_datapoints = read_datapoints(args.val_data_path)
    test_datapoints = read_datapoints(args.test_data_path)

    with open(os.path.join(args.output_dir, "cleaned_trained_data.json"), "w") as f:
        json.dump(train_datapoints, f)

    with open(os.path.join(args.output_dir, "cleaned_val_data.json"), "w") as f:
        json.dump(val_datapoints, f)

    with open(os.path.join(args.output_dir, "cleaned_test_data.json"), "w") as f:
        json.dump(test_datapoints, f)