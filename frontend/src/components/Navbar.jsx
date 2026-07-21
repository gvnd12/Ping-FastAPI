import { NavLink, useNavigate } from "react-router-dom";
import { motion } from "motion/react";
import { LogOut, ImagePlusIcon } from "lucide-react";
import { useAuth } from "../context/AuthContext.jsx";
import { useToast } from "./ui/Toast.jsx";
import Button from "./ui/Button.jsx";

const USER_LINKS = [
  { to: "/app/create", label: <ImagePlusIcon size={15}></ImagePlusIcon> },
  { to: "/app/settings", label: "Settings" },
];

const ADMIN_LINKS = [{ to: "/admin/users", label: "Users" }];

export default function Navbar() {
  const { isAdmin, username, logout } = useAuth();
  const toast = useToast();
  const navigate = useNavigate();
  const links = isAdmin ? ADMIN_LINKS : USER_LINKS;
  const profilePath = isAdmin ? "/admin/users" : "/app/profile";

  const handleLogout = async () => {
    await logout();
    toast.info("Signed out");
    navigate("/login", { replace: true });
  };

  return (
    <aside className="sticky top-0 flex h-screen w-56 shrink-0 flex-col border-r border-white/10 bg-ink/60 backdrop-blur-xl">
      <div className="flex flex-col gap-6 p-4">
        <div className="flex items-center gap-2 px-2">
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
            <span className="rounded-md bg-brand/20 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider text-brand-2">
              Admin
            </span>
          )}
        </div>

        <nav className="flex flex-col gap-1">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `relative rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-white/10 text-white"
                    : "text-slate-400 hover:bg-white/5 hover:text-slate-200"
                }`
              }
            >
              {({ isActive }) => (
                <>
                  {link.label}
                  {isActive && (
                    <motion.span
                      layoutId="nav-indicator"
                      className="absolute inset-y-1 left-0 w-0.5 rounded-full bg-gradient-to-b from-brand to-accent"
                    />
                  )}
                </>
              )}
            </NavLink>
          ))}
        </nav>
      </div>

      <div className="mt-auto flex flex-col gap-3 border-t border-white/10 p-4">
        {username && (
          <NavLink
            to={profilePath}
            className={({ isActive }) =>
              `rounded-lg px-3 py-2 text-sm transition-colors ${
                isActive
                  ? "bg-white/10 font-medium text-white"
                  : "text-slate-400 hover:bg-white/5 hover:text-slate-200"
              }`
            }
          >
            {username}
          </NavLink>
        )}
        <Button variant="primary" onClick={handleLogout} className="w-full px-3 py-2">
          <LogOut size={18} />
          Logout
        </Button>
      </div>
    </aside>
  );
}
