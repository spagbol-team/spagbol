import { createContext, useContext, useState } from "react";

const settingsContext = createContext({});

export function SettingsProvider({ children }) {
  const [tracing, setTracing] = useState(true)
  // searchedData used to hold temporary filtered data based on user search text input feature

  const value = {
    tracing,
    setTracing,
  }

  return (
    <settingsContext.Provider value={value}>
      {children}
    </settingsContext.Provider>
  )
}

export function useSettings() {
  const value = useContext(settingsContext)

  return value
}
