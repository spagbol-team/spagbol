"""
Copyright 2024 Spagbol team

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import logging

import numpy as np
from sklearn.decomposition import IncrementalPCA
from typing import Iterable

from spagbol.reduction import DimensionalityReduction
from spagbol.partitioning import PartitionManager
from spagbol.errors import UnfitModelError


class IncrementalPcaReduction(DimensionalityReduction):
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
        self._model = IncrementalPCA(n_components=2)
        self._output_model = IncrementalPCA(n_components=2)
        self._was_fit = False

    def fit(self, batched_data: Iterable):
        """
        Fits the PCA reduction model with the passed data

        :param batched_data: Batched dataset for a series of partial fits
        """
        for batch in batched_data:
            self._model.partial_fit(batch)
        self._was_fit = True

    def fit_transform(self, partition_manager: PartitionManager, column_name="input") -> np.ndarray:
        """
        Partial fits the PCA model on batched data and then applies reduction on the data it was fit on.

        :param partition_manager: Partition manager that will provide embedding data for fit_transform
        :param column_name: Data column name - input or output, will fit a separate model for separate columns
        :return: Reduced data
        """
        logging.debug("Starting IncrementalPCA fit_transform.")
        reduced_data = np.ndarray((0, 2))
        try:
            for batch in partition_manager.batched_partition_iterator(100):
                # Proceed with PCA fit_transform
                if column_name == "input":
                    self._model.partial_fit(batch)
                else:
                    self._output_model.partial_fit(batch)
            self._was_fit = True
            for batch in partition_manager.batched_partition_iterator(100):
                data = np.asarray(batch, dtype=object)
                data = np.array([np.asarray(d, dtype=float) for d in data])
                if column_name == "input":
                    print(np.array(self._model.transform(data)).shape)
                    print(reduced_data.shape)
                    reduced_data = np.concatenate([reduced_data, np.array(self._model.transform(data))])
                else:
                    reduced_data = np.concatenate([reduced_data, np.array(self._output_model.transform(data))])
            logging.debug("PCA fit_transform completed.")
            return reduced_data

        except Exception as e:
            logging.error(f"Error during PCA fit_transform: {e}")
            raise

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