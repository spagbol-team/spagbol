
/**
 * Function to save data to localStorage
 * @param {string} key - The key under which to save the data
 * @param {any} data - The data to be saved
 */
export const saveToLocalStorage = (key, data) => {
  localStorage.setItem(key, JSON.stringify(data));
}

/**
 * Function to get data from localStorage
 * @param {string} key - The key under which the data is saved
 * @returns {any} The retrieved data
 */
export const getFromLocalStorage = (key) => {
  const data = localStorage.getItem(key);
  return data ? JSON.parse(data) : null;
}

/**
 * Function to delete data from localStorage
 * @param {string} key - The key of the data to be deleted
 */
export const deleteFromLocalStorage = (key) => {
  localStorage.removeItem(key);
}

