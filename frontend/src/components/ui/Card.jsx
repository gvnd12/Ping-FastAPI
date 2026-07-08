import { motion } from "motion/react";

export default function Card({ children, className = "", ...props }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ type: "spring", stiffness: 260, damping: 28 }}
      className={`glass rounded-2xl p-6 shadow-xl shadow-black/20 ${className}`}
      {...props}
    >
      {children}
    </motion.div>
  );
}
