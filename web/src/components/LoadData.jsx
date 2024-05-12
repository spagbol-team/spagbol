import React, { useState } from 'react';
import { postData } from '@/api/apiService';
import { Input } from './Input';
import { extractFormValues } from '@/utils/form';
import clsx from 'clsx';
import { toast } from 'react-toastify';

export const LoadData = ({ onLoaded }) => {
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    const formData = extractFormValues(event);
    const location = formData.filePath;
    try {
        const response = await postData('load_data', { location });
        if (response.message === 'Data loaded and embeddings created successfully') {
          onLoaded(response.data);
        } else {
          console.log('Data load unsuccessful:', response.message); 
          toast.error('Failed to load data: ' + response.message);
        }
    } catch (error) {
        console.error('Error during data load:', error); 
        toast.error('Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      <div className="flex gap-4">
        <Input id="filePath" placeholder="Insert file path, should be absolute path" disabled={loading}></Input>
        <button type="submit" className={clsx("bg-blue-500 text-white px-4 rounded-lg", { 'bg-slate-500': loading })} disabled={loading}>Load Data</button>
      </div>
      {loading && (
        <div className="relative flex items-center justify-center">
          <p className="text-blue-500 font-semibold mr-2">Loading...</p>
          <div className="animate-spin h-5 w-5 border-t-2 border-b-2 border-blue-500 rounded-full"></div>
        </div>
      )}
    </form>
  );
};