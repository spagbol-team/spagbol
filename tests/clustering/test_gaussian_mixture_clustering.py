"""
Copyright 2023 Spaghetti team

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
language governing permissions and limitations under the License.
"""
import unittest
import numpy as np
from spaghetti.clustering.GaussianMixtureClustering import GaussianMixtureClustering

# you can run this test using the following command line call
# python -m unittest tests.clustering.test_gaussian_mixture_clustering

class TestGaussianMixtureClustering(unittest.TestCase):
    def setUp(self):
        self.gmc = GaussianMixtureClustering()
        self.data = np.random.rand(100, 5)

    def test_fit(self):
        self.gmc.fit(self.data)

    def test_predict(self):
        self.gmc.fit(self.data)
        clusters = self.gmc.predict(self.data)
        self.assertEqual(clusters.shape[0], self.data.shape[0])

    def test_fit_predict(self):
        clusters = self.gmc.fit_predict(self.data)
        self.assertEqual(clusters.shape[0], self.data.shape[0])

if __name__ == '__main__':
    unittest.main()
