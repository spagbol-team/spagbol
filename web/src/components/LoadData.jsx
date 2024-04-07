import React, { useState } from 'react';
import { postData } from '../apiService';

export const LoadData = ({ onLoaded }) => {
  const [datasetLocation, setDatasetLocation] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await postData('load_data', { location: datasetLocation });
      console.log('Response from load_data:', response); 
      if (response.message === 'Data loaded and embeddings created successfully') {
        console.log('Data loaded successfully, calling onLoaded'); 
        onLoaded();
      } else {
        console.log('Data load unsuccessful:', response.message); 
        alert('Failed to load data: ' + response.message);
      }
    } catch (error) {
      console.error('Error during data load:', error); 
      alert('Failed to load data');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={datasetLocation}
        onChange={(e) => setDatasetLocation(e.target.value)}
        placeholder="Enter dataset location"
        required
        className="dataset-input"
      />
      <button type="submit" style={{ backgroundColor: 'RoyalBlue', color: 'white' }}>Load Data</button>
    </form>
  );
};