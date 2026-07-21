import { motion } from "motion/react";
import Spinner from "./Spinner.jsx";

const VARIANTS = {
  primary:
    "bg-[rgb(21,24,49)] text-white hover:bg-[rgb(28,32,64)]",
  ghost:
    "bg-white/5 text-slate-200 border border-white/10 hover:bg-white/10",
  danger:
    "bg-gradient-to-r from-rose-600 to-red-800 text-white",
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
      className={`inline-flex items-center justify-center gap-2 rounded-xl px-3.5 py-3.5 text-sm font-semibold transition-colors disabled:cursor-not-allowed disabled:opacity-60 ${VARIANTS[variant]} ${className}`}
      {...props}
    >
      {loading && <Spinner size={16} />}
      {children}
    </motion.button>
  );
}
