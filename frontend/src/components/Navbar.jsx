import { NavLink, useNavigate } from "react-router-dom";
import { motion } from "motion/react";
import { useAuth } from "../context/AuthContext.jsx";
import { useToast } from "./ui/Toast.jsx";
import Button from "./ui/Button.jsx";

const USER_LINKS = [
  { to: "/app/create", label: "Create" },
  { to: "/app/profile", label: "Profile" },
  { to: "/app/settings", label: "Settings" },
];

const ADMIN_LINKS = [{ to: "/admin/users", label: "Users" }];

export default function Navbar() {
  const { isAdmin, username, logout } = useAuth();
  const toast = useToast();
  const navigate = useNavigate();
  const links = isAdmin ? ADMIN_LINKS : USER_LINKS;

  const handleLogout = async () => {
    await logout();
    toast.info("Signed out");
    navigate("/login", { replace: true });
  };

  return (
    <header className="sticky top-0 z-40 border-b border-white/10 bg-ink/60 backdrop-blur-xl">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-3">
        <div className="flex items-center gap-2">
          <motion.div
            initial={{ rotate: -12, scale: 0.8 }}
            animate={{ rotate: 0, scale: 1 }}
            transition={{ type: "spring", stiffness: 300, damping: 18 }}
            className="grid h-9 w-9 place-items-center rounded-xl bg-gradient-to-br from-brand to-accent text-lg font-black text-white"
          >
            P
          </motion.div>
          <span className="text-lg font-bold tracking-tight">Ping</span>
          {isAdmin && (
            <span className="ml-1 rounded-md bg-brand/20 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider text-brand-2">
              Admin
            </span>
          )}
        </div>

        <nav className="hidden items-center gap-1 sm:flex">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `relative rounded-lg px-3 py-1.5 text-sm font-medium transition-colors ${
                  isActive ? "text-white" : "text-slate-400 hover:text-slate-200"
                }`
              }
            >
              {({ isActive }) => (
                <>
                  {link.label}
                  {isActive && (
                    <motion.span
                      layoutId="nav-underline"
                      className="absolute inset-x-2 -bottom-0.5 h-0.5 rounded-full bg-gradient-to-r from-brand to-accent"
                    />
                  )}
                </>
              )}
            </NavLink>
          ))}
        </nav>

        <div className="flex items-center gap-3">
          {username && (
            <span className="hidden text-sm text-slate-400 sm:inline">
              @{username}
            </span>
          )}
          <Button variant="ghost" onClick={handleLogout} className="px-3 py-1.5">
            Logout
          </Button>
        </div>
      </div>
    </header>
  );
}
