"""
Copyright 2023 Spaghetti team

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import numpy as np
from sklearn.cluster import OPTICS

from spagbol.clustering.ClusteringModel import ClusteringModel


class OpticsClustering(ClusteringModel):
    """
    OPTICS Clustering model. It is a subclass of the ClusteringModel class.
    It uses the OPTICS model from sklearn for clustering data.
    Example usages:
        For fitting the model:
            oc = OpticsClustering()
            oc.fit(data)
        For predicting clusters:
            oc = OpticsClustering()
            clusters = oc.predict(data)
        For fitting the model and predicting clusters:
            oc = OpticsClustering()
            clusters = oc.fit_predict(data)

    :param data: Data to be clustered. It should be a numpy array or similar data structure.
    """
    def __init__(self):
        # Initialize the OPTICS model here
        try:
            self._model: OPTICS = OPTICS()
        except Exception as e:
            print(f"Error initializing OPTICS model: {e}")

    def _init_model(self):
        # Initialize the OPTICS model here
        try:
            self._model: OPTICS = OPTICS()
        except Exception as e:
            print(f"Error initializing OPTICS model: {e}")
            return None

    def fit(self, data):
        # Fit the model to the data
        try:
            self._model.fit(data)
        except Exception as e:
            print(f"Error fitting the model: {e}")
    
    def predict(self, data) -> np.array:
        return self.fit_predict(data)

    def fit_predict(self, data) -> np.array:
        # Fit the model to the data and predict the clusters
        try:
            return self._model.fit_predict(data)
        except Exception as e:
            print(f"Error fitting the model and predicting the clusters: {e}")
            return None

