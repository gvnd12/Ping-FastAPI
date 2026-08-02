import { motion } from "motion/react";
import { Link } from "react-router-dom";

export const fieldStagger = {
  hidden: {},
  show: {
    transition: { staggerChildren: 0.06, delayChildren: 0.05 },
  },
};

export const fieldItem = {
  hidden: { opacity: 0, y: 12 },
  show: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 320, damping: 26 } },
};

export default function AuthShell({ subtitle, footer, children }) {
  return (
    <div className="flex min-h-screen items-center justify-center px-4 py-10">
      <motion.div
        initial={{ opacity: 0, y: 24, scale: 0.98 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ type: "spring", stiffness: 220, damping: 26 }}
        className="glass w-full max-w-md rounded-3xl p-8 shadow-2xl shadow-black/40"
      >
        <div className="mb-8 text-center">
          <motion.div
            className="text-4xl font-black tracking-tight"
          >
            Ping
          </motion.div>
          <div className="mb-6 text-left">
            {subtitle && <p className="mt-1 text-sm text-slate-200">{subtitle}</p>}
          </div>
        </div>
        {children}
        {footer && <div className="mt-6 text-center text-sm text-slate-400">{footer}</div>}
      </motion.div>
    </div>
  );
}

export function AuthLink({ to, children }) {
  return (
    <Link to={to} className="font-semibold text-brand-2 hover:text-brand">
      {children}
    </Link>
  );
}
