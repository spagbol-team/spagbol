"""
Copyright 2023 Spaghetti team

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

from spagbol.clustering import ClusteringModel
from spagbol.embedding import Embedder
from spagbol.loading import DataLoader
from spagbol.reduction import DimensionalityReduction
from spagbol.similarity import SimilarityMeasure
from spagbol.errors import NoDatasetError, ClusteringError
from spagbol.loading import AlpacaLoader

import pandas as pd
from typing import Dict, Any
from injector import inject
from weaviate.client import WeaviateClient
import weaviate.classes as wvc


class Spagbol:

    def __init__(self, data_loader: DataLoader, embedder: Embedder, clustering_model: ClusteringModel,
                 reducer: DimensionalityReduction):
        self.data_loader = data_loader
        self.embedder = embedder
        self.clustering_model = clustering_model
        self.reducer = reducer
        self.dataset = None

    @inject
    def load_data(self, dataset_location: str):
        # Create an instance of AlpacaLoader with the dataset location
        data_loader = AlpacaLoader(dataset_location)
        # Load the data into memory
        self.dataset = data_loader.load_data()

    def find_similarities(self):
        pass

    def edit_data_point(self, new_data_point: Dict[str, Any]):
        if self.dataset is None:
            raise NoDatasetError("You need to load the dataset before editing data points")
        data_point_df = pd.DataFrame.from_dict(new_data_point)
        data_point_df["input_embedding"] = self.embedder.embed(new_data_point["input"])
        data_point_df["output_embedding"] = self.embedder.embed(new_data_point["output_embedding"])
        self.dataset[self.dataset["id"] == new_data_point["id"]] = data_point_df

    def delete_data_point(self, data_point_id):
        if self.dataset is None:
            raise NoDatasetError("You need to load the dataset before editing data points")
        self.dataset.drop(self.dataset[self.dataset["id"] == data_point_id].index)

    def apply_clustering(self, target_column: str):
        clustered_dataset = self.clustering_model.fit_predict(self.dataset[target_column])
        if clustered_dataset is None:
            raise ClusteringError("An error occurred while clustering the dataset for target column %s" % target_column)

        return clustered_dataset
