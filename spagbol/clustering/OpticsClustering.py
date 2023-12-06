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

