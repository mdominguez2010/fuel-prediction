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
from pydantic import BaseModel

from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

######## TODO: BUILD ########
# from fake_news.utils.constants import CANONICAL_SPEAKER_TITLES
# from fake_news.utils.constants import CANONICAL_STATE
# from fake_news.utils.constants import PARTY_AFFILIATIONS
# from fake_news.utils.constants import SIX_WAY_LABEL_TO_BINARY
#############################

logging.basicConfig(
    format = "%(levelname)s - %(asctime)s - %(filename)s - %(message)s",
    level = logging.DEBUG
)

LOGGER = logging.getLogger(__name__)

class Datapoint(BaseModel):
    date: numpy.datetime64
    value: float