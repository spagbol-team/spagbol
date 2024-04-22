"""
Copyright 2024 Spaghetti team

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import logging
from spagbol.clustering import ClusteringModel
from spagbol.embedding import Embedder
from spagbol.loading import DataLoader
from spagbol.reduction import DimensionalityReduction
from spagbol.similarity import SimilarityMeasure
from spagbol.errors import NoDatasetError, ClusteringError
from spagbol.loading import AlpacaLoader

import pandas as pd
import json
from typing import Dict, Any, List
from injector import inject
from weaviate.client import WeaviateClient
import weaviate.classes as wvc


class Spagbol:

    #@inject
    def __init__(self, data_loader: DataLoader, embedder: Embedder, clustering_model: ClusteringModel,
                 reducer: DimensionalityReduction):
        self.data_loader = data_loader
        self.embedder = embedder
        self.clustering_model = clustering_model
        self.reducer = reducer
        self.dataset = None

    def load_data(self, dataset_location: str) -> str:
        # Create an instance of AlpacaLoader with the dataset location
        data_loader = AlpacaLoader(dataset_location)
        # Load the data into memory
        self.dataset = data_loader.load_data()

        print(self.dataset)

    def create_embeddings(self):
        if self.dataset is None:
            raise NoDatasetError("You need to load the dataset before creating embeddings")
        
        # Convert 'input' and 'output' columns to lists of strings, precasting non-string items
        input_data = [str(item) for item in self.dataset['input'].tolist() if item is not None]
        output_data = [str(item) for item in self.dataset['output'].tolist() if item is not None]


        try:
            # Embed the input data
            input_embeddings = self.embedder.embed_batch(input_data)
            self.dataset['input_embedding'] = list(input_embeddings)
        except Exception as e:
            logging.debug(f"failed to create input embeddings: {e}")
            raise Exception(f"Failed to create input embeddings: {e}")

        try:
            # Embed the output data
            output_embeddings = self.embedder.embed_batch(output_data)
            self.dataset['output_embedding'] = list(output_embeddings)
        except Exception as e:
            logging.debug(f"failed to create output embeddings: {e}")
            raise Exception(f"Failed to create output embeddings: {e}")

        print(self.dataset)

    def reduce_dimensions(self):
        if self.dataset is None:
            raise NoDatasetError("You need to load and prepare the dataset before reducing dimensions")

        # Assuming 'input_embedding' and 'output_embedding' are the columns you want to reduce
        input_embeddings = self.dataset['input_embedding']
        output_embeddings = self.dataset['output_embedding']

        try:
            # Reduce dimensions for input embeddings
            reduced_input_embeddings = self.reducer.fit_transform(input_embeddings)
            # Extracting x and y coordinates
            self.dataset['instruction_x'] = reduced_input_embeddings[:, 0]  # Extract x coordinates
            self.dataset['instruction_y'] = reduced_input_embeddings[:, 1]  # Extract y coordinates
        except Exception as e:
            logging.debug(f"Failed to reduce dimensions for input embeddings: {e}")

        try:
            # Reduce dimensions for output embeddings
            reduced_output_embeddings = self.reducer.fit_transform(output_embeddings)
            #self.dataset['reduced_output_embedding'] = reduced_output_embeddings.tolist()
            self.dataset['output_x'] = reduced_output_embeddings[:, 0]  # Extract x coordinates
            self.dataset['output_y'] = reduced_output_embeddings[:, 1]  # Extract y coordinates

        except Exception as e:
            logging.debug(f"Failed to reduce dimensions for output embeddings: {e}")

        print("Reduced Input Embeddings:", self.dataset[['instruction_x', 'instruction_y']])
        print("Reduced Output Embeddings:", self.dataset[['output_x', 'output_y']])

        logging.debug("Dimensionality reduction completed successfully.")

    def to_json(self):
        if self.dataset is None:
            raise NoDatasetError("Dataset is not loaded or prepared.")
        
        # Prepare data for JSON conversion
        data_for_json = []
        for index, row in self.dataset.iterrows():
            item = {
               # "instruction": row["instruction"],
                "input": row["input"],
                "output": row["output"],
                "instruction_x": row["instruction_x"],
                "instruction_y": row["instruction_y"],
                "output_x": row["output_x"],
                "output_y": row["output_y"]
            }
            data_for_json.append(item)
        
        # Convert to JSON string
        json_data = json.dumps(data_for_json, indent=4)
        
        return json_data

    def find_similarities(self):
        pass

    def get_data_points(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        # Filter the dataset based on the criteria
        filtered_data = self.dataset[self.dataset.columns.intersection(criteria.keys())].isin(criteria).dropna()
        
        # Transform the filtered data into the desired format
        transformed_data = []
        for _, row in filtered_data.iterrows():
            transformed_data.append({
                "instruction": row["instruction"],
                "input": row.get("input", ""),  # Assuming 'input' column might not exist for all rows
                "output": row["output"],
                "instruction_x": row["instruction_x"],
                "instruction_y": row["instruction_y"],
                "output_x": row["output_x"],
                "output_y": row["output_y"]
            })
    
        return transformed_data

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
