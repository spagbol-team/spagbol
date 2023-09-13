import React, {createContext, useContext, useState} from 'react';

const chartDataContext = createContext({});

/**
 * Everything related to chart and need to be shared accross apps
 *
 * @param {*} children
 * @return {*} chart data Provider
 */
export function ChartDataProvider({children}) {
  const [data, setData] = useState([]);
  // searchedData used to hold temporary
  // filtered data based on user search text input feature
  const [searchedData, setSearchedData] = useState([]);
  const [shownInstructionData, setShownInstructionData] = useState(null);
  const [shownOutputData, setShownOutputData] = useState(null);
  const [isTextSearching, setIsTextSearching] = useState(false);

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
  };

  return (
    <chartDataContext.Provider value={value}>
      {children}
    </chartDataContext.Provider>
  );
}

/**
 * use chart data context
 *
 * @return {*} chart data context
 */
export function useChartData() {
  const value = useContext(chartDataContext);

  return value;
}
