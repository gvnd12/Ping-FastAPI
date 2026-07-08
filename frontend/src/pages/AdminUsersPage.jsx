import { useCallback, useEffect, useState } from "react";
import { AnimatePresence, motion } from "motion/react";
import PageTransition from "../components/PageTransition.jsx";
import PageHeader from "../components/PageHeader.jsx";
import Card from "../components/ui/Card.jsx";
import Button from "../components/ui/Button.jsx";
import Spinner from "../components/ui/Spinner.jsx";
import { useToast } from "../components/ui/Toast.jsx";
import { adminApi } from "../api/endpoints.js";
import { extractError } from "../api/client.js";

function StatusBadge({ ok, yes, no }) {
  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-[11px] font-medium ${
        ok
          ? "bg-emerald-500/15 text-emerald-200"
          : "bg-rose-500/15 text-rose-200"
      }`}
    >
      <span className={`h-1.5 w-1.5 rounded-full ${ok ? "bg-emerald-400" : "bg-rose-400"}`} />
      {ok ? yes : no}
    </span>
  );
}

export default function AdminUsersPage() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [pendingId, setPendingId] = useState(null);
  const toast = useToast();

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await adminApi.listUsers();
      setUsers(Array.isArray(data) ? data : []);
    } catch (err) {
      toast.error(extractError(err, "Could not load users."));
    } finally {
      setLoading(false);
    }
  }, [toast]);

  useEffect(() => {
    load();
  }, [load]);

  const handleUndelete = async (userId) => {
    setPendingId(userId);
    try {
      const { data } = await adminApi.undelete(userId);
      toast.success(data?.message || "User restored.");
      setUsers((prev) =>
        prev.map((u) => (u._id === userId ? { ...u, is_deleted: false } : u)),
      );
    } catch (err) {
      toast.error(extractError(err, "Could not restore user."));
    } finally {
      setPendingId(null);
    }
  };

  const term = search.trim().toLowerCase();
  const filtered = term
    ? users.filter(
        (u) =>
          u.username?.toLowerCase().includes(term) ||
          u.name?.toLowerCase().includes(term) ||
          u.email?.toLowerCase().includes(term),
      )
    : users;

  return (
    <PageTransition>
      <PageHeader
        title="Users"
        description="All registered users. Restore soft-deleted accounts with Undelete."
      />

      <div className="mb-4 flex items-center gap-3">
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search by name, username or email"
          className="w-full max-w-sm rounded-xl border border-white/10 bg-white/5 px-3.5 py-2.5 text-sm text-slate-100 placeholder:text-slate-500 outline-none transition focus:border-brand/60 focus:ring-2 focus:ring-brand/30"
        />
        <Button variant="ghost" onClick={load} loading={loading}>
          Refresh
        </Button>
        <span className="ml-auto text-sm text-slate-500">{filtered.length} shown</span>
      </div>

      <Card className="overflow-hidden p-0">
        {loading ? (
          <div className="flex items-center justify-center gap-3 py-16 text-slate-400">
            <Spinner /> Loading users...
          </div>
        ) : filtered.length === 0 ? (
          <div className="py-16 text-center text-slate-500">No users found.</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="border-b border-white/10 text-xs uppercase tracking-wider text-slate-400">
                <tr>
                  <th className="px-5 py-3 font-medium">User</th>
                  <th className="px-5 py-3 font-medium">Contact</th>
                  <th className="px-5 py-3 font-medium">Privacy</th>
                  <th className="px-5 py-3 font-medium">Status</th>
                  <th className="px-5 py-3 font-medium">Action</th>
                </tr>
              </thead>
              <tbody>
                <AnimatePresence initial={false}>
                  {filtered.map((u, i) => (
                    <motion.tr
                      key={u._id ?? u.username ?? i}
                      layout
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0 }}
                      transition={{ delay: Math.min(i * 0.03, 0.3) }}
                      className="border-b border-white/5 last:border-0 hover:bg-white/5"
                    >
                      <td className="px-5 py-3">
                        <div className="font-medium text-slate-100">{u.name}</div>
                        <div className="text-xs text-slate-500">@{u.username}</div>
                      </td>
                      <td className="px-5 py-3">
                        <div className="text-slate-300">{u.email}</div>
                        <div className="text-xs text-slate-500">{u.mobile_no}</div>
                      </td>
                      <td className="px-5 py-3 capitalize text-slate-300">
                        {u.account_privacy}
                      </td>
                      <td className="px-5 py-3">
                        <div className="flex flex-col gap-1">
                          <StatusBadge ok={u.is_active} yes="Active" no="Inactive" />
                          {u.is_deleted && (
                            <StatusBadge ok={false} yes="" no="Deleted" />
                          )}
                        </div>
                      </td>
                      <td className="px-5 py-3">
                        {u.is_deleted ? (
                          <Button
                            variant="ghost"
                            loading={pendingId === u._id}
                            onClick={() => handleUndelete(u._id)}
                            className="px-3 py-1.5"
                          >
                            Undelete
                          </Button>
                        ) : (
                          <span className="text-xs text-slate-600">-</span>
                        )}
                      </td>
                    </motion.tr>
                  ))}
                </AnimatePresence>
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </PageTransition>
  );
}
