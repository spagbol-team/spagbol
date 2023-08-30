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
    def test_optics_clustering(self):
        # Initialize the OpticsClustering
        oc = OpticsClustering()

        # Create some dummy data
        data = np.random.rand(100, 5)

        # Test the fit method
        oc.fit(data)

        # Test the fit_predict method
        clusters = oc.fit_predict(data)
        self.assertEqual(clusters.shape[0], data.shape[0])

if __name__ == '__main__':
    unittest.main()
