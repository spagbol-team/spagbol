"""
Copyright 2023 Spaghetti team

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import logging
from spagbol.loading import DataLoader, AlpacaLoader
from spagbol.embedding import Embedder, AllMiniLMEmbedder
from spagbol.clustering import ClusteringModel, GaussianMixtureClustering
from spagbol.reduction import DimensionalityReduction, PcaReduction
from spagbol.errors import InvalidSourceError, NoDatasetError, ClusteringError

class SpagbolController:
    def __init__(self, spagbol_instance):
        self.spagbol = spagbol_instance

    def load_and_prepare_data(self, dataset_location):
        self.spagbol.load_data(dataset_location)
        self.spagbol.create_embeddings()

        logging.debug("embeddings created successfully.")
        