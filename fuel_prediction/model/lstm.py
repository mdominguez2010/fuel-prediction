import logging
import os
import pickle
from typing import Dict
from typing import List
from typing import Optional

import numpy as np
import tensorflow as tf

from fuel_prediction.model.base import Model

loggin.basicConfig(
    format = "%(levelname)s - %(asctime)s - %(filename)s - %(message)s",
    level = logging.DEBUG
)

LOGGER = logging.getLogger(__name__)

class EarlyStopping(tf.keras.callbacks.Callback):
    pass

class BidirectionalLstmModel(Model):
    def __init__(self, config: Optional[Dict] = None):
        self.config = config
        model_cache_path = os.path.join(config["model_output_path"], "model.p")
        if "evaluate" in config and config["evaluate"] and not os.path.exists(model_cache_path):
            raise ValueError("Model config in `evaluate` mode, but model output path does not exist!")
        if model_cache_path and os.path.exists(model_cache_path):
            LOGGER.info("Loading model from cache...")
            with open(model_cache_path, "rb") as f:
                self.model = pickle.load(f)
        else:
            LOGGER.info("Initializing model from scratch...")
            ##### LEFT OFF HERE