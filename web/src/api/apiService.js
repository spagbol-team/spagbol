
// Base URL for the Flask API
const API_BASE_URL = 'http://localhost:5000';


/**
 * Asynchronously retrieves data from the specified API endpoint.
 * @param {string} endpoint - The endpoint to fetch data from.
 * @returns {Promise<Object>} A promise that resolves with the fetched data, or rejects with an error.
 */
export const fetchData = async (endpoint) => {
  try {
    // Construct the full URL for the API request
    const url = `${API_BASE_URL}/${endpoint}`;
    // Perform the fetch operation
    const response = await fetch(url);
    // Check if the response is successful (status in the range 200-299)
    if (!response.ok) {
      // Throw an error with the status code in case of a failed response
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    // Parse and return the response body as JSON
    return await response.json();
    } catch (error) {
    console.error('Fetch error:', error);
    throw error; // Rethrow the error after logging
  }
};

/**
 * Posts data to a predefined endpoint.
 * @param {Object} data - The data to be sent to the endpoint.
 * @returns {Promise<Object>} The result of the POST operation.
 */
export const postData = async (endpoint, data) => {
  try {
    // Perform a POST request with the provided data
    const response = await fetch(`${API_BASE_URL}/${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    // Check if the response status indicates a successful request
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    // Parse the response body as JSON
    const result = await response.json();
    return result;
  } catch (error) {
    // Log any errors that occur during the post operation
    console.error('Post error:', error);
  }
};

/**
 * Deletes a data point from the server.
 * @param {number} dataPointId - The unique identifier of the data point to delete.
 * @returns {Promise<Object>} A promise that resolves with the deletion result or logs an error.
 */
export const deleteData = async (dataPointId) => {
  try {
    // Initialize the DELETE request to remove the data point
    const response = await fetch(`${API_BASE_URL}/delete_data_point`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ id: dataPointId }),
    });

    // Check if the server's response indicates a successful deletion
    if (!response.ok) {
      // If not successful, throw an error with the status code
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // Parse and return the server's response as JSON
    return await response.json();
  } catch (error) {
    // Log any errors that occur during the deletion process
    console.error('Delete error:', error);
  }
};

