import React, { useState } from 'react';
import { Input } from './Input';
import { extractFormValues } from '@/utils/form';
import { postData } from '@/api/apiService';

export const HuggingFaceExportForm = ({ isOpen, onClose }) => {

    const handleSubmit = async (event) => {
        event.preventDefault()
        const formData = extractFormValues(event);
        let make_private = document.getElementById("private").checked 
        try{
            let result = await postData("export_to_huggingface", {
                "organization": formData.organization,
                "dataset_id": formData.dataset_id,
                "private": make_private
            })
            let alert_string = "Dataset successfully exported to " + formData.organization + "/" + formData.dataset_id
            if (formData.private){
                alert_string += " as a private dataset."
            }
            alert(alert_string)
            console.log(result)
        }
        catch(error) {
            console.error(error)
        }
        finally{
            onClose()
        }
    }

    if (!isOpen) return null

    return (
        <div className="popup-overlay">
            <div className="popup">
                <button className="px-0 py-0 text-gray-100 transition-colors duration-200 rounded-lg bg-gray-600 close-btn" onClick={onClose}>
                    <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>
                <h2>Export To Huggingface</h2>
                <form onSubmit={handleSubmit} className='huggingface_export_data'>
                    <div className="flex gap-4">
                        <Input id="organization" placeholder="Insert huggingface organization name"></Input>
                    </div>
                    <div className="flex gap-4">
                        <Input id="dataset_id" placeholder="Insert dataset id"></Input>
                    </div>
                    <div className="flex gap-4 bg-secondary-bg-color items-center text-sm p-2 border-slate-600 hover:border-gray-400 border rounded-lg w-36 ml-4">
                        <label htmlFor="private" className="flex items-center">  
                            <input id="private" type="checkbox" className='mr-2' />

                            Make private
                        </label>
                    </div>
                    <div>
                        <button 
                            className="flex items-center justify-center w-1/2 px-3 py-2 text-sm 
                            capitalize transition-colors duration-200 border rounded-lg sm:w-auto 
                            gap-x-2 bg-gray-900 text-gray-200 border-gray-700 hover:bg-gray-800" type="submit"
                        >
                            Export
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}