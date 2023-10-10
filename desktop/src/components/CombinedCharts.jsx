/*
 * Copyright 2023 Spaghetti team
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing,
 * softwaredistributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
 * either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */

import React, {useEffect, useRef, useState} from 'react';
import {useChartData} from '@/context/chart';
import PlotInitializer from '@/utils/PlotInitializer';
import {useSettings} from '@/context/settings';
import {deleteDataPoints} from '@/api';

/**
 * @component
 * @return {JSX.Element} Header component.
 */
export function Scatter() {
  // var data_template = [trace1, trace3];
  const [onPreview, setOnPreview] = useState(new Set());

  /**
   * TODO:
   * - Combine instructionPointsIdx and
   * outputPointsIdx to shownInstructionData and shownOutputData
   */
  const [instructionPointsIdx, setInstructionPointsIdx] = useState([]);
  const [outputPointsIdx, setOutputPointsIdx] = useState([]);
  const [loading, setLoading] = useState('');
  const {
    data,
    setData,
    searchedData,
    setShownInstructionData,
    setShownOutputData,
    isTextSearching,
  } = useChartData();
  const {tracing} = useSettings();
  const previewRef = useRef();
  previewRef.current = onPreview;
  const plotRef = useRef(null);

  useEffect(() => {
    if (plotRef.current) plotRef.current.setEnableTracing(tracing);
  }, [tracing]);

  /**
   * Initialize the plot class.
   * @return {Promise<PlotInitializer>} The initialized plot class.
   */
  async function initPlotClass() {
    const inputSrc = isTextSearching ? searchedData : data;
    // const outputSrc = isTextSearching ? searchedData: data
    const plot1 = new PlotInitializer(inputSrc);
    // const plot1 = new PlotInitializer(data, inputSrc, outputSrc)
    await plot1.initPlot();
    plot1.addChartOnClickEvent(
        (
            normalizedInput,
            clickedInputIdx,
            normalizedOutput,
            clickedOutputIdx,
        ) => {
        // give null if no point to use view data again
          setShownInstructionData(
          normalizedInput.length ? normalizedInput : null,
          );
          setShownOutputData(normalizedOutput.length ? normalizedOutput : null);
          setInstructionPointsIdx(clickedInputIdx);
          setOutputPointsIdx(clickedOutputIdx);
        },
    );
    plot1.addChartOnSelectedEvent({
      onSelectionStart: () => {
        setLoading('Creating Lines');
      },
      onEventData: (
          normalizedInstruction,
          instructionsIdxs,
          normalizedOutput,
          outputIdxs,
      ) => {
        setLoading('');
        const newPreview = new Set(previewRef.current);
        if (instructionsIdxs.length) {
          setInstructionPointsIdx(instructionsIdxs);
          setShownInstructionData(normalizedInstruction);
          newPreview.add('instruction');
        }
        if (outputIdxs.length) {
          setOutputPointsIdx(outputIdxs);
          setShownOutputData(normalizedOutput);
          newPreview.add('output');
          // newPreview += ';output'
        }
        // create lines on selected points
        setOnPreview(newPreview);
      },
      onEmptyData: () => {
        setLoading('');
        setInstructionPointsIdx([]);
        setOutputPointsIdx([]);
        const newPreview = new Set(previewRef.current);
        newPreview.delete('instruction');
        newPreview.delete('output');
        setOnPreview(newPreview);
        setShownInstructionData(null);
        setShownOutputData(null);
      },
    });
    plotRef.current = plot1;
    return plot1;
  }

  useEffect(() => {
    // if(data.length) initPlot()
    let chart;
    if (data.length) initPlotClass().then((res) => (chart = res));

    return () => {
      if (chart) chart.removeChartFromDOM();
    };
  }, [data, isTextSearching]);

  useEffect(() => {
    let chart;
    if (isTextSearching) initPlotClass().then((res) => (chart = res));

    return () => {
      if (chart) chart.removeChartFromDOM();
    };
  }, [searchedData]);

  /**
   * Delete the selected data points.
   */
  function deletePoints() {
    const toBeRemoved = [...outputPointsIdx, ...instructionPointsIdx];
    /** might want to refetch clustering */
    deleteDataPoints(toBeRemoved, data).then((newData) => {
      setData(newData);
      setShownOutputData(null);
      setOutputPointsIdx([]);
      setInstructionPointsIdx([]);
      setShownInstructionData(null);
    });
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
  );
}
