import type { InputHTMLAttributes } from "react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export function Input({ label, error, id, className = "", ...props }: InputProps) {
  return (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label htmlFor={id} className="text-sm font-medium text-(--color-text-secondary)">
          {label}
        </label>
      )}
      <input id={id} className={`input-field ${className}`} {...props} />
      {error && <span className="text-sm text-(--color-danger)">{error}</span>}
    </div>
  );
}
