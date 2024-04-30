/**
 * Extracts form values from the event target elements
 * @param {Event} event - The event object
 * @returns {Object} - Form values extracted from the event target elements
 */
export const extractFormValues = (event) => {
  const elements = event.target.elements;
  const formValues = {};
  for (let key in elements) {
    formValues[key] = elements[key].value;
  }
  return formValues;
};