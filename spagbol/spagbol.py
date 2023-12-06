"""
Copyright 2023 Spagbol team

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
language governing permissions and limitations under the License.
"""

from spagbol.clustering import ClusteringModel
from spagbol.embedding import Embedder
from spagbol.loading import DataLoader
from spagbol.reduction import DimensionalityReduction
from spagbol.similarity import SimilarityMeasure
from spagbol.errors import NoDatasetError, ClusteringError

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
    def load_data(self, client: WeaviateClient, embedding_batch_size=200):
        # Load data -> run embeddings on input and output, store them as self.dataset["input_embedding"] and
        # self.dataset["output_embedding"], apply reduction on those two, store reduced coordinates as
        # self.dataset["reduced_input_x"], self.dataset["reduced_input_y"], self.dataset["reduced_output_x"],
        # self.dataset["reduced_output_y"]. Either add ids to rows here or add it in the DataLoader,
        # should be stored in the "id" column
        pass

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
