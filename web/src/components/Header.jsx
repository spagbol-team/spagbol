/*
 * Copyright 2023 Spaghetti team
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */

// import { Scatter } from '@/components/Charts'
import React from 'react';
import {findBySimiliarity} from '@/api';
import {SearchInput} from '@/components/Input';
import {useChartData} from '@/context/chart';
import {useSettings} from '@/context/settings';

/**
 * @component
 * @return {JSX.Element} Header component.
 */
export function Header() {
  const {
    data,
    setSearchedData,
    setShownInstructionData,
    setShownOutputData,
    setIsTextSearching,
  } = useChartData();
  const {tracing, setTracing, searchByFamiliarity, setSearchByFamiliarity} =
    useSettings();

  /**
   * Find words based on the given text.
   * @param {string} text - The text to search for.
   * @return {Promise<void>}
   */
  async function findWords(text) {
    if (text) {
      let filtered = [];
      if (!searchByFamiliarity) {
        filtered = data.filter(
            (dt) =>
              dt.instruction.includes(text) ||
            dt.input.includes(text) ||
            dt.output.includes(text),
        );
      } else {
        filtered = await findBySimiliarity(data, text);
      }
      setSearchedData([...filtered]);
      setShownInstructionData(filtered);
      setShownOutputData(filtered);
      setIsTextSearching(true);
    } else {
      setSearchedData(null);
      setShownInstructionData(null);
      setShownOutputData(null);
      setIsTextSearching(false);
    }
  }

  return (
    <div
      className="w-screen flex lg:grid lg:grid-cols-3
    justify-center py-4 border-b border-gray-600"
    >
      <div></div>
      <div className="flex justify-center">
        <SearchInput onFind={findWords} />
      </div>
      <div className="flex">
        <div
          className="bg-secondary-bg-color items-center text-sm p-2
          border-slate-600 hover:border-gray-400 border rounded-lg w-42 ml-4"
          title="will search by familiarity instead of simple string"
        >
          <label htmlFor="disableTracing" className="flex items-center">
            <input
              id="disableTracing"
              type="checkbox"
              className="mr-2"
              onChange={(e) => setSearchByFamiliarity(e.target.checked)}
              checked={searchByFamiliarity}
            />
            Search By Familiarity
          </label>
        </div>
        <div
          className="bg-secondary-bg-color items-center text-sm p-2
        border-slate-600 hover:border-gray-400 border rounded-lg w-36 ml-4"
        >
          <label htmlFor="disableTracing" className="flex items-center">
            <input
              id="disableTracing"
              type="checkbox"
              className="mr-2"
              onChange={(e) => setTracing(e.target.checked)}
              checked={tracing}
            />
            Enable tracing
          </label>
        </div>
      </div>
    </div>
  );
}
