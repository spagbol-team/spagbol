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
import Plotly from 'plotly.js-dist-min'
import { useChartData } from '@/context/chart'
import Button from './Button';

/**
 * THIS COMPONENT IS NOT USED ANYMORE MAYBE TEMPORARY
 */

const trace1 = {
  x: [1, 2, 3, 4],
  y: [10, 15, 13, 17],
  mode: 'markers',
  type: 'scatter',
  // colorscale: 'Bluered',
  name: 'Instructions',
  marker: {
    color: [],
    colorscale: 'Electric',
    size: 8,
    colorbar: {
      title: 'Instruction Cluster',
      titleside: 'right',
      thickness: 10,
      tickfont: {
        size: 8
      }
    },
  },
};

const trace3 = {
  x: [1, 2, 3, 4],
  y: [12, 9, 15, 12],
  mode: 'markers',
  type: 'scatter'
};

const title = {
  text: "Clustered 2D Plot of Instructions Embedding",
  font: {
    color: 'white'
  },
  x: 0,
  y: 1,
}

const DEFAULT_LAYOUT = {
  xaxis: { title: 'instructions_x' },
  yaxis: { title: 'instructions_y' },
  coloraxis: {
    colorbar: {
      title: 'Color Scale',
      titleside: 'right'
    }
  },
  paper_bgcolor: '#343541',
  plot_bgcolor: '#343541',
  font: {
    color: 'white'
  },
  showlegend: false
    // annotations: []
}

const CONFIG = {responsive: true}

export function Scatter({}) {
  // var data_template = [trace1, trace3];
  const [onPreview, setOnPreview] = useState('')
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

  async function initPlot() {
    const output_x = []
    const output_y = []
    const instruction_x = []
    const instruction_y = []
    const text_insturction = []
    const text_output = []

    const inputSrc = shownInstructionData && isTextSearching ? shownInstructionData: data
    inputSrc.map(rs => {
      console.log('cek res', rs)
      instruction_x.push(rs.instruction_x)
      instruction_y.push(rs.instruction_y)
      text_insturction.push(`input: ${rs.input}\nword count: ${rs.instruction_word_count}\navg word len: ${rs.instruction_avg_word_len}`)
    })
    const outputSrc = shownOutputData && isTextSearching ? shownOutputData: data
    outputSrc.map(rs => {
      output_x.push(rs.output_x)
      output_y.push(rs.output_y)
      text_output.push(`output: ${rs.output}\nword count: ${rs.output_word_count}\navg word len: ${rs.output_avg_word_len}`)
    })
    const data1 = JSON.parse(JSON.stringify(trace1))
    data1.marker.color = instruction_x
    data1.x = instruction_x
    data1.y = instruction_y
    data1.z = [...instruction_y]
    data1.text = text_insturction
    const layout1 = JSON.parse(JSON.stringify(DEFAULT_LAYOUT))
    layout1.title = 'Clustered 2D Plot of Instructions Embedding'
    const instruction_chart = await Plotly.newPlot('chart1', {
      "data": [data1],
      "layout": layout1,
    }, CONFIG)
    instruction_chart.on('plotly_click', (eventData) => {
      const points = eventData.points;
      const root = document.getElementById('chart1')

      const clickedName = 'Clicked Instruction'
      points.forEach(point => {
        if (instruction_chart.data.length > 1 || point.fullData.name === clickedName) {
          Plotly.deleteTraces(root, 1)
        } else {
          Plotly.addTraces(root, {
            x: [point.x],
            y: [point.y],
            type: 'scatter',
            mode: 'markers',
            marker: {'color': 'red'},
            name: clickedName,
            prev_color: point.data.marker.color,
            text: point.text
          })
        }
      });
    })
    instruction_chart.on('plotly_selected', (eventData) => {
      if (eventData) {
        const selectedPoints = eventData.points;
        // Do something with the selected points
        const normalized = []
        const idxs = []
        selectedPoints.map(sp => {
          normalized.push({
            instruction_x: sp.x,
            instruction_y: sp.y,
            input: data[sp.pointIndex].input,
            instruction_word_count: data[sp.pointIndex].instruction_word_count,
            instruction_avg_word_len: data[sp.pointIndex].instruction_avg_word_len,
          })
          idxs.push(sp.pointIndex)
        })
        setInstructionPointsIdx(idxs)
        setShownInstructionData(normalized)
        setOnPreview(`${previewRef.current};instruction`)
      } else {
        setInstructionPointsIdx([])
        setOnPreview(previewRef.current.replace('instruction',''))
        setShownInstructionData(null)
      }
    })

    // 2nd Layout
    const layout_2 = JSON.parse(JSON.stringify(DEFAULT_LAYOUT))
    layout_2.xaxis.title = 'answer_x'
    layout_2.yaxis.title = 'answer_y'
    layout_2.title = 'Clustered 2D Plot of Answers Embedding'
    const data2 = JSON.parse(JSON.stringify(trace1))
    data2.marker.colorbar.title = 'Answer Cluster'
    data2.marker.color = output_x
    data2.x = output_x
    data2.y = output_y
    data2.text = text_output
    const answer_chart = await Plotly.newPlot('chart2', {
      "data": [data2],
      "layout": layout_2,
    }, CONFIG)

    answer_chart.on('plotly_click', (eventData) => {
      const points = eventData.points;
      const root = document.getElementById('chart2')

      const clickedName = 'Clicked Instruction'
      points.forEach(point => {
        if (answer_chart.data.length > 1 || point.fullData.name === clickedName) {
          Plotly.deleteTraces(root, 1)
        } else {
          Plotly.addTraces(root, {
            x: [point.x],
            y: [point.y],
            type: 'scatter',
            mode: 'markers',
            marker: {'color': 'red'},
            name: clickedName,
            prev_color: point.data.marker.color,
            text: point.text
          })
        }
      });
    })
    answer_chart.on('plotly_selected', (eventData) => {
      if (eventData) {
        const selectedPoints = eventData.points;
        // Do something with the selected points
        const normalized = []
        const idxs = []
        selectedPoints.map(sp => {
          normalized.push({
            output_x: sp.x,
            output_y: sp.y,
            output: data[sp.pointIndex].input,
            output_word_count: data[sp.pointIndex].output_word_count,
            output_avg_word_len: data[sp.pointIndex].output_avg_word_len,
          })
          idxs.push(sp.pointIndex)
        })
        setOutputPointsIdx(idxs)
        setShownOutputData(normalized)
        setOnPreview(`${previewRef.current};answer`)
      } else {
        setOutputPointsIdx([])
        setOnPreview(previewRef.current.replace('answer',''))
        setShownOutputData(null)
      }
    })
  }

  useEffect(() => {
    if(data.length) initPlot()
  }, [data, isTextSearching])

  function deletePoints(type) {
    const newData = [...data]
    switch(type) {
      case 'instruction':
        instructionPointsIdx.map(ipi => {
          newData.splice(ipi, 1)
        })
        setData(newData)
        setShownInstructionData(null)
        break
      case 'output':
        outputPointsIdx.map(ipi => {
          newData.splice(ipi, 1)
        })
        setData(newData)
        setShownOutputData(null)
        break
    }
  }

  return (
    <>
      <div id="chart1"></div>
      <div className="w-full flex justify-end">
        <Button
          className="bg-red-500 disabled:bg-gray-600"
          onClick={() => deletePoints('instruction')}
          disabled={!onPreview.includes('instruction')}
        >
          Delete Points 
        </Button>
      </div>
      <div id="chart2"></div>
      <div className="w-full flex justify-end">
        <Button
          className="bg-red-500 disabled:bg-gray-600" 
          onClick={() => deletePoints('output')}
          disabled={!onPreview.includes('answer')}
        >
          Delete Points 
        </Button>
      </div>
    </>
  )
}
