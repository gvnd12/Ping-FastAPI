import { forwardRef, useId } from "react";

const Input = forwardRef(function Input(
  { label, hint, error, className = "", as = "input", children, ...props },
  ref,
) {
  const id = useId();
  const Field = as;
  return (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label htmlFor={id} className="text-xs font-medium text-slate-300">
          {label}
        </label>
      )}
      <Field
        id={id}
        ref={ref}
        className={`w-full rounded-xl border border-white/10 bg-white/5 px-3.5 py-2.5 text-sm text-slate-100 placeholder:text-slate-500 outline-none transition focus:border-brand/60 focus:ring-2 focus:ring-brand/30 ${className}`}
        {...props}
      >
        {children}
      </Field>
      {error ? (
        <span className="text-xs text-rose-300">{error}</span>
      ) : (
        hint && <span className="text-xs text-slate-500">{hint}</span>
      )}
    </div>
  );
});

export default Input;
