/*
 * Copyright 2023 Spaghetti team
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License. You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 */

import { useEffect, useState } from "react"

function THeader({ children }) {
  return (
    <th
      scope="col"
      title={children}
      className="px-4 py-2 text-sm font-normal text-left rtl:text-right overflow-hidden whitespace-nowrap overflow-ellipsis max-w-[120px]"
    >
      {children}
    </th>
  )
}

function TData({ children }) {
  return (
    <td className="px-6 py-2 text-xs font-medium text-left">
      {children}
    </td>
  )
}

function ShortIcon() {
  return (
    <svg className="h-3" viewBox="0 0 10 11" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M2.13347 0.0999756H2.98516L5.01902 4.79058H3.86226L3.45549 3.79907H1.63772L1.24366 4.79058H0.0996094L2.13347 0.0999756ZM2.54025 1.46012L1.96822 2.92196H3.11227L2.54025 1.46012Z" fill="currentColor" stroke="currentColor" stroke-width="0.1" />
      <path d="M0.722656 9.60832L3.09974 6.78633H0.811638V5.87109H4.35819V6.78633L2.01925 9.60832H4.43446V10.5617H0.722656V9.60832Z" fill="currentColor" stroke="currentColor" stroke-width="0.1" />
      <path d="M8.45558 7.25664V7.40664H8.60558H9.66065C9.72481 7.40664 9.74667 7.42274 9.75141 7.42691C9.75148 7.42808 9.75146 7.42993 9.75116 7.43262C9.75001 7.44265 9.74458 7.46304 9.72525 7.49314C9.72522 7.4932 9.72518 7.49326 9.72514 7.49332L7.86959 10.3529L7.86924 10.3534C7.83227 10.4109 7.79863 10.418 7.78568 10.418C7.77272 10.418 7.73908 10.4109 7.70211 10.3534L7.70177 10.3529L5.84621 7.49332C5.84617 7.49325 5.84612 7.49318 5.84608 7.49311C5.82677 7.46302 5.82135 7.44264 5.8202 7.43262C5.81989 7.42993 5.81987 7.42808 5.81994 7.42691C5.82469 7.42274 5.84655 7.40664 5.91071 7.40664H6.96578H7.11578V7.25664V0.633865C7.11578 0.42434 7.29014 0.249976 7.49967 0.249976H8.07169C8.28121 0.249976 8.45558 0.42434 8.45558 0.633865V7.25664Z" fill="currentColor" stroke="currentColor" stroke-width="0.3" />
    </svg>
  )
}

function TableButton({children, ...props}) {
  return (
    <button className="flex items-center justify-center w-1/2 px-3 py-2 text-sm capitalize transition-colors duration-200 border rounded-lg sm:w-auto gap-x-2 bg-gray-900 text-gray-200 border-gray-700 hover:bg-gray-800" {...props}>
      {children}
    </button>
  )
}

const SHOWN_DATA = 6

export function Tables({ title='Instructions', headers=[], dataKey=[], data=[] }) {
  const [page, setPage] = useState(1)
  const [partialData, setPartialData] = useState([])

  useEffect(() => {
    const start = (page-1)*SHOWN_DATA
    setPartialData([...data].slice(start, start+SHOWN_DATA))
  }, [data, page])
  
  return (
    <section className="container px-4 mx-auto text-white mb-8">
      <div className="sm:flex sm:items-center sm:justify-between flex-wrap">
        <div>
          <div className="flex items-center gap-x-3">
            <h2 className="text-lg font-medium text-white">{title}</h2>

            <span className="px-3 py-1 text-xs text-blue-600 bg-blue-100 rounded-full dark:bg-gray-800 dark:text-blue-400">{data.length} total data</span>
          </div>

          <p className="mt-1 text-sm text-gray-500 dark:text-gray-300">Clustered 2D Plot of {title} Embedding.</p>
        </div>

        <div className="flex items-center mt-4 gap-x-3">
          <button className="flex items-center justify-center w-1/2 px-3 py-1 text-sm text-gray-700 transition-colors duration-200 bg-white border rounded-lg gap-x-2 sm:w-auto hover:bg-gray-100">
            <svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-5 h-5">
              <g clip-path="url(#clip0_3098_154395)">
              <path d="M13.3333 13.3332L9.99997 9.9999M9.99997 9.9999L6.66663 13.3332M9.99997 9.9999V17.4999M16.9916 15.3249C17.8044 14.8818 18.4465 14.1806 18.8165 13.3321C19.1866 12.4835 19.2635 11.5359 19.0351 10.6388C18.8068 9.7417 18.2862 8.94616 17.5555 8.37778C16.8248 7.80939 15.9257 7.50052 15 7.4999H13.95C13.6977 6.52427 13.2276 5.61852 12.5749 4.85073C11.9222 4.08295 11.104 3.47311 10.1817 3.06708C9.25943 2.66104 8.25709 2.46937 7.25006 2.50647C6.24304 2.54358 5.25752 2.80849 4.36761 3.28129C3.47771 3.7541 2.70656 4.42249 2.11215 5.23622C1.51774 6.04996 1.11554 6.98785 0.935783 7.9794C0.756025 8.97095 0.803388 9.99035 1.07431 10.961C1.34523 11.9316 1.83267 12.8281 2.49997 13.5832" stroke="currentColor" stroke-width="1.67" stroke-linecap="round" stroke-linejoin="round"/>
              </g>
              <defs>
              <clipPath id="clip0_3098_154395">
              <rect width="20" height="20" fill="white"/>
              </clipPath>
              </defs>
            </svg>

            <span>Export</span>
          </button>

            <TableButton>
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" className="w-5 h-5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v6m3-3H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>

                <span>Add data</span>
            </TableButton>
        </div>
    </div>

    {/* <div className="mt-6 md:flex md:items-center md:justify-between">
        <div className="inline-flex overflow-hidden bg-white border divide-x rounded-lg dark:bg-gray-900 rtl:flex-row-reverse dark:border-gray-700 dark:divide-gray-700">
            <button className="px-5 py-2 text-xs font-medium text-gray-600 transition-colors duration-200 bg-gray-100 sm:text-sm dark:bg-gray-800 dark:text-gray-300">
                View all
            </button>
        </div>
    </div> */}

    <div className="flex flex-col mt-6">
      <div className="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div className="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
              <div className="overflow-hidden border border-gray-700 md:rounded-lg">
                  <table className="min-w-full divide-y divide-gray-700">
                      <thead className="bg-gray-900">
                          <tr>
                            {
                              headers.map(hd => (
                                <THeader key={hd}>
                                  {hd}
                                </THeader>
                              ))
                            }
                          </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-700 bg-gray-800">
                        {
                          partialData.map((dt,idx) => (
                            <tr key={idx}>
                              {dataKey.map((dk,jdx) => (
                                <TData key={`${idx}-${jdx}`}>
                                  <p className="overflow-hidden whitespace-nowrap overflow-ellipsis max-w-[120px]" title={dt[dk]}>
                                    {dt[dk] || '-'}
                                  </p>
                                </TData>
                              ))}
                              {/* <TData>
                                <button className="px-1 py-1 text-gray-100 transition-colors duration-200 rounded-lg bg-gray-600">
                                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" className="w-6 h-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z" />
                                  </svg>
                                </button>
                              </TData> */}
                            </tr>
                          ))
                        }
                      </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <div className="mt-6 sm:flex sm:items-center sm:justify-between ">
        <div className="text-sm text-gray-500 dark:text-gray-400">
            Page <span className="font-medium text-gray-300">{page} of {Math.round(data.length/SHOWN_DATA)}</span> 
        </div>

        <div className="flex items-center mt-4 gap-x-4 sm:mt-0">
            <button
              onClick={() => setPage(Math.max(0, page-1))}
              className="flex items-center justify-center w-1/2 px-5 py-2 text-sm capitalize transition-colors duration-200 border rounded-md sm:w-auto gap-x-2 bg-gray-900 text-gray-200 border-gray-700 hover:bg-gray-800 disabled:bg-gray-400"
              disabled={page <= 1}
            >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" className="w-5 h-5 rtl:-scale-x-100">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 15.75L3 12m0 0l3.75-3.75M3 12h18" />
                </svg>

                <span>
                    previous
                </span>
            </button>

            <button
              onClick={() => {
                setPage(
                  Math.min(
                    Math.round(data.length/SHOWN_DATA),
                    page+1
                  )
                )
              }}
              className="flex items-center justify-center w-1/2 px-5 py-2 text-sm capitalize transition-colors duration-200 border rounded-md sm:w-auto gap-x-2 bg-gray-900 text-gray-200 border-gray-700 hover:bg-gray-800 disabled:bg-gray-4 00"
              disabled={page >= Math.round(data.length/SHOWN_DATA)}
            >
                <span>
                    Next
                </span>

                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" className="w-5 h-5 rtl:-scale-x-100">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 8.25L21 12m0 0l-3.75 3.75M21 12H3" />
                </svg>
            </button>
        </div>
    </div>
    </section>
  )
}