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


import { createContext, useContext, useState } from "react";

const chartDataContext = createContext({});

export function ChartDataProvider({ children }) {
  const [data, setData] = useState([])
  // searchedData used to hold temporary filtered data based on user search text input feature
  const [searchedData, setSearchedData] = useState([])
  const [shownInstructionData, setShownInstructionData] = useState(null)
  const [shownOutputData, setShownOutputData] = useState(null)
  const [isTextSearching, setIsTextSearching] = useState(false)

  const value = {
    data,
    setData,
    searchedData,
    setSearchedData,
    shownInstructionData,
    setShownInstructionData,
    shownOutputData,
    setShownOutputData,
    isTextSearching,
    setIsTextSearching,
  }

  return (
    <chartDataContext.Provider value={value}>
      {children}
    </chartDataContext.Provider>
  )
}

export function useChartData() {
  const value = useContext(chartDataContext)

  return value
}
