/*
 * Copyright 2023 Spaghetti team
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 */

import './App.css'
import { useEffect, useState } from 'react'
import { Scatter } from '@/components/CombinedCharts'
// import { Scatter } from '@/components/Charts'
import { Table } from '@/components/Table'
import { SearchInput } from '@/components/SearchInput'
import { ChartDataProvider, useChartData } from '@/context/chart'
import { SettingsProvider } from './context/settings'
import { Header } from '@/components/Header'
import { LoadData } from '@/components/LoadData';
import { fetchData } from './api/apiService'; 

function App() {
  return (
    <SettingsProvider>
      <ChartDataProvider>
        <HomePage />
      </ChartDataProvider>
    </SettingsProvider>
  )
}

const INSTRUCTION_KEY = ['input', 'instruction_word_count', 'instruction_avg_word_len', 'instruction_x', 'instruction_y']
const ANSWER_KEY = ['output', 'output_word_count', 'output_avg_word_len', 'output_x', 'output_y']

function HomePage() {
  const [dataLoaded, setDataLoaded] = useState(false);
  const {
    data,
    setData,
    shownInstructionData,
    setShownInstructionData,
    shownOutputData,
    setShownOutputData,
  } = useChartData()

  //async function getData() {
  //  const data = await fetch('/subset_data.json')
  //  const json = await data.json()
  //  return json
  //}

  // Define the getData function
  const getData = async () => {
    try {
      const fetchedData = await fetchData('get_data_points');
      setData(fetchedData);
    } catch (error) {
      alert('Failed to fetch data from get_data_points');
    }
  };

  // useEffect hook for other logic if needed
  useEffect(() => {
    // Any other logic that needs to run on component mount
  }, []);

  // Conditional rendering based on whether the data is loaded
  if (!dataLoaded) {
    return <LoadData onLoaded={(loadedData) => {

      loadedData = JSON.parse(loadedData);
      
      let max_y_answer = 0;
      // Assuming loadedData.data is the array you need to manipulate
      console.log(typeof loadedData);

      loadedData.forEach(item => {
        
        if (max_y_answer < item.output_y) max_y_answer = item.output_y;
      });
      const OFFSET = max_y_answer * 4 || 300;
      const adjustedData = loadedData.map((item, idx) => ({
        ...item,
        idx,
        instruction_y: item.instruction_y + OFFSET
      }));
      setDataLoaded(true);
      setData(adjustedData);
    }} />;
  }

  function previewInstructionData(partialData) {
    setShownInstructionData(partialData)
  }

  function previewOutputData(partialData) {
    setShownOutputData(partialData)
  }

  function removeOneData(idx) {
    console.log("data", idx)
  }

  return (
    <div className="flex flex-col bg-main-bg-color text-third-bg-color h-screen">
      {/* <div className="w-screen flex justify-center py-4 border-b border-gray-600">
        <div>
          <SearchInput />
        </div>
      </div> */}
      <Header />
      <div className="flex flex-1 h-full flex-wrap md:flex-nowrap">
        <div className="flex-1">
          <Scatter
            data={data}
            onPreviewInstructionData={previewInstructionData}
            onPreviewOutputData={previewOutputData}
          />
        </div>
        <div className="flex-1 border-l border-slate-600 py-4 max-w-sm md:max-w-none">
          <Table
            data={shownInstructionData ? shownInstructionData: data}
            headers={INSTRUCTION_KEY}
            dataKey={INSTRUCTION_KEY}
            onRemoveData={removeOneData}
          />
          <Table
            title="Answers"
            data={shownOutputData ? shownOutputData: data}
            headers={ANSWER_KEY}
            dataKey={ANSWER_KEY}
            onRemoveData={removeOneData}
          />
        </div>
      </div>
    </div>
  )
}


export default App
