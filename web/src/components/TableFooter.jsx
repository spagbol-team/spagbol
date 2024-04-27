export default function TableFooter({
  page,
  totalData,
  dataShown,
  onClickPrevious,
  onClickNext
}) {
  return (
    <div className="mt-6 sm:flex sm:items-center sm:justify-between ">
      <div className="text-sm text-gray-500 dark:text-gray-400">
        Page <span className="font-medium text-gray-300">{page} of {Math.round(totalData/dataShown)}</span> 
      </div>

      <div className="flex items-center mt-4 gap-x-4 sm:mt-0">
        <button
          onClick={onClickPrevious}
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
          onClick={onClickNext}
          className="flex items-center justify-center w-1/2 px-5 py-2 text-sm capitalize transition-colors duration-200 border rounded-md sm:w-auto gap-x-2 bg-gray-900 text-gray-200 border-gray-700 hover:bg-gray-800 disabled:bg-gray-4 00"
          disabled={page >= Math.round(totalData/dataShown)}
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
  );
}