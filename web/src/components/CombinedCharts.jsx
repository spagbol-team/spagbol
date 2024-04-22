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

import { useEffect, useRef, useState } from 'react'
import { useChartData } from '@/context/chart'
import PlotInitializer from '@/utils/PlotInitializer'
import { useSettings } from '@/context/settings'


export function Scatter({}) {
  // var data_template = [trace1, trace3];
  const [onPreview, setOnPreview] = useState(new Set())

  /**
   * TODO:
   * - Combine instructionPointsIdx and outputPointsIdx to shownInstructionData and shownOutputData
   */
  const [instructionPointsIdx, setInstructionPointsIdx] = useState([])
  const [outputPointsIdx, setOutputPointsIdx] = useState([])
  const [loading, setLoading] = useState('')
  const {
    data,
    setData,
    searchedData,
    setShownInstructionData,
    setShownOutputData,
    isTextSearching,
  } = useChartData()
  const {
    tracing,
  } = useSettings()
  const previewRef = useRef()
  previewRef.current = onPreview
  const plotRef = useRef(null)

  useEffect(() => {
    if(plotRef.current) plotRef.current.setEnableTracing(tracing)
  }, [tracing])

  async function initPlotClass() {
    const inputSrc = isTextSearching ? searchedData: data
    // const outputSrc = isTextSearching ? searchedData: data
    const plot1 = new PlotInitializer(inputSrc)
    // const plot1 = new PlotInitializer(data, inputSrc, outputSrc)
    await plot1.initPlot()
    plot1.addChartOnClickEvent((
      normalizedInput,
      clickedInputIdx,
      normalizedOutput,
      clickedOutputIdx
    ) => {
      // give null if no point to use view data again
      setShownInstructionData(normalizedInput.length ? normalizedInput: null)
      setShownOutputData(normalizedOutput.length ? normalizedOutput: null)
      setInstructionPointsIdx(clickedInputIdx)
      setOutputPointsIdx(clickedOutputIdx)
    })
    plot1.addChartOnSelectedEvent({
      onSelectionStart: () => {
        setLoading('Creating Lines')
      },
      onEventData: (
        normalized_instruction,
        instructions_idxs,
        normalized_output,
        output_idxs,
      ) => {
        setLoading('')
        const newPreview = new Set(previewRef.current)
        if(instructions_idxs.length) {
          setInstructionPointsIdx(instructions_idxs)
          setShownInstructionData(normalized_instruction)
          newPreview.add('instruction')
        }
        if(output_idxs.length) {
          setOutputPointsIdx(output_idxs)
          setShownOutputData(normalized_output)
          newPreview.add('output')
          // newPreview += ';output'
        }
        // create lines on selected points
        setOnPreview(newPreview)
      },
      onEmptyData: () => {
        setLoading('')
        setInstructionPointsIdx([])
        setOutputPointsIdx([])
        const newPreview = new Set(previewRef.current)
        newPreview.delete('instruction')
        newPreview.delete('output')
        setOnPreview(newPreview)
        setShownInstructionData(null)
        setShownOutputData(null)
      }
    })
    plotRef.current = plot1
    return plot1
  }

  useEffect(() => {
    // if(data.length) initPlot()
    let chart
    if(data.length) initPlotClass().then(res => chart = res)

    return () => {
      if(chart) chart.removeChartFromDOM()
    }
  }, [data, isTextSearching])

  useEffect(() => {
    let chart
    if(isTextSearching) initPlotClass().then(res => chart = res)

    return () => {
      if(chart) chart.removeChartFromDOM()
    }
  }, [searchedData])

  function deletePoints() {
    const newData = [...data]
    const toBeRemoved = [...outputPointsIdx, ...instructionPointsIdx]

    toBeRemoved.map(ipi => {
      newData.splice(ipi, 1)
    })
    setData(newData)
    setShownOutputData(null)
    setOutputPointsIdx([])
    setInstructionPointsIdx([])
    setShownInstructionData(null)
  }

  return (
    <>
      <div id="chart1" className="min-h-[85%]"></div>
      <div className="w-full flex justify-end">
        <div>{loading}</div>
        <button
          className="px-2 py-0 bg-red-500 mx-10 z-10 disabled:bg-gray-600"
          onClick={() => deletePoints()}
          disabled={!outputPointsIdx.length && !instructionPointsIdx.length}
        >
          Delete Points 
        </button>
      </div>
    </>
  )
}
