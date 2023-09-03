import { createContext, useContext, useEffect, useState } from "react";

const chartDataContext = createContext({});

export function ChartDataProvider({ children }) {
  const [data, setData] = useState([])
  const [shownInstructionData, setShownInstructionData] = useState(null)
  const [shownOutputData, setShownOutputData] = useState(null)
  const [isTextSearching, setIsTextSearching] = useState(false)

  const value = {
    data,
    setData,
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
