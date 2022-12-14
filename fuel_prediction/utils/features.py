# export PYTHONPATH="${PYTHONPATH}:/home/md_ghsd/fuel-prediction"
import json
import logging
import os
import pickle
from copy import deepcopy
from functools import partial
from dataclasses import dataclass
import tensorflow as tf

from typing import Dict
from typing import List
from typing import Optional

import numpy as np
import pandas as pd
from datetime import datetime
from pydantic import BaseModel

from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.model_selection import train_test_split

######## TODO: BUILD ########
# Do we need this?????
#############################

logging.basicConfig(
    format = "%(levelname)s - %(asctime)s - %(filename)s - %(message)s",
    level = logging.DEBUG
)

LOGGER = logging.getLogger(__name__)


def clean_and_organize_data(data_dict: dict) -> list:
    LOGGER.info("Cleaning and organizing data...")
    df = pd.DataFrame(data = data_dict)
    df.sort_values(by = ['year', 'period'], axis = 0, ascending = True, inplace = True)
    df = df[['date', 'value']]
    df.reset_index(drop = True, inplace = True)
    df['date'] = pd.to_datetime(df['date'], format = "%Y/%m/%d", unit = 'D')
    return df


def windowed_dataset(series: list, window_size: int, batch_size: int, shuffle_buffer: int) -> list:
	"""
	We create time windows to create X and y features.
	For example, if we choose a window of 20, we will create a dataset formed by 20 points as X
	"""
	LOGGER.info("BUilding windowed dataset...")
	dataset = tf.data.Dataset.from_tensor_slices(series)
	dataset = dataset.window(window_size + 1, shift=1, drop_remainder=True)
	dataset = dataset.flat_map(lambda window: window.batch(window_size + 1))
	dataset = dataset.shuffle(shuffle_buffer)
	dataset = dataset.map(lambda window: (window[:-1], window[-1]))
	dataset = dataset.batch(batch_size).prefetch(1)
	return dataset

    
def train_test_val_split(series: list) -> list:
    """
    Input: X --> array of features, set aside for validating/testing.
    Output: Features and target split into train, val and test sets. 
    Test size = 20%
    Val size = 20%
    """
    series, series_test = train_test_split(series, test_size=0.2, random_state=51, shuffle = False)
    series_train, series_val = train_test_split(series, test_size=0.2, random_state=51, shuffle = False)

    return series_train, series_val, series_test
