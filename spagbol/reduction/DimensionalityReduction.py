"""
Copyright 2023 Spaghetti team

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
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

