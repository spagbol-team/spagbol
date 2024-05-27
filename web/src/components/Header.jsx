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

// import { Scatter } from '@/components/Charts'
import { SearchInput } from '@/components/SearchInput'
import { useChartData } from '@/context/chart'
import { useSettings } from '@/context/settings'
import { postData } from '../api/apiService'
import Button from './Button'
import { saveToLocalStorage } from '@/utils/localStorage'
import { throttle } from '@/utils/helper'
import { Checkbox } from './Checkbox'

export function Header() {
  const {
    data,
    setData,
    setSearchedData,
    setShownInstructionData,
    setShownOutputData,
    setIsTextSearching,
  } = useChartData()
  const {
    tracing,
    setTracing,
    useSimiliaritySearch,
    setUseSimiliaritySearch
  } = useSettings()

  function findWords(text) {
    if (text) {
      if (useSimiliaritySearch) {
        postData('find_similarities', { searchQuery: text }).then(filteredData => {
          setSearchedData([...filteredData]);
          setShownInstructionData(filteredData);
          setShownOutputData(filteredData);
          setIsTextSearching(true);
        });
      } else {
        setIsTextSearching(true);
        const filteredData = data.filter(item => item.input.includes(text) || item.output.includes(text));
        setSearchedData([...filteredData]);
        setShownInstructionData(filteredData);
        setShownOutputData(filteredData);
        setIsTextSearching(true);
      }
      
    } else {
      resetDataState();
    }
  }

  function resetDataState() {
    setSearchedData(null);
    setShownInstructionData(null);
    setShownOutputData(null);
    setIsTextSearching(false);
  }

  function onLoadAnotherData() {
    resetDataState();
    setData(null);
    saveToLocalStorage('data', null);
  }

  return (
    <div className="w-screen grid grid-cols-3 justify-center py-4 border-b border-gray-600">
      <div className="">
      </div>
      <div className="flex justify-center">
        <SearchInput onFind={throttle(findWords)}/>
      </div>
      <div className="flex gap-2">
        <div>
          <Button onClick={onLoadAnotherData}>Load new data</Button>
        </div>
        <Checkbox
          id="similiaritySearch"
          onChange={(e) => setUseSimiliaritySearch(e.target.checked)}
          checked={useSimiliaritySearch}
          label="Similiarity search"
        />
        <Checkbox
          id="disableTracing"
          onChange={(e) => setTracing(e.target.checked)}
          checked={tracing}
          label="Enable tracing"
        />
      </div>
    </div>
  )
}