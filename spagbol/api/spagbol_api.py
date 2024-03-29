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
    # Bind Spagbol class to itself so the injector creates the instance
    binder.bind(Spagbol, to=Spagbol, scope=singleton)

# Apply the dependency injection configuration to the Flask app
FlaskInjector(app=app, modules=[configure])

# Define route for loading data into the system
@app.route('/load_data', methods=['POST'])
@inject
def load_data(spagbol_instance: Spagbol):
    # Parse request content as JSON
    content = request.json
    try:
        # Extract the dataset location from the request
        dataset_location = content['location']
        # Load data using the Spagbol instance
        spagbol_instance.load_data(dataset_location)
        # Return success message
        return jsonify({"message": "Data loaded successfully"}), 200
    except KeyError as e:
        # Return error message for missing request keys
        return jsonify({"error": f"Missing key in request: {str(e)}"}), 400
    except Exception as e:
        # Return error message for any other exceptions
        return jsonify({"error": "An unexpected error occurred"}), 500
    
@app.route('/get_data_points', methods=['GET'])
@inject
def get_data_points(spagbol_instance: Spagbol):
    # Convert query parameters to a dictionary
    criteria = request.args.to_dict()
    try:
        # Retrieve data points from Spagbol instance based on criteria
        data_points = spagbol_instance.get_data_points(criteria)
        # Return the data points as JSON with a 200 OK status
        return jsonify(data_points), 200
    except Exception as e:
        # Return an error message if an exception occurs during retrieval
        return jsonify({"error": "An error occurred while retrieving data points"}), 500
    
@app.route('/add_data_point', methods=['POST'])
@inject
def add_data_point(spagbol_instance: Spagbol):
    # Parse the incoming request data as JSON
    new_data_point = request.json
    try:
        # Add the new data point to the Spagbol instance
        spagbol_instance.add_data_point(new_data_point)
        # Return a success message with a 201 Created status
        return jsonify({"message": "Data point added successfully"}), 201
    except Exception as e:
        # Return an error message if an exception occurs during addition
        return jsonify({"error": "An error occurred while adding the data point"}), 500

# Define route for editing a data point
@app.route('/edit_data_point', methods=['POST'])
@inject
def edit_data_point(spagbol_instance: Spagbol):
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
    
# Define route for deleting a data point
@app.route('/delete_data_point', methods=['DELETE'])
@inject
def delete_data_point(spagbol_instance: Spagbol):
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
    
# Define route for batch updating data points
@app.route('/batch_update_data_points', methods=['PUT'])
@inject
def batch_update_data_points(spagbol_instance: Spagbol):
    # Parse request content as JSON for batch update
    data_points = request.json
    try:
        # Perform batch update of data points using the Spagbol instance
        spagbol_instance.batch_update_data_points(data_points)
        # Return success message if update is successful
        return jsonify({"message": "Data points updated successfully"}), 200
    except Exception as e:
        # Return error message if an exception occurs during batch update
        return jsonify({"error": "An error occurred while updating data points"}), 500

# Define route for batch deleting data points
@app.route('/batch_delete_data_points', methods=['DELETE'])
@inject
def batch_delete_data_points(spagbol_instance: Spagbol):
    # Parse request content as JSON for batch delete
    data_point_ids = request.json
    try:
        # Perform batch deletion of data points using the Spagbol instance
        spagbol_instance.batch_delete_data_points(data_point_ids)
        # Return success message if deletion is successful
        return jsonify({"message": "Data points deleted successfully"}), 200
    except Exception as e:
        # Return error message if an exception occurs during batch deletion
        return jsonify({"error": "An error occurred while deleting data points"}), 500

# Define route for finding similarities in the dataset
@app.route('/find_similarities', methods=['POST'])
@inject
def find_similarities(spagbol_instance: Spagbol):
    # Check for Request Data if needed
    # Find similarities using the Spagbol instance
    try:
        similarities = spagbol_instance.find_similarities()
        # Return the similarities
        return jsonify(similarities), 200
    except NoDatasetError as e:
        # Return error message if no dataset is loaded
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Return error message for any other exceptions
        return jsonify({"error": "An unexpected error occurred"}), 500

# Define route for applying clustering to the dataset
@app.route('/apply_clustering', methods=['POST'])
@inject
def apply_clustering(spagbol_instance: Spagbol):
    # Check for Request Data if needed
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
    
@app.route('/export_data', methods=['GET'])
@inject
def export_data(spagbol_instance: Spagbol):
    # Retrieve query parameters as criteria for export
    criteria = request.args.to_dict()
    try:
        # Export data based on the provided criteria using the Spagbol instance
        dataset = spagbol_instance.export_data(criteria)
        # Return the exported dataset
        return jsonify(dataset), 200
    except Exception as e:
        # Return error message if an exception occurs during data export
        return jsonify({"error": "An error occurred while exporting the data"}), 500
    

@app.route('/import_data', methods=['POST'])
@inject
def import_data(spagbol_instance: Spagbol):
    # Parse request content as JSON for data import
    data_to_import = request.json
    try:
        # Import data using the Spagbol instance
        spagbol_instance.import_data(data_to_import)
        # Return success message if import is successful
        return jsonify({"message": "Data imported successfully"}), 201
    except Exception as e:
        # Return error message if an exception occurs during data import
        return jsonify({"error": "An error occurred while importing the data"}), 500


# Start the Flask application if this script is the main program
if __name__ == '__main__':
    app.run(debug=True)