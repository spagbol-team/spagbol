"""
Copyright 2023 Spaghetti team

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
language governing permissions and limitations under the License.
"""

import numpy as np
from sklearn.decomposition import PCA
from typing import Iterable

from spaghetti.reduction import DimensionalityReduction
from spaghetti.errors import UnfitModelError


class PcaReduction(DimensionalityReduction):
    """
    Object for applying PCA dimensionality reduction. Can only work with numerical features.
    You have to fit a model before using transform. You should use scaled or normalized data for better performance
    Example usage:
        If you want to apply reduction to a feature set that wasn't used to fit the model:
            reducer = PcaReduction()
            reducer.fit(numerical_features_train)
            reduced_data = reducer.transform(numerical_features_test)
        Otherwise:
            reducer = PcaReduction()
            reduced_data = reducer.fit_transform(numerical_features)
        """
    def __init__(self):
        self._model = PCA(n_components=2)
        self._was_fit = False

    def fit(self, data: Iterable):
        """
        Fits the PCA reduction model with the passed data

        :param data: Data that will be used to fit the model
        """
        self._model.fit(data)
        self._was_fit = True

    def fit_transform(self, data: Iterable) -> np.ndarray:
        """
        Fits the PCA model and then applies reduction on the data it was fit on.

        :param data: Data that will be used to fit the model and that will be reduced by the model
        :return: Reduced data
        """
        reduced_data = np.array(self._model.fit_transform(data))
        self._was_fit = True
        return reduced_data

    def transform(self, data: Iterable) -> np.ndarray:
        """
        Applies PCA dimensionality reduction on the given data. Model has to be fit before using
        this method.

        :param data: Data that will be reduced
        :raises UnfitModelError: If model wasn't fit before using the method
        :return: Reduced data
        """
        if not self._was_fit:
            raise UnfitModelError("Model has to be fit before using the transform method")
        return np.array(self._model.transform(data))
