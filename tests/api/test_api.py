"""
Copyright 2024 Spaghetti team

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import weaviate
import json
import unittest
from unittest.mock import MagicMock
from flask_injector import FlaskInjector, inject
from injector import Binder, Module, singleton

from spagbol.api.spagbol_api import app

class MockDataLoader:
    def load_data(self, client, batch_size):
        pass  # Mock implementation

class TestModule(Module):
    def configure(self, binder: Binder):
        binder.bind(MockDataLoader, to=MockDataLoader, scope=singleton)

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.data_loader = MockDataLoader()

        self.weaviate_client = weaviate.Client("http://localhost:8080")
        
        with self.app.app_context():
            # Set up Flask-Injector with the test module
            FlaskInjector(app=self.app, modules=[TestModule])

    @inject
    def test_load_data(self):
        # Mock the DataLoader's load_data method
        
        data_loader = MagicMock()
        data_loader.load_data = MagicMock(return_value=None)

        # Make a POST request to the load_data route
        response = self.client.post('/load_data', data=json.dumps({
            'client': 'test_client',
            'batch_size': 100
        }), content_type='application/json')

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Data loaded successfully"})
        data_loader.load_data.assert_called_once_with('test_client', 100)

if __name__ == '__main__':
    unittest.main()