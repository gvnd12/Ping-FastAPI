import { forwardRef, useId } from "react";

const Input = forwardRef(function Input(
  { label, hint, error, className = "", as = "input", children, ...props },
  ref,
) {
  const id = useId();
  const Field = as;
  return (
    <div className="flex w-full flex-col gap-1.5">
      {label && (
        <label htmlFor={id} className="text-xs font-medium text-slate-300">
          {label}
        </label>
      )}
      <Field
        id={id}
        ref={ref}
        className={`w-full resize-none rounded-xl bg-white/5 px-3.5 py-3.5 text-sm text-slate-100 placeholder:text-slate-500 outline-none transition focus:border-brand/60 focus:ring-1 focus:ring-brand/20 ${className}`}
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
