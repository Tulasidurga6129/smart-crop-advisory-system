import type { InputHTMLAttributes, TextareaHTMLAttributes } from 'react';

interface FormInputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  hint?: string;
}

export function FormInput({ label, error, hint, id, className = '', ...props }: FormInputProps) {
  const inputId = id || props.name;
  return (
    <div className="flex flex-col gap-1">
      <label htmlFor={inputId} className="text-sm font-medium text-gray-700">
        {label}
        {props.required && <span className="text-red-500"> *</span>}
      </label>
      <input
        id={inputId}
        className={`rounded-lg border px-3 py-2 text-sm outline-none transition focus:ring-2 focus:ring-primary-200 ${
          error ? 'border-red-400 focus:border-red-500' : 'border-gray-300 focus:border-primary-500'
        } ${className}`}
        {...props}
      />
      {hint && !error && <p className="text-xs text-gray-400">{hint}</p>}
      {error && <p className="text-xs text-red-600">{error}</p>}
    </div>
  );
}

interface FormTextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label: string;
  error?: string;
}

export function FormTextarea({ label, error, id, className = '', ...props }: FormTextareaProps) {
  const inputId = id || props.name;
  return (
    <div className="flex flex-col gap-1">
      <label htmlFor={inputId} className="text-sm font-medium text-gray-700">
        {label}
        {props.required && <span className="text-red-500"> *</span>}
      </label>
      <textarea
        id={inputId}
        rows={3}
        className={`rounded-lg border px-3 py-2 text-sm outline-none transition focus:ring-2 focus:ring-primary-200 ${
          error ? 'border-red-400 focus:border-red-500' : 'border-gray-300 focus:border-primary-500'
        } ${className}`}
        {...props}
      />
      {error && <p className="text-xs text-red-600">{error}</p>}
    </div>
  );
}
