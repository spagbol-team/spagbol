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

import { useEffect, useRef, useState } from 'react'
import Plotly from 'plotly.js-dist-min'
import { useChartData } from '@/context/chart'

const INSTRUCTION_NAME = 'Instructions'
const OUTPUT_NAME = 'Output'

const trace1 = {
  x: [1, 2, 3, 4],
  y: [10, 15, 13, 17],
  mode: 'markers',
  type: 'scatter',
  // colorscale: 'Bluered',
  name: INSTRUCTION_NAME,
  marker: {
    color: [],
    colorscale: 'Electric',
    size: 8,
  },
};

const DEFAULT_LAYOUT = {
  xaxis: { title: 'instructions_x & answers_x' },
  yaxis: { title: 'instructions_y & answers_y' },
  coloraxis: {
    colorbar: {
      title: 'Color Scale',
      titleside: 'right'
    }
  },
  // width: 580,
  // height: 500,
  paper_bgcolor: '#343541',
  plot_bgcolor: '#343541',
  font: {
    color: 'white'
  },
  showlegend: false
    // annotations: []
}

const CONFIG = {
  responsive: false
}

const UNREMOVED_DATA = 3


export function Scatter({}) {
  // var data_template = [trace1, trace3];
  const [onPreview, setOnPreview] = useState(new Set())
  const [instructionPointsIdx, setInstructionPointsIdx] = useState([])
  const [outputPointsIdx, setOutputPointsIdx] = useState([])
  const {
    data,
    setData,
    shownInstructionData,
    setShownInstructionData,
    shownOutputData,
    setShownOutputData,
    isTextSearching,
  } = useChartData()
  const previewRef = useRef()
  previewRef.current = onPreview

  /**
   * Will use class based initialization
   * On TODO List
   */
  async function initPlot() {
    console.log("Initializing plot")
    const output_x = []
    const output_y = []
    const instruction_x = []
    const instruction_y = []
    const text_insturction = []
    const text_output = []

    const inputSrc = shownInstructionData && isTextSearching ? shownInstructionData: data
    let max_y_instruction = 0
    inputSrc.map(rs => {
      instruction_x.push(rs.instruction_x)
      instruction_y.push(rs.instruction_y)
      if (max_y_instruction < rs.instruction_y) max_y_instruction  = rs.instruction_y
      text_insturction.push(`input: ${rs.input}\nword count: ${rs.instruction_word_count}\navg word len: ${rs.instruction_avg_word_len}`)
    })

    const OFFSET = max_y_instruction * 4 || 300
    const outputSrc = shownOutputData && isTextSearching ? shownOutputData: data
    outputSrc.map(rs => {
      output_x.push(rs.output_x)
      output_y.push(rs.output_y + OFFSET)
      text_output.push(`output: ${rs.output}\nword count: ${rs.output_word_count}\navg word len: ${rs.output_avg_word_len}`)
    })
    const data1 = JSON.parse(JSON.stringify(trace1))
    data1.marker.color = instruction_y
    data1.x = instruction_x
    data1.y = instruction_y
    data1.z = [...instruction_y]
    // data1['marker.size'] = sizes
    // data1.marker.size = sizes
    data1.text = text_insturction
    // 2nd Layout
    const data2 = JSON.parse(JSON.stringify(trace1))
    data2.name = OUTPUT_NAME
    data2.marker.color = output_y
    data2.marker.cmin = Math.min(...instruction_y)
    data2.marker.cmax = Math.max(...output_y)
    data2.marker.colorbar = {
      title: 'Instruction & Answers Cluster',
      titleside: 'right',
      thickness: 10,
      tickfont: {
        size: 8
      }
    }

    data2.x = output_x
    data2.y = output_y
    data2.text = text_output

    const layout1 = JSON.parse(JSON.stringify(DEFAULT_LAYOUT))
    layout1.title = 'Clustered 2D Plot of Instructions & Answers Embedding'
    const chart = await Plotly.newPlot('chart1', {
      "data": [
        data1,
        data2,
        addRedHorizontalLine(instruction_x, instruction_y, output_y)
      ],
      "layout": layout1,
    }, CONFIG)
    const root = document.getElementById('chart1')

    
    addChartOnClickEvent(root, chart, instruction_x, instruction_y, output_x, output_y)
    addChartOnSelectedEvent(root, chart, instruction_x, instruction_y, output_x, output_y)
  }

  function addChartOnSelectedEvent(root, chart, instruction_x, instruction_y, output_x, output_y) {
    chart.on('plotly_selected', (eventData) => {
      if (eventData) {
        const selectedPoints = eventData.points;
        // Do something with the selected points
        const normalized_instruction = []
        const normalized_output = []
        const instructions_idxs = []
        const output_idxs = []
        selectedPoints.map(sp => {
          if(sp.data.name === INSTRUCTION_NAME) {
            addLine(
              root,
              [sp.x, output_x[sp.pointIndex]],
              [sp.y, output_y[sp.pointIndex]]
            )
            normalized_instruction.push({
              instruction_x: sp.x,
              instruction_y: sp.y,
              input: data[sp.pointIndex].input,
              instruction_word_count: data[sp.pointIndex].instruction_word_count,
              instruction_avg_word_len: data[sp.pointIndex].instruction_avg_word_len,
            })
            instructions_idxs.push(sp.pointIndex)
          } else {
            // console.log("CEK 2", sp.x, sp.pointIndex, instruction_x[sp.pointIndex])
            addLine(
              root,
              [sp.x, instruction_x[sp.pointIndex]],
              [sp.y, instruction_y[sp.pointIndex]]
            )
            normalized_output.push({
              output_x: sp.x,
              output_y: sp.y,
              output: data[sp.pointIndex].input,
              output_word_count: data[sp.pointIndex].output_word_count,
              output_avg_word_len: data[sp.pointIndex].output_avg_word_len,
            })
            output_idxs.push(sp.pointIndex)
          }
        })

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
      } else {
        setInstructionPointsIdx([])
        setOutputPointsIdx([])
        const newPreview = previewRef.current
        newPreview.replace('instruction','')
        newPreview.replace('output','')
        setOnPreview(newPreview)
        setShownInstructionData(null)
        setShownOutputData(null)
        resetTraces(root, chart)
      }
    })
  }

  function addChartOnClickEvent(root, chart, instruction_x, instruction_y, output_x, output_y) {
    chart.on('plotly_click', (eventData) => {
      const points = eventData.points;

      const clickedName = `Clicked`
      const clickedInputIdx = []
      const clickedOutputIdx = []
      points.forEach(point => {
        if (chart.data.length > UNREMOVED_DATA || point.fullData.name === clickedName) {
          resetTraces(root, chart)
        } else {
          const target_x = isOutputData(point) ? instruction_x: output_x
          const target_y = isOutputData(point) ? instruction_y: output_y
          if (isOutputData(point)) {
            clickedOutputIdx.push(point.pointIndex)
          } else {
            clickedInputIdx.push(point.pointIndex)
          }
          addMarkPoint(
            root,
            [point.x, target_x[point.pointIndex]],
            [point.y, target_y[point.pointIndex]],
            clickedName,
            point
          )
          addLine(
            root, 
            [point.x, target_x[point.pointIndex]],
            [point.y, target_y[point.pointIndex]]
          )
          }
        });
        setInstructionPointsIdx(clickedInputIdx)
        setOutputPointsIdx(clickedOutputIdx)
    })
  }
  
  function resetTraces(root, chart) {
    while(chart.data.length > UNREMOVED_DATA) {
      Plotly.deleteTraces(root, UNREMOVED_DATA)
    }
  }

  function isOutputData(point) {
    return point.data.name === OUTPUT_NAME
  }

  function addRedHorizontalLine(xInput, yInput, yOutput) {
    const max = Math.max(...yOutput);
    const min = Math.min(...yInput);
    const median = (max + min) / 2
    const lineData = {
      x: [Math.min(...xInput), Math.max(...xInput)],
      y: [median, median],
      type: 'scatter',
      mode: 'lines',
      name: 'Input & Output Separator',
      line: {
        color: 'red',
        width: 2
      },
      showlegend: false
    };
    return lineData
  }
  

  function addLine(root, xPoints, yPoints) {
    Plotly.addTraces(root, {
      x: xPoints,
      y: yPoints,
      type: 'scatter',
      mode: 'lines',
      line: {
        color: 'green',
        width: 2
      },
      showlegend: false
    })
  }

  function addMarkPoint(root, xPoints, yPoints, name, point) {
    Plotly.addTraces(root, {
      x: xPoints,
      y: yPoints,
      type: 'scatter',
      mode: 'markers',
      marker: {'color': 'red'},
      name: name,
      prev_color: point.data.marker.color,
      text: point.text
    })
  }

  useEffect(() => {
    if(data.length) initPlot()
  }, [data, isTextSearching])

  useEffect(() => {
    if(isTextSearching) initPlot()
  }, [shownInstructionData, shownOutputData])

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
