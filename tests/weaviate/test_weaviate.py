"""
Copyright 2024 Spaghetti team

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import unittest
import weaviate
#from weaviate.exceptions import RequestsConnectionError

class WeaviateTestCase(unittest.TestCase):

    def setUp(self):
        # Initialize the client attribute before each test
        self.client = weaviate.Client("http://localhost:8080")

    def test_weaviate_ready(self):
        """Test if the Weaviate instance is ready."""
        is_ready = self.client.is_ready()
        self.assertTrue(is_ready, "Weaviate instance is not ready.")

    def test_weaviate_schema(self):
        """Test if the Weaviate schema can be retrieved."""
        schema = self.client.schema.get()
        self.assertIsInstance(schema, dict, "Weaviate schema is not a dictionary.")
        self.assertIn('classes', schema, "Weaviate schema does not contain classes.")

    def test_weaviate_create_data_object(self):
        """Test if a data object can be created in the Weaviate instance."""
        test_object = {
            "class": "TestObject",
            "properties": {
                "name": "testName"
            }
        }
        result = self.client.data_object.create(test_object, "TestObject")
        self.assertIsNotNone(result, "Failed to create a data object in Weaviate.")




if __name__ == '__main__':
    unittest.main()