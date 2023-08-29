import { createContext, useContext, useEffect, useState } from "react";

const chartDataContext = createContext({});

export function ChartDataProvider({ children }) {
  const [data, setData] = useState([])
  const [shownInstructionData, setShownInstructionData] = useState(null)
  const [shownOutputData, setShownOutputData] = useState(null)

  const value = {
    data,
    setData,
    shownInstructionData,
    setShownInstructionData,
    shownOutputData,
    setShownOutputData,
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
