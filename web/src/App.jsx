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
import { useEffect } from 'react'
import { Scatter } from '@/components/CombinedCharts'
// import { Scatter } from '@/components/Charts'
import { Table } from '@/components/Table'
import { SearchInput } from '@/components/Input'
import { ChartDataProvider, useChartData } from '@/context/chart'
import { SettingsProvider } from './context/settings'
import { Header } from '@/components/Header'

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
  const {
    data,
    setData,
    shownInstructionData,
    setShownInstructionData,
    shownOutputData,
    setShownOutputData,
  } = useChartData()

  async function getData() {
    const data = await fetch('/subset_data.json')
    const json = await data.json()
    return json
  }

  useEffect(() => {
    getData()
    .then(res => {
      let max_y_answer = 0
      const OFFSET = max_y_answer * 4 || 300
      res.map((rs,idx) => {
        if (max_y_answer < rs.output_y) max_y_answer = rs.output_y
        /** idx needed for deleting point as it will become only object and not array*/
        rs.idx = idx
      })
      res.map(rs => {
        rs.instruction_y = rs.instruction_y + OFFSET
      })
      setData(res)
    })
    .catch(err => alert(err))
  }, [])

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
