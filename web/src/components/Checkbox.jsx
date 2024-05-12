export function Checkbox({ onChange, checked, label, id }) {
  return (
    <div className="bg-secondary-bg-color items-center text-sm p-2 border-slate-600 hover:border-gray-400 border rounded-lg min-w-[9rem] ml-4">
      <label htmlFor={id ?? "disableTracing"} className="flex items-center">
        <input
          id={id ?? "disableTracing"}
          type="checkbox"
          className="mr-2"
          onChange={onChange}
          checked={checked}
        />
        {label}
      </label>
    </div>
  );
}

