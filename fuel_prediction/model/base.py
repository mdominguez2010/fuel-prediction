from abc import ABC
from abc import abstractmethod
from typing import Dict
from typing import List
from typing import Optional

import numpy as np

from fuel_prediction.utils.features import Datapoint #TODO: BUILD OUT

class Model(ABC):
    @abstractmethod
    def train(
        self,
        train_datapoints: List[Datapoint],
        val_datapoints: List[Datapoint],
        cache_featurizer: Optional[bool] = False) -> None:
        """
        Performs training of model. The exact train implementations are model specific.
        :param train_datapoints: List of train datapoints
        :param val_datapoints: List of validation datapoints that can be used
        :param cache_featurizer: Whether or not to cache the model featurizer
        :return:
        """
        pass

    @abstractmethod
    def predict(self, datapoints: List[Datapoint]) -> np.array:
        """
        Performs inference of model on collection of datapoints. Returns an
        array of model predictions. This should only be called after the model
        has been trained.
        :param datapoints: List of datapoints to perform inference on
        :return: Array of predictions
        """
        pass

    @abstractmethod
    def compute_metrics(self, eval_datapoints: List[Datapoint])