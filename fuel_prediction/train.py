import argparse
import json
import logging
import os
import random
from shutil import copy

import mlflow
import numpy as np
import tensorflow as tf

from fuel_prediction.model.lstm import BidirectionalLstmModel
from fuel_prediction.utils.reader import read_json_data

logging.basicConfig(
    format="%(levelname)s - %(asctime)s - %(filename)s - %(message)s",
    level=logging.DEBUG
)

LOGGER = logging.getLogger(__name__)


def read_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-file", type = str)
    return parser.parse_args()


def set_random_seed(val: int = 51) -> None:
    random.seed(val)
    np.random.seed(val)
    # tensorflow specific random-seed
    tf.random.set_seed(val)


if __name__ == "__main__":
    args = read_args()
    with open(args.config_file) as f:
        config = json.load(f)

    set_random_seed(val = 51)