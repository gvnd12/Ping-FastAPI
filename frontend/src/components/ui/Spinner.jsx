import { motion } from "motion/react";

export default function Spinner({ size = 20 }) {
  return (
    <motion.span
      style={{ width: size, height: size }}
      className="inline-block rounded-full border-2 border-white/30 border-t-white"
      animate={{ rotate: 360 }}
      transition={{ repeat: Infinity, ease: "linear", duration: 0.8 }}
    />
  );
}
