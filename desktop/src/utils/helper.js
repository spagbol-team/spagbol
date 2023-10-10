/**
 * Converts a string of tailwind classes into an object representation.
 *
 * @param {string} className - The string of tailwind classes.
 * @return {Object} - The object representation of the tailwind classes.
 */
export function classNameToObj(className) {
  const tailwindClasses = className.split(' ');
  const classObj = {};
  tailwindClasses.forEach((twc) => {
    const style = twc.split('-')[0];
    classObj[style] = twc;
  });
  return classObj;
}

/**
 * Merges a base tailwind class with additional tailwind classes.
 *
 * @param {string} baseClass - The base tailwind class.
 * @param {string} additionClass - The additional tailwind classes.
 * @return {string} - The merged tailwind classes.
 */
export function mergeTailwindClass(baseClass, additionClass) {
  const classNames = additionClass.split(' ');
  const classObj = classNameToObj(baseClass);
  classNames.forEach((cn) => {
    const style = cn.split('-')[0];
    classObj[style] = cn;
  });
  return Object.values(classObj).join(' ');
}
