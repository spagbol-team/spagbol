import clsx from "clsx";

export default function Button({children, leftIcon, className, ...props}) {
  return (
    <button
      className={clsx("flex items-center justify-center w-1/2 px-3 py-2 text-sm capitalize transition-colors duration-200 border rounded-lg sm:w-auto gap-x-2 bg-gray-900 text-gray-200 border-gray-700 hover:bg-gray-800", className)}
      {...props}
    >
      {!!leftIcon ? leftIcon : <></>}
      {children}
    </button>
  )
}