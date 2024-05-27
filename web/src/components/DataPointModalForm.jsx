import React, { useEffect, useState } from 'react';
import { TextAreaInput } from './TextAreaInput';
import Button from './Button';

const DataPointModalForm = ({ showModal, data, onClose, onSubmit }) => {
  const [formData, setFormData] = useState({ ...data });

  useEffect(() => {
    setFormData({ ...data });
  }, [data]);

  function closeModal(e) {
    // prevent childrens onClick to trigger this
    if (e.target !== e.currentTarget) {
      return;
    }
    e.preventDefault();
    e.stopPropagation();
    onClose();
  }

  if (!showModal) {
    return <></>;
  }

  return (
    <div className="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-black bg-opacity-50" onClick={closeModal}>
      <div className="bg-gray-800 p-8 rounded-lg">
        <h2 className="text-2xl font-bold mb-4">{`Data Point ${data.type}`}</h2>
        <div className="mb-4">
          <label htmlFor="instruction" className="block text-sm font-medium text-gray-100">
            Instruction
          </label>
          <TextAreaInput
            id="instruction"
            name="instruction"
            defaultValue={data.input}
            onChange={(val) => setFormData({ ...data, input: val })}
            rows="3"
          />
        </div>
        {/* <div className="mb-4">
          <label htmlFor="input" className="block text-sm font-medium text-gray-100">
            Input
          </label>
          <TextAreaInput
            id="input"
            name="input"
            defaultValue={data.input}
            onChange={(val) => setFormData({ ...data, input: val })}
            rows="3"
          />
        </div> */}
        <div className="mb-4">
          <label htmlFor="output" className="block text-sm font-medium text-gray-100">
            Output
          </label>
          <TextAreaInput
            id="output"
            name="output"
            defaultValue={data.output}
            onChange={(val) => setFormData({ ...data, output: val })}
            rows="3"
            // className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
          />
        </div>
        <div className="flex justify-end">
          <Button onClick={onClose} className="mr-2 px-4 py-2 bg-gray-500 text-gray-200 rounded-md hover:bg-gray-100">Close</Button>
          <Button onClick={() => {
            onClose();
            onSubmit(formData);
          }}>Submit</Button>
        </div>
      </div>
    </div>
  );
};

export default DataPointModalForm;
