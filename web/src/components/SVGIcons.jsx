import React from 'react';

/**
 * CloseIcon component.
 *
 * @param {object} props - The props object.
 * @return {JSX.Element} The CloseIcon component.
 */
export function CloseIcon(props) {
  return (
    <svg
      {...props}
      className="w-4 h-4 text-gray-400"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth="2"
        d="M6 18L18 6M6 6l12 12"
      ></path>
    </svg>
  );
}
