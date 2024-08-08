import React, { useState } from 'react';
import { Input } from './Input';
import { extractFormValues } from '@/utils/form';
import { postData } from '@/api/apiService';
import { useChartData } from "@/context/chart"

export const EditDatasetForm = ({ isOpen, onClose, inputValue, outputValue, data_ids }) => {

    const {
        data: originalData,
        setData,
        shownInstructionData,
        setShownInstructionData,
        shownOutputData,
        setShownOutputData,
      } = useChartData()

    const handleSubmit = async (event) => {
        event.preventDefault()
        const formData = extractFormValues(event);
        let newData = [...originalData]
        let payload = {}
        let input_text = formData.input_text
        let output_text = formData.output_text
        data_ids.forEach((data_id) => {
            if (input_text != ""){
                if (!("input" in payload)){
                    payload["input"] = {}
                }
                payload["input"][data_id] = input_text
            }
            if(output_text != ""){
                if (!("output" in payload)){
                    payload["output"] = {}
                }
                payload["output"][data_id] = output_text
            }
        })
        let result = await postData("edit_data_points", {
            "data_points": payload
        })
        result = result["edited_data_points"]
        console.log(result)
        let input_datapoints = result["input"] ?? {}
        let output_datapoints = result["output"] ?? {}
        console.log(result)

        let max_y_answer = 0;
        newData.forEach(item => {
            if (max_y_answer < item.output_y) max_y_answer = item.output_y;
        });
        const OFFSET = max_y_answer * 4 || 300;
        
        for (const [data_id, input_coords] of Object.entries(input_datapoints)){
            console.log(newData[data_id])
            newData[data_id]["instruction_x"] = input_coords[0] 
            newData[data_id]["instruction_y"] = input_coords[1] + OFFSET
            newData[data_id]["input"] = input_text
            if (shownInstructionData != null){
                shownInstructionData.forEach((data_point) => {
                    if (data_point.idx == data_id){
                        data_point["instruction_x"] = input_coords[0]
                        data_point["instruction_y"] = input_coords[1] + OFFSET
                        data_point["input"] = input_text
                        return
                    }                    
                })
                setShownInstructionData(shownInstructionData)
            }
        }
        for (const [data_id, output_coords] of Object.entries(output_datapoints)){
            newData[data_id]["output_x"] = output_coords[0]
            newData[data_id]["output_y"] = output_coords[1]
            newData[data_id]["output"] = output_text
            if (shownOutputData != null){
                shownOutputData.forEach((data_point) => {
                    if (data_point.idx == data_id){
                        data_point["output_x"] = output_coords[0]
                        data_point["output_y"] = output_coords[1] 
                        data_point["output"] = output_text
                        return
                    }                    
                })
                setShownOutputData(shownOutputData)
            }
        }
        
        setData(newData)
        if (shownInstructionData == null){
            setShownInstructionData(null)
        }
        if (shownOutputData == null){
            setShownOutputData(null)
        }
        onClose()
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
                <h2>Edit Data</h2>
                <form onSubmit={handleSubmit} className='huggingface_export_data'>
                    <div className="flex gap-4">
                        <Input id="input_text"  defaultValue={inputValue} placeholder="Insert new input text"></Input>
                    </div>
                    <div className="flex gap-4">
                        <Input id="output_text" defaultValue={outputValue} placeholder="Insert new output text (Optional)"></Input>
                    </div>
                    <div>
                        <button 
                            className="flex items-center justify-center w-1/2 px-3 py-2 text-sm 
                            capitalize transition-colors duration-200 border rounded-lg sm:w-auto 
                            gap-x-2 bg-gray-900 text-gray-200 border-gray-700 hover:bg-gray-800" type="submit"
                        >
                            Edit
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}