/*
 * Copyright 2023 Spaghetti team
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License. You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */

import './App.css'
import { useEffect } from 'react'
import { Scatter } from '@/components/CombinedCharts'
// import { Scatter } from '@/components/Charts'
import { Tables } from '@/components/Tables'
import { SearchInput } from '@/components/Input'
import { ChartDataProvider, useChartData } from '@/context/chart'

function App() {
  return (
    <ChartDataProvider>
      <HomePage />
    </ChartDataProvider>
  )
}

const INSTRUCTION_KEY = ['input', 'instruction_word_count', 'instruction_avg_word_len', 'instruction_x', 'instruction_y']
const ANSWER_KEY = ['output', 'output_word_count', 'output_avg_word_len', 'output_x', 'output_y']

function HomePage() {
  const {
    data,
    setData,
    shownInstructionData,
    setShownInstructionData,
    shownOutputData,
    setShownOutputData,
    setIsTextSearching,
  } = useChartData()

  async function getData() {
    const data = await fetch('/subset_data.json')
    const json = await data.json()
    return json
  }

  useEffect(() => {
    getData()
    .then(res => setData(res))
    .catch(err => alert(err))
  }, [])

  function previewInstructionData(partialData) {
    setShownInstructionData(partialData)
  }

  function previewOutputData(partialData) {
    setShownOutputData(partialData)
  }

  function findWords(text) {
    if (text) {
      let filtered = data.filter(dt => dt.instruction.includes(text) || dt.input.includes(text) || dt.output.includes(text))
      setShownInstructionData(filtered)
      setShownOutputData(filtered)
      setIsTextSearching(true)
    } else {
      setShownInstructionData(null)
      setShownOutputData(null)
      setIsTextSearching(false)
    }
  }

  return (
    <div className="flex flex-col bg-main-bg-color text-third-bg-color h-screen">
      <div className="w-screen flex justify-center py-4 border-b border-gray-600">
        <div>
          <SearchInput onFind={findWords}/>
          {/* Another filtering */}
          {/* <div className="bg-secondary-bg-color text-sm  border-slate-600 hover:border-gray-400 p-1 border rounded-lg w-24 mt-4">
            Treshold
          </div> */}
        </div>
      </div>
      <div className="flex flex-1 h-full flex-wrap md:flex-nowrap">
        <div className="flex-1">
          <Scatter
            data={data}
            onPreviewInstructionData={previewInstructionData}
            onPreviewOutputData={previewOutputData}
          />
        </div>
        <div className="flex-1 border-l border-slate-600 py-4 max-w-sm md:max-w-none">
          <Tables
            data={shownInstructionData ? shownInstructionData: data}
            headers={INSTRUCTION_KEY}
            dataKey={INSTRUCTION_KEY}
          />
          <Tables
            title="Answers"
            data={shownOutputData ? shownOutputData: data}
            headers={ANSWER_KEY}
            dataKey={ANSWER_KEY}
          />
        </div>
      </div>
    </div>
  )
}


export default App
