import type { SelectHTMLAttributes } from 'react';

interface SelectProps extends SelectHTMLAttributes<HTMLSelectElement> {
  label: string;
  error?: string;
  options: { value: string; label: string }[];
}

export function Select({ label, error, options, id, className = '', ...props }: SelectProps) {
  const inputId = id || props.name;
  return (
    <div className="flex flex-col gap-1">
      <label htmlFor={inputId} className="text-sm font-medium text-gray-700">
        {label}
        {props.required && <span className="text-red-500"> *</span>}
      </label>
      <select
        id={inputId}
        className={`rounded-lg border bg-white px-3 py-2 text-sm outline-none transition focus:ring-2 focus:ring-primary-200 ${
          error ? 'border-red-400' : 'border-gray-300 focus:border-primary-500'
        } ${className}`}
        {...props}
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
      {error && <p className="text-xs text-red-600">{error}</p>}
    </div>
  );
}
