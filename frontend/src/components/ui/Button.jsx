import { motion } from "motion/react";
import Spinner from "./Spinner.jsx";

const VARIANTS = {
  primary:
    "bg-gradient-to-r from-brand to-brand-2 text-white shadow-lg shadow-brand/25 hover:shadow-brand/40",
  ghost:
    "bg-white/5 text-slate-200 border border-white/10 hover:bg-white/10",
  danger:
    "bg-gradient-to-r from-rose-500 to-red-500 text-white shadow-lg shadow-rose-500/25",
};

export default function Button({
  children,
  variant = "primary",
  loading = false,
  disabled = false,
  className = "",
  type = "button",
  ...props
}) {
  const isDisabled = disabled || loading;
  return (
    <motion.button
      type={type}
      whileHover={isDisabled ? undefined : { scale: 1.02 }}
      whileTap={isDisabled ? undefined : { scale: 0.97 }}
      transition={{ type: "spring", stiffness: 400, damping: 22 }}
      disabled={isDisabled}
      className={`inline-flex items-center justify-center gap-2 rounded-xl px-4 py-2.5 text-sm font-semibold transition-colors disabled:cursor-not-allowed disabled:opacity-60 ${VARIANTS[variant]} ${className}`}
      {...props}
    >
      {loading && <Spinner size={16} />}
      {children}
    </motion.button>
  );
}
