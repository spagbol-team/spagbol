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
from spaghetti.clustering.OpticsClustering import OpticsClustering

# you can run this test using the following command line call
# python -m unittest tests.clustering.test_optics_clustering

class TestOpticsClustering(unittest.TestCase):
    # Setup for the tests, initializing the OpticsClustering object 
    # and generating random data
    def setUp(self):
        self.oc = OpticsClustering()
        self.data = np.random.rand(100, 5)

    # Test to check if the object is an instance of OpticsClustering
    def test_initialization(self):
        self.assertIsInstance(self.oc, OpticsClustering)

    # Test to check if the fit method works without throwing any exceptions
    def test_fit(self):
        try:
            self.oc.fit(self.data)
        except Exception as e:
            self.fail(f"Test failed due to: {e}")

    # Test to check if the predict method works correctly
    def test_predict(self):
        self.oc.fit(self.data)
        clusters = self.oc.predict(self.data)
        self.assertIsInstance(clusters, np.ndarray)
        self.assertEqual(clusters.shape[0], self.data.shape[0])

    # Test to check if the fit_predict method works correctly
    def test_fit_predict(self):
        clusters = self.oc.fit_predict(self.data)
        self.assertIsInstance(clusters, np.ndarray)
        self.assertEqual(clusters.shape[0], self.data.shape[0])

if __name__ == '__main__':
    unittest.main()
