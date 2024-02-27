"""
Copyright 2023 Spaghetti team

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
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
