/*
 * Copyright 2023 Spaghetti team
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */

import React, {useRef} from 'react';
import {CloseIcon} from './SVGIcons';
import {mergeTailwindClass} from '@/utils/helper';

/**
 * SearchInput component for searching instructions, input, or output text.
 *
 * @component
 * @param {Function} onFind - Callback function for handling search.
 * @return {JSX.Element} SearchInput component.
 */
export function SearchInput({onFind}) {
  const inputRef = useRef();

  const debounce = (func, delay) => {
    let timeoutId;
    return function(...args) {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => {
        func(...args);
      }, delay);
    };
  };

  const handleInputChange = (event) => {
    const {value} = event.target;
    debounce(onFind, 800)(value);
  };

  const clearInput = () => {
    if (inputRef?.current) {
      inputRef.current.value = '';
      onFind('');
    }
  };

  return (
    <div className="flex items-center">
      <div className="relative w-96">
        <div
          className="flex absolute inset-y-0 left-0
        items-center pl-3 pointer-events-none"
        >
          <svg
            className="w-5 h-5 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            ></path>
          </svg>
        </div>
        <BaseInput
          forwardRef={inputRef}
          type="search"
          id="default-search"
          placeholder="Search instruction, input or output text..."
          className="pl-10"
          onChange={handleInputChange}
          required
        ></BaseInput>
        <button
          type="submit"
          className="text-white absolute right-1.5 bottom-1.5 focus:ring-2
          focus:outline-none focus:ring-blue-300 font-medium rounded-lg
          text-sm px-2 py-1"
          onClick={clearInput}
        >
          <CloseIcon />
        </button>
      </div>
    </div>
  );
}

/**
 * BaseInput component for rendering an input element.
 *
 * @component
 * @param {React.Ref} forwardRef - Reference to the input element.
 * @param {string} className - Additional CSS classes for the input element.
 * @param {Object} props - Additional props for the input element.
 * @return {JSX.Element} BaseInput component.
 */
export function BaseInput({forwardRef, className, ...props}) {
  let baseClass = `block py-2 px-4 w-full text-smrounded-lg border
    ring-blue-500 bg-gray-700 border-gray-600 placeholder-gray-400
    text-white focus:ring-blue-500 focus:border-blue-500`;
  if (className) {
    baseClass = mergeTailwindClass(baseClass, className);
  }

  return <input ref={forwardRef} className={baseClass} {...props}></input>;
}

/**
 * BaseTextInput component for rendering a textarea element.
 *
 * @component
 * @param {React.Ref} forwardRef - Reference to the textarea element.
 * @param {string} className - Additional CSS classes for the textarea element.
 * @param {Object} props - Additional props for the textarea element.
 * @return {JSX.Element} BaseTextInput component.
 */
export function BaseTextInput({forwardRef, className, ...props}) {
  let baseClass = `block py-2 px-4 w-full text-sm rounded-lg border
    ring-blue-500 bg-gray-700 border-gray-600 placeholder-gray-400
    text-white focus:ring-blue-500 focus:border-blue-500`;
  if (className) {
    baseClass = mergeTailwindClass(baseClass, className);
  }

  return (
    <textarea ref={forwardRef} className={baseClass} {...props}></textarea>
  );
}
