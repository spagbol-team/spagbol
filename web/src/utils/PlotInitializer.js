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

import Plotly from 'plotly.js-dist-min'

/**
 * Class representing a PlotInitializer.
 * @class
 * Usage:
 * const plotInitializer = new PlotInitializer(data, inputSrc, outputSrc);
 * await plotInitializer.initPlot();
 */

export default class PlotInitializer {
  #INSTRUCTION_NAME = 'Instructions'
  #OUTPUT_NAME = 'Output'

  #TRACE_FORMAT = {
    x: [1, 2, 3, 4],
    y: [10, 15, 13, 17],
    mode: 'markers',
    type: 'scatter',
    // colorscale: 'Bluered',
    name: this.#INSTRUCTION_NAME,
    marker: {
      color: [],
      colorscale: 'Electric',
      size: 8,
    },
  };

  #DEFAULT_LAYOUT = {
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

  #CONFIG = {
    responsive: false
  }

  #UNREMOVED_DATA = 3

  constructor(data) {
    this.data = data;
    /**
     * TODO: 
     * no need to separate inputSrc and outputSRC
     */
    // this.inputSrc = JSON.parse(JSON.stringify(data))
    // this.outputSrc = JSON.parse(JSON.stringify(data))
    // this.inputSrc = inputSrc
    // this.outputSrc = outputSrc
    this.output_x = [];
    this.output_y = [];
    this.instruction_x = [];
    this.instruction_y = [];
    this.text_insturction = [];
    this.text_output = [];
    this.root = document.getElementById('chart1')
    this.chart = null
    this.chartId = 'chart1'
    this.settings = {
      enableTracing: true
    }
  }

  /**
   * Initialization of the plotly chart
   * 
   * TODO: 
   * no need to separate inputSrc and outputtSrc
   */
  async initPlot() {
    console.log("Initializing plot")

    this.data.map(rs => {
      this.instruction_x.push(rs.instruction_x)
      this.instruction_y.push(rs.instruction_y)
      // if (max_y_instruction < rs.instruction_y) max_y_instruction = rs.instruction_y
      this.text_insturction.push(this.#createInputText(rs))

      this.output_x.push(rs.output_x)
      this.output_y.push(rs.output_y)
      // this.output_y.push(rs.output_y + OFFSET)
      this.text_output.push(this.#createOutputText(rs))
    })

    const data1 = JSON.parse(JSON.stringify(this.#TRACE_FORMAT))
    data1.marker.color = this.instruction_y
    data1.x = this.instruction_x
    data1.y = this.instruction_y
    data1.z = [...this.instruction_y]
    // data1['marker.size'] = sizes
    // data1.marker.size = sizes
    data1.text = this.text_insturction
    // 2nd Layout
    const data2 = JSON.parse(JSON.stringify(this.#TRACE_FORMAT))
    data2.name = this.#OUTPUT_NAME
    data2.marker.color = this.output_y
    data2.marker.cmin = Math.min(...this.instruction_y)
    data2.marker.cmax = Math.max(...this.output_y)
    data2.marker.colorbar = {
      title: 'Instruction & Answers Cluster',
      titleside: 'right',
      thickness: 10,
      tickfont: {
        size: 8
      }
    }

    data2.x = this.output_x
    data2.y = this.output_y
    data2.text = this.text_output

    const layout1 = JSON.parse(JSON.stringify(this.#DEFAULT_LAYOUT))
    layout1.title = 'Clustered 2D Plot of Instructions & Answers Embedding'
    this.chart = await Plotly.newPlot(this.chartId, {
      "data": [
        data1,
        data2,
        this.addRedHorizontalLine()
      ],
      "layout": layout1,
    }, this.#CONFIG)
  }

  /**
   * Adds documentation for the method.
   * 
   * @param {Object} options - The options for the method.
   * @param {Function} options.setInstructionPointsIdx - The function to set the indices of clicked input points.
   * @param {Function} options.setOutputPointsIdx - The function to set the indices of clicked output points.
   */
  addRedHorizontalLine() {
    const max = Math.max(...this.output_y);
    const min = Math.min(...this.instruction_y);
    const median = (max + min) / 2
    const lineData = {
      x: [
        Math.min(...[...this.instruction_x, ...this.output_x]),
        Math.max(...[...this.instruction_x, ...this.output_x])
    ],
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

  /**
   * Adds documentation for the method.
   * 
   * @param {Object} options - The options for the method.
   * @param {Function} options.setInstructionPointsIdx - The function to set the indices of clicked input points.
   * @param {Function} options.setOutputPointsIdx - The function to set the indices of clicked output points.
   */
  isOutputData(point) {
    return point.data.name === this.#OUTPUT_NAME
  }

  #createInputText(dataPoint) {
    return `input: ${dataPoint.input}\nword count: ${dataPoint.instruction_word_count}\navg word len: ${dataPoint.instruction_avg_word_len}`
  }

  #createOutputText(dataPoint) {
    return `output: ${dataPoint.output}\nword count: ${dataPoint.output_word_count}\navg word len: ${dataPoint.output_avg_word_len}`
  }

  /**
   * Setter method for this.settings
   * 
   * @param {Boolean} value - The settings object.
   */
  setEnableTracing(value) {
    this.settings.enableTracing = value;
  }
  

  /**
   * Adds a mark point to the chart.
   * 
   * @param {number[]} xPoints - The x-coordinates of the mark point.
   * @param {number[]} yPoints - The y-coordinates of the mark point.
   * @param {string} name - The name of the mark point.
   * @param {Object} point - The point object.
   */  
  async addMarkPoint(xPoints, yPoints, name, point) {
    const dataProps = {
      type: 'scatter',
      mode: 'markers',
      marker: {'color': 'red'}
    }

    Plotly.addTraces(this.root, {
      ...dataProps,
      x: xPoints,
      y: yPoints,
      name: name + ' input',
      prev_color: point.data.marker.color,
      text: [
        this.data[point.pointIndex].input,
        this.data[point.pointIndex].output
      ],
    })
  }

  /**
   * Adds a line trace to the chart.
   * 
   * @param {number[]} xPoints - The x-coordinates of the line.
   * @param {number[]} yPoints - The y-coordinates of the line.
   */  
  async addLine(xPoints, yPoints) {
    return Plotly.addTraces(this.root, {
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

  /**
   * Resets all traces in the chart.
   */
  resetTraces() {
    console.log('resetting traces')
    while(this.chart.data.length > this.#UNREMOVED_DATA) {
      Plotly.deleteTraces(this.root, this.#UNREMOVED_DATA)
    }
  }

  /**
   * Adds a chart on click event.
   * triggered when user click a point or the chart itself.
   * based on plotly_click
   * @param {Function} onEventData - Callback that is called when data about point clicked is ready
   */
  addChartOnClickEvent(onEventData) {
    this.chart.on('plotly_click', (eventData) => {

      console.log('on plotly_click')
      const points = eventData.points;

      const clickedName = `Clicked`
      let normalizedInput = []
      let normalizedOutput = []
      const clickedInputIdx = []
      const clickedOutputIdx = [] 
      points.map(point => {
        if (
          this.chart.data.length > this.#UNREMOVED_DATA ||
          point.fullData.name === clickedName
        ) {
          this.resetTraces()
        } else {
          const target_x = this.isOutputData(point) ? this.instruction_x: this.output_x
          const target_y = this.isOutputData(point) ? this.instruction_y: this.output_y
          const [
            normalized_input,
            normalized_output
          ] = this.pointToNormalizedData(point)
          
          clickedOutputIdx.push(point.pointIndex) // also assign corresponding input
          clickedInputIdx.push(point.pointIndex)
          normalizedOutput.push(normalized_output)
          normalizedInput.push(normalized_input)
          const xList = [point.x]
          const yList = [point.y]
          if(this.settings.enableTracing) {
            xList.push(target_x[point.pointIndex])
            yList.push(target_y[point.pointIndex])
          }

          this.addMarkPoint(
            xList,
            yList,
            clickedName,
            point
          )
          
          if(this.settings.enableTracing) {
            this.addLine(
              [point.x, target_x[point.pointIndex]],
              [point.y, target_y[point.pointIndex]]
            ).then(res => {
              console.log('point created', res)
            })
          }
        }
      });

      if(onEventData) onEventData(normalizedInput, clickedInputIdx, normalizedOutput, clickedOutputIdx)
    })
  }

  /**
   * Adds a chart on selected event.
   * 
   * @param {Object} options - The options for the event.
   * @param {Function} options.onEventData - The callback function to be called when there is event data. *_idxs means list of index of selected points, *_normalized means object ready for selected points
   * @param {Function} options.onEmptyData - The callback function to be called when there is no event data.
   */
  addChartOnSelectedEvent({onSelectionStart, onEventData, onEmptyData}) {
    this.chart.on('plotly_selected', (eventData) => {
      console.log('on selected', eventData)
      if (!eventData) {
        this.resetTraces()
        onEmptyData()
        return
      }
      if (onSelectionStart) onSelectionStart()

      const selectedPoints = eventData.points;
      // Do something with the selected points
      const normalized_instruction = []
      const normalized_output = []
      const instructions_idxs = []
      const output_idxs = []
      const lineCreation = []
      selectedPoints.map(sp => {
        const [
          input,
          output,
        ] = this.pointToNormalizedData(sp)
        if(this.settings.enableTracing) {
          if(sp.data.name === this.#INSTRUCTION_NAME) {
            const linePromise = this.addLine(
              [sp.x, this.output_x[sp.pointIndex]],
              [sp.y, this.output_y[sp.pointIndex]]
            )
            lineCreation.push(linePromise)
          } else {
            const linePromise = this.addLine(
              [sp.x, this.instruction_x[sp.pointIndex]],
              [sp.y, this.instruction_y[sp.pointIndex]]
            )
            lineCreation.push(linePromise)
          }
        }

        normalized_instruction.push(input)
        instructions_idxs.push(sp.pointIndex)
        normalized_output.push(output)
        output_idxs.push(sp.pointIndex)
      })
      Promise.all(lineCreation)
      .then(() => {
        onEventData(normalized_instruction, instructions_idxs, normalized_output, output_idxs)
      })
    })
  }

  /**
   * Gives point index and normalized data so that it's ready for use in table UI
   * @param {*} point 
   * TODO: combine pointIndex so that we don't need two object
   */
  pointToNormalizedData(point) {
    console.log("data", this.data[point.pointIndex])
    const normalized_input = {
      instruction_x: this.data[point.pointIndex].instruction_x,
      instruction_y: this.data[point.pointIndex].instruction_y,
      input: this.data[point.pointIndex].input,
      instruction_word_count: this.data[point.pointIndex].instruction_word_count,
      instruction_avg_word_len: this.data[point.pointIndex].instruction_avg_word_len,
      idx: point.pointIndex,
    }
    const normalized_output = {
      output_x: this.data[point.pointIndex].output_x,
      output_y: this.data[point.pointIndex].output_y,
      output: this.data[point.pointIndex].output,
      output_word_count: this.data[point.pointIndex].output_word_count,
      output_avg_word_len: this.data[point.pointIndex].output_avg_word_len,
      idx: point.pointIndex,
    }
    return [normalized_input, normalized_output]
  }
  
  /**
   * Adds documentation for the method.
   * 
   * @param {Object} options - The options for the method.
   * @param {Function} options.setInstructionPointsIdx - The function to set the indices of clicked input points.
   * @param {Function} options.setOutputPointsIdx - The function to set the indices of clicked output points.
   */
  removeChartFromDOM() {
    const chartElement = document.getElementById(this.chartId);
    if (chartElement) {
      Plotly.purge(chartElement);
      chartElement.innerHTML = '';
    }
  }
}
