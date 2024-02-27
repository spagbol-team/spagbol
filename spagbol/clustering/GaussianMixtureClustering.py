"""
Copyright 2023 Spaghetti team

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import numpy as np
from sklearn.mixture import GaussianMixture

from spagbol.clustering.ClusteringModel import ClusteringModel


class GaussianMixtureClustering(ClusteringModel):
    """
    Gaussian Mixture Clustering model. It is a subclass of the ClusteringModel class.
    It uses the GaussianMixture model from sklearn for clustering data.
    Example usages:
        For fitting the model:
            gmc = GaussianMixtureClustering()
            gmc.fit(data)
        For predicting clusters:
            gmc = GaussianMixtureClustering()
            clusters = gmc.predict(data)
        For fitting the model and predicting clusters:
            gmc = GaussianMixtureClustering()
            clusters = gmc.fit_predict(data)

    :param data: Data to be clustered. It should be a numpy array or similar data structure.
    """
    def __init__(self):
        super().__init__()

        # Initialize the GaussianMixture model here
        try:
            self._model: GaussianMixture = GaussianMixture()
        except Exception as e:
            print(f"Error initializing GaussianMixture model: {e}")

    def _init_model(self):
        try:
            return GaussianMixture()
        except Exception as e:
            print(f"Error initializing GaussianMixture model: {e}")
            return None

    def fit(self, data):
        # Fit the model to the data
        try:
            self._model.fit(data)
        except Exception as e:
            print(f"Error fitting the model: {e}")

    def fit_predict(self, data) -> np.array:
        # Fit the model to the data and predict the clusters
        try:
            return self._model.fit_predict(data)
        except Exception as e:
            print(f"Error fitting and predicting the model: {e}")
            return None

    def predict(self, data) -> np.array:
        # Predict the clusters for the data
        try:
            return self._model.predict(data)
        except Exception as e:
            print(f"Error predicting the model: {e}")
            return None
