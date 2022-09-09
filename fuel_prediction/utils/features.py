import json
import logging
import os
import pickle
from copy import deepcopy
from functools import partial

from typing import Dict
from typing import List
from typing import Optional

import numpy as np
from datetime import datetime
from pydantic import BaseModel

from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

######## TODO: BUILD ########
# May not need this page
#############################

logging.basicConfig(
    format = "%(levelname)s - %(asctime)s - %(filename)s - %(message)s",
    level = logging.DEBUG
)

LOGGER = logging.getLogger(__name__)

class Datapoint(BaseModel):
    date: datetime
    value: float

def extract_time_series(datapoints: List[Datapoint]) -> List[Dict]:
    pass

def clean_data(datapoints: List[Dict]) -> List[Dict]:
    pass