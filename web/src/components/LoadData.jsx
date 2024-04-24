import React, { useState } from 'react';
import { postData } from '@/api/apiService';
import { Input } from './Input';
import { extractFormValues } from '@/utils/form';
import clsx from 'clsx';

export const LoadData = ({ onLoaded }) => {
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    const formData = extractFormValues(event);
    const location = formData.filePath;
    try {
        alert('Hang tight while we load your data...')
        const response = await postData('load_data', { location });
        if (response.message === 'Data loaded and embeddings created successfully') {
          onLoaded(response.data);
        } else {
          console.log('Data load unsuccessful:', response.message); 
          alert('Failed to load data: ' + response.message);
        }
    } catch (error) {
        console.error('Error during data load:', error); 
        alert('Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-4">
      <Input id="filePath" placeholder="Insert file path, should be absolute path" disabled={loading}></Input>
      <button type="submit" className={clsx("bg-blue-500 text-white px-4 rounded-lg", { 'bg-slate-500': loading })} disabled={loading}>Load Data</button>
    </form>
  );
};