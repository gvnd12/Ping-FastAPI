import { createContext, useCallback, useContext, useMemo, useRef, useState } from "react";
import { AnimatePresence, motion } from "motion/react";

const ToastContext = createContext(null);

const TOAST_DURATION_MS = 1000;

const TONE_STYLES = {
  success: "border-emerald-400/30 bg-emerald-500/15 text-emerald-100",
  error: "border-rose-400/30 bg-rose-500/15 text-rose-100",
  info: "border-sky-400/30 bg-sky-500/15 text-sky-100",
};

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);
  const idRef = useRef(0);

  const dismiss = useCallback((id) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const push = useCallback(
    (message, tone = "info") => {
      const id = ++idRef.current;
      setToasts((prev) => [...prev, { id, message, tone }]);
      setTimeout(() => dismiss(id), TOAST_DURATION_MS);
    },
    [dismiss],
  );

  const value = useMemo(
    () => ({
      toast: push,
      success: (m) => push(m, "success"),
      error: (m) => push(m, "error"),
      info: (m) => push(m, "info"),
    }),
    [push],
  );

  return (
    <ToastContext.Provider value={value}>
      {children}
      <div className="pointer-events-none fixed inset-x-0 bottom-6 z-50 flex flex-col-reverse items-center gap-2 px-4">
        <AnimatePresence>
          {toasts.map((t) => (
            <motion.div
              key={t.id}
              layout
              initial={{ opacity: 0, y: 24, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -24, scale: 0.95 }}
              transition={{ type: "keyframes", stiffness: 500, damping: 32 }}
              onClick={() => dismiss(t.id)}
              className={`pointer-events-auto w-full max-w-sm cursor-pointer rounded-xl border px-4 py-3 text-sm font-medium shadow-lg backdrop-blur text-center ${
                TONE_STYLES[t.tone] ?? TONE_STYLES.info
              }`}
            >
              {t.message}
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error("useToast must be used within a ToastProvider");
  return ctx;
}
