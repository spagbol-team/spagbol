import React, {createContext, useContext, useState} from 'react';

const settingsContext = createContext({});

/**
 * Provides settings context for the application.
 *
 * @component
 * @param {Object} props - The component props.
 * @param {ReactNode} props.children - The child components.
 * @return {ReactNode} The rendered component.
 */
export function SettingsProvider({children}) {
  const [tracing, setTracing] = useState(true);
  const [searchByFamiliarity, setSearchByFamiliarity] = useState(false);
  const [formModal, setFormModal] = useState();
  // searchedData used to hold temporary
  // filtered data based on user search text input feature

  const value = {
    tracing,
    setTracing,
    formModal,
    setFormModal,
    searchByFamiliarity,
    setSearchByFamiliarity,
  };

  return (
    <settingsContext.Provider value={value}>
      {children}
    </settingsContext.Provider>
  );
}

/**
 * Custom hook to access the settings context.
 *
 * @return {Object} The settings context value.
 */
export function useSettings() {
  const value = useContext(settingsContext);

  return value;
}
