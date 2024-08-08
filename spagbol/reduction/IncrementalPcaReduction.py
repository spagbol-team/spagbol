"""
Copyright 2024 Spagbol team

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import logging
import os
import numpy as np
from sklearn.decomposition import IncrementalPCA
from typing import Iterable
import pickle as pk


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
        self._input_partition_manager = PartitionManager(
            os.path.join(os.path.expanduser("~"), "input_reduction_partition_dir"),
            10000
        )
        self._output_partition_manager = PartitionManager(
            os.path.join(os.path.expanduser("~"), "output_reduction_partition_dir"),
            10000
        )
        self._model_path = os.path.join(os.path.expanduser("~"), "reduction_weights")
        self._was_fit = False
        if os.path.exists(os.path.join(self._model_path, "input_model.pkl")):
            with open(os.path.join(self._model_path, "input_model.pkl"), 'rb') as fs:
                self._model = pk.load(fs)
                self._was_fit = True
                fs.close()
        if os.path.exists(os.path.join(self._model_path, "output_model.pkl")):
            with open(os.path.join(self._model_path, "output_model.pkl"), 'rb') as fs:
                self._output_model = pk.load(fs)
                self._was_fit = True
                fs.close()

    def fit(self, batched_data: Iterable):
        """
        Fits the PCA reduction model with the passed data

        :param batched_data: Batched dataset for a series of partial fits
        """
        for batch in batched_data:
            self._model.partial_fit(batch)
        self._was_fit = True

    def fit_transform(self, partition_manager: PartitionManager, column_name="input"):
        """
        Partial fits the PCA model on batched data and then applies reduction on the data it was fit on.

        :param partition_manager: Partition manager that will provide embedding data for fit_transform
        :param column_name: Data column name - input or output, will fit a separate model for separate columns
        :return: Reduced data
        """
        logging.debug("Starting IncrementalPCA fit_transform.")
        reduced_data = np.ndarray((0, 2))
        try:
            current_manager = self._input_partition_manager
            if column_name != "input":
                current_manager = self._output_partition_manager
            flat_id_map = partition_manager.partition_map.flatten()
            current_flat_id_map = current_manager.partition_map.flatten()
            flat_id_map.sort()
            current_flat_id_map.sort()
            maps_diff = np.setdiff1d(flat_id_map, current_flat_id_map)
            if len(maps_diff) == 0:
                for entry_id, datapoint in current_manager.partition_iterator():
                    reduced_data = np.concatenate([reduced_data, np.array([datapoint])])
                return reduced_data
            map_dif_by_partition = partition_manager.group_ids_by_partition(maps_diff)
            for partition_name, ids in map_dif_by_partition.items():
                for i in range(0, len(ids), 100):
                    entry_ids = ids[i:i+100]
                    print(entry_ids)
                    batch = partition_manager.get_batch(entry_ids)
                    print(batch)
                    if column_name == "input":
                        if len(batch) > 0:
                            self._model.partial_fit(batch)
                    else:
                        if len(batch) > 0:
                            self._output_model.partial_fit(batch)
            if column_name == "input" and len(maps_diff) != 0:
                with open(os.path.join(self._model_path, "input_model.pkl"), "wb") as fs:
                    pk.dump(self._model, fs)
                    fs.close()
            if column_name == "output" and len(maps_diff) != 0:
                with open(os.path.join(self._model_path, "output_model.pkl"), "wb") as fs:
                    pk.dump(self._output_model, fs)
                    fs.close()
            self._was_fit = True
            new_reduced_data = {}
            if column_name == "input":
                existing_reduced_elements = list(self._input_partition_manager.partition_iterator())
            else:
                existing_reduced_elements = list(self._output_partition_manager.partition_iterator())
            if len(existing_reduced_elements) > 0:
                reduced_data = np.array(existing_reduced_elements)
            for partition_name, ids in map_dif_by_partition.items():
                for i in range(0, len(ids), 100):
                    entry_ids = ids[i:i + 100]
                    batch = partition_manager.get_batch(entry_ids)
                    data = np.asarray(batch, dtype=object)
                    data = np.array([np.asarray(d, dtype=float) for d in data])
                    if column_name == "input":
                        reduced_batch: np.ndarray = self._model.transform(data)
                    else:
                        reduced_batch: np.ndarray = self._output_model.transform(data)
                    for j, new_id in enumerate(entry_ids):
                        reduced_data = np.concatenate([reduced_data, np.array([reduced_batch[j]])])
                        new_reduced_data[new_id] = reduced_batch[j].tolist()
            if column_name == "input" and len(new_reduced_data) > 0:
                self._input_partition_manager.add_data(new_reduced_data)
                self._input_partition_manager.save_partition()
            if column_name == "output" and len(new_reduced_data) > 0:
                self._output_partition_manager.add_data(new_reduced_data)
                self._output_partition_manager.save_partition()
            logging.debug("PCA fit_transform completed.")
            return reduced_data

        except Exception as e:
            logging.error(f"Error during PCA fit_transform: {e}")
            raise

    def transform(self, data: Iterable, column_name="input") -> np.ndarray:
        """
        Applies PCA dimensionality reduction on the given data. Model has to be fit before using
        this method.

        :param data: Data that will be reduced
        :param column_name: Name of the data column. Accepts only 'input' and 'output' for values
        :raises UnfitModelError: If model wasn't fit before using the method
        :return: Reduced data
        """
        if not self._was_fit:
            raise UnfitModelError("Model has to be fit before using the transform method")
        if column_name.lower() == "input":
            return np.array(self._model.transform(data))
        else:
            return np.array(self._output_model.transform(data))
