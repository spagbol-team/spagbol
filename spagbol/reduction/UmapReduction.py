"""
Copyright 2023 Spaghetti team

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

from typing import Iterable
import umap
import numpy as np

from spagbol.reduction import DimensionalityReduction
from spagbol.errors import UnfitModelError


class UmapReduction(DimensionalityReduction):
    """
    Object for applying UMAP dimensionality reduction. Can only work with numerical features.
    You have to fit a model before using transform. You should use scaled or normalized data for better performance
    Example usage:
        If you want to apply reduction to a feature set that wasn't used to fit the model:
            reducer = UmapReduction()
            reducer.fit(numerical_features_train)
            reduced_data = reducer.transform(numerical_features_test)
        Otherwise:
            reducer = UmapReduction()
            reduced_data = reducer.fit_transform(numerical_features)
    """

    def __init__(self):
        self._model = umap.UMAP()
        self._was_fit = False

    def fit(self, data: Iterable) -> None:
        """
        Fits the UMAP reduction model with the passed data

        :param data: Data that will be used to fit the model
        """
        self._model.fit(data)
        self._was_fit = True

    def fit_transform(self, data: Iterable) -> np.ndarray:
        """
        Fits the UMAP model and then applies reduction on the data it was fit on.

        :param data: Data that will be used to fit the model and that will be reduced by the model
        :return: Reduced data
        """
        reduced_data = np.array(self._model.fit_transform(data))
        self._was_fit = True
        return reduced_data

    def transform(self, data: Iterable) -> np.ndarray:
        """
        Applies UMAP dimensionality reduction on the given data. Model has to be fit before using
        this method.

        :param data: Data that will be reduced
        :raises UnfitModelError: If model wasn't fit before using the method
        :return: Reduced data
        """
        if not self._was_fit:
            raise UnfitModelError("Model has to be fit before using the transform method")
        return np.array(self._model.transform(data))


