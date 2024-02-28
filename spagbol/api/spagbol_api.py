"""
Copyright 2024 Spaghetti team

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

# Import necessary modules from Flask and dependency injection libraries
from flask import Flask, request, jsonify
from flask_injector import FlaskInjector
from injector import inject, singleton

# Import Spagbol system components
from spagbol.spagbol import Spagbol
from spagbol.loading import DataLoader, AlpacaLoader
from spagbol.embedding import Embedder, AllMiniLMEmbedder
from spagbol.clustering import ClusteringModel, GaussianMixtureClustering
from spagbol.reduction import DimensionalityReduction, PcaReduction

# Initialize Flask application
app = Flask(__name__)

# Configure dependency injection for the application
def configure(binder):
    # Bind interfaces to concrete implementations with singleton scope
    binder.bind(DataLoader, to=AlpacaLoader, scope=singleton)
    binder.bind(Embedder, to=AllMiniLMEmbedder, scope=singleton)
    binder.bind(ClusteringModel, to=GaussianMixtureClustering, scope=singleton)
    binder.bind(DimensionalityReduction, to=PcaReduction, scope=singleton)
    # Additional bindings can be added here if necessary

# Apply the dependency injection configuration to the Flask app
FlaskInjector(app=app, modules=[configure])

# Define route for loading data into the system
@app.route('/load_data', methods=['POST'])
@inject
def load_data():
    # Parse request content as JSON
    content = request.json
    try:
        # Extract required parameters from the request
        client = content['client']
        batch_size = content.get('batch_size', 200)  # Default batch size is 200 if not specified
        # Load data using the Spagbol instance
        spagbol_instance.load_data(client, batch_size)
        # Return success message
        return jsonify({"message": "Data loaded successfully"}), 200
    except KeyError as e:
        # Return error message for missing request keys
        return jsonify({"error": f"Missing key in request: {str(e)}"}), 400
    except Exception as e:
        # Return error message for any other exceptions
        return jsonify({"error": "An unexpected error occurred"}), 500

# Define route for editing a data point
@app.route('/edit_data_point', methods=['POST'])
@inject
def edit_data_point():
    # Parse request content as JSON
    data_point = request.json
    try:
        # Edit the data point using the Spagbol instance
        spagbol_instance.edit_data_point(data_point)
        # Return success message
        return jsonify({"message": "Data point edited successfully"}), 200
    except NoDatasetError as e:
        # Return error message if no dataset is loaded
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Return error message for any other exceptions
        return jsonify({"error": "An unexpected error occurred"}), 500

# Define route for finding similarities in the dataset
@app.route('/find_similarities', methods=['POST'])
@inject
def find_similarities():
    try:
        # Find similarities using the Spagbol instance
        similarities = spagbol_instance.find_similarities()
        # Return the similarities
        return jsonify(similarities), 200
    except NoDatasetError as e:
        # Return error message if no dataset is loaded
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Return error message for any other exceptions
        return jsonify({"error": "An unexpected error occurred"}), 500

# Define route for deleting a data point
@app.route('/delete_data_point', methods=['DELETE'])
@inject
def delete_data_point():
    # Parse request content as JSON
    data_point_id = request.json.get('id')
    try:
        # Delete the data point using the Spagbol instance
        spagbol_instance.delete_data_point(data_point_id)
        # Return success message
        return jsonify({"message": "Data point deleted successfully"}), 200
    except NoDatasetError as e:
        # Return error message if no dataset is loaded
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Return error message for any other exceptions
        return jsonify({"error": "An unexpected error occurred"}), 500

# Define route for applying clustering to the dataset
@app.route('/apply_clustering', methods=['POST'])
@inject
def apply_clustering():
    try:
        # Apply clustering using the Spagbol instance
        clustering_result = spagbol_instance.apply_clustering()
        # Return the clustering result
        return jsonify(clustering_result), 200
    except NoDatasetError as e:
        # Return error message if no dataset is loaded
        return jsonify({"error": str(e)}), 400
    except ClusteringError as e:
        # Return error message for clustering errors
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        # Return error message for any other exceptions
        return jsonify({"error": "An unexpected error occurred"}), 500

# Start the Flask application if this script is the main program
if __name__ == '__main__':
    app.run(debug=True)