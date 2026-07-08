import { motion } from "motion/react";

export default function PageHeader({ title, description }) {
  return (
    <div className="mb-6">
      <motion.h1
        initial={{ opacity: 0, x: -12 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ type: "spring", stiffness: 280, damping: 26 }}
        className="text-2xl font-bold tracking-tight"
      >
        {title}
      </motion.h1>
      {description && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.08 }}
          className="mt-1 max-w-2xl text-sm text-slate-400"
        >
          {description}
        </motion.p>
      )}
    </div>
  );
}
