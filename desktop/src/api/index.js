import jsonDataUrl from '/subset_data.json?url';

console.log('cek', jsonDataUrl)
/**
 * Fetches the first data.
 * @return {Promise<any>} The fetched data.
 */
export async function fetchFirstData() {
  // const data = jsonData;
  // const data = await fetch('/subset_data.json');
  const data = await fetch(jsonDataUrl);
  const json = await data.json();
  return json;
}


/**
 * Finds data by similarity.
 * @param {Array<any>} data - The data to search.
 * @param {string} textInput - The input text to search for.
 * @return {Array<any>} The filtered data.
 */
export async function findBySimiliarity(data, textInput) {
  const filtered = data.filter(
      (dt) =>
        dt.instruction.includes(textInput) ||
      dt.input.includes(textInput) ||
      dt.output.includes(textInput),
  );
  return filtered;
}

/**
 * Edits a data point.
 * @param {Array<any>} data - The original data.
 * @param {number} idx - The index of the data point to edit.
 * @param {object} form - The form data to update the data point with.
 * @return {Array<any>} The updated data.
 */
export async function editDataPoint(data, idx, form) {
  const newData = [...data];
  newData[idx] = {
    ...newData[idx],
    ...form,
  };
  return newData;
}

/**
 * Deletes data points.
 * @param {Array<number>} toBeRemoved
 * - The indices of the data points to remove.
 * @param {Array<any>} originalData - The original data.
 * @return {Array<any>} The updated data.
 */
export async function deleteDataPoints(toBeRemoved, originalData) {
  const newData = [...originalData];

  toBeRemoved.map((ipi) => {
    newData.splice(ipi, 1);
  });
  return newData;
}

/**
 * Fetches clustering data.
 * @param {Array<any>} data - The data to fetch clustering for.
 * @return {Array<any>} The clustering data.
 */
export async function fetchClustering(data) {
  return data;
}
