/*
 * Copyright 2023 Spaghetti team
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */

import './App.css';
import React, {useEffect} from 'react';
import {Scatter} from '@/components/CombinedCharts';
// import { Scatter } from '@/components/Charts'
import {Table} from '@/components/Table';
import {Header} from '@/components/Header';
import {ChartDataProvider, useChartData} from '@/context/chart';
import {SettingsProvider} from '@/context/settings';
import {fetchFirstData} from '@/api';

/**
 * @component
 * @return {JSX.Element} Header component.
 */
function App() {
  return (
    <SettingsProvider>
      <ChartDataProvider>
        <HomePage />
      </ChartDataProvider>
    </SettingsProvider>
  );
}

// const FULL_INSTRUCTION_KEY =
// ['input', 'instruction_word_count',
// 'instruction_avg_word_len', 'instruction_x', 'instruction_y']
const INSTRUCTION_KEY = ['instruction'];
// const FULL_ANSWER_KEY =
// ['output', 'output_word_count',
// 'output_avg_word_len', 'output_x', 'output_y']
const ANSWER_KEY = ['output'];

/**
 * @component
 * @return {JSX.Element} Header component.
 */
function HomePage() {
  const {
    data,
    setData,
    shownInstructionData,
    setShownInstructionData,
    shownOutputData,
    setShownOutputData,
  } = useChartData();

  useEffect(() => {
    fetchFirstData()
        .then((res) => {
          let maxYAnswer = 0;
          const OFFSET = maxYAnswer * 4 || 300;
          res.map((rs, idx) => {
            if (maxYAnswer < rs.output_y) maxYAnswer = rs.output_y;
            /** idx needed for deleting point as
           * it will become only object and not array */
            rs.idx = idx;
          });
          res.map((rs) => {
            rs.instruction_y += OFFSET;
          });
          setData(res);
        })
        .catch((err) => alert(err));
  }, []);

  /**
   * Preview instruction data.
   * @param {any} partialData - Partial data to preview.
   */
  function previewInstructionData(partialData) {
    setShownInstructionData(partialData);
  }

  /**
   * Preview output data.
   * @param {any} partialData - Partial data to preview.
   */
  function previewOutputData(partialData) {
    setShownOutputData(partialData);
  }

  /**
   * Remove one data.
   * @param {number} idx - Index of the data to remove.
   */
  function removeOneData(idx) {
    console.log('data', idx);
  }

  return (
    <div
      className="flex flex-col bg-main-bg-color
    text-third-bg-color h-screen"
    >
      <Header />
      <div className="flex flex-1 h-full flex-wrap lg:flex-nowrap">
        <div className="flex-1">
          <Scatter
            data={data}
            onPreviewInstructionData={previewInstructionData}
            onPreviewOutputData={previewOutputData}
          />
        </div>
        <div
          className="flex-1 border-l border-slate-600
        py-4 max-w-sm md:max-w-none"
        >
          <Table
            data={shownInstructionData || data}
            headers={INSTRUCTION_KEY}
            dataKey={INSTRUCTION_KEY}
            onRemoveData={removeOneData}
          />
          <Table
            title="Answers"
            data={shownOutputData || data}
            headers={ANSWER_KEY}
            dataKey={ANSWER_KEY}
            onRemoveData={removeOneData}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
