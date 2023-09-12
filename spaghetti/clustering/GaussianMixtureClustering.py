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
from sklearn.mixture import GaussianMixture
from spaghetti.clustering.ClusteringModel import ClusteringModel

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
