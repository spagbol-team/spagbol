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

export function Header() {
  const {
    data,
    setSearchedData,
    setShownInstructionData,
    setShownOutputData,
    setIsTextSearching,
  } = useChartData()
  const {
    tracing,
    setTracing
  } = useSettings()

  function findWords(text) {
    if (text) {
      postData({ searchQuery: text }).then(filteredData => {
        setSearchedData([...filteredData]);
        setShownInstructionData(filteredData);
        setShownOutputData(filteredData);
        setIsTextSearching(true);
      });
    } else {
      setSearchedData(null);
      setShownInstructionData(null);
      setShownOutputData(null);
      setIsTextSearching(false);
    }
  }

  return (
    <div className="w-screen grid grid-cols-3 justify-center py-4 border-b border-gray-600">
      <div className=""></div>
      <div className="flex justify-center">
        <SearchInput onFind={findWords}/>
      </div>
      <div className="bg-secondary-bg-color items-center text-sm p-2 border-slate-600 hover:border-gray-400 border rounded-lg w-36 ml-4">
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
  )
}