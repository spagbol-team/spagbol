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
from typing import Iterable
from numpy import ndarray


class DimensionalityReduction(ABC):
    """
    Interface for dimensionality reduction techniques that can be used in Spaghetti standalone app
    """

    @abstractmethod
    def fit(self, data: Iterable) -> None:
        """
        This method has to fit the reduction model with the passed data

        :param data: Data that will be used to fit the model
        """
        raise NotImplementedError

    @abstractmethod
    def fit_transform(self, data: Iterable) -> ndarray:
        """
        This method has to fit the model and then apply reduction on the data it was fit on.

        :param data: Data that will be used to fit the model and that will be reduced by the model
        :return: Reduced data
        """
        raise NotImplementedError

    @abstractmethod
    def transform(self, data: Iterable) -> ndarray:
        """
        This method has to apply dimensionality reduction on the given data. Model has to be fit before using
        this method.

        :param data: Data that will be reduced
        :return: Reduced data
        """
        raise NotImplementedError

