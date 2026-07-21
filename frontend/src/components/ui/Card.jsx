import { motion } from "motion/react";

export default function Card({ children, className = "", ...props }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ type: "spring", stiffness: 260, damping: 28 }}
      className={`p-6 ${className}`}
      {...props}
    >
      {children}
    </motion.div>
  );
}
