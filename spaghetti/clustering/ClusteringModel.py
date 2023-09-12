"""
Copyright 2023 Spaghetti team

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
language governing permissions and limitations under the License.
"""
from abc import ABC, abstractmethod
import numpy as np

class ClusteringModel(ABC):
    """
    This is the interface for all clustering techniques used in this project.
    Every clustering class imported into this project has to use this interface
    """

    @abstractmethod
    def __init__(self):
        """
        This method should initialize the model
        """
        pass

    @abstractmethod
    def _init_model(self):
        """
        This method should initialize the model
        """
        raise NotImplementedError()

    @abstractmethod
    def fit(self, data):
        """
        This method should fit the model to the data
        """
        raise NotImplementedError()

    @abstractmethod
    def fit_predict(self, data) -> np.array:
        """
        This method should fit the model to the data and predict the clusters
        :param data: Input data to be clustered
        :return: Predicted clusters
        """
        raise NotImplementedError()

    @abstractmethod
    def predict(self, data) -> np.array:
        """
        This method should predict the clusters for the data
        :param data: Input data to be clustered
        :return: Predicted clusters
        """
        raise NotImplementedError()
