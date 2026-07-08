import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { AnimatePresence, motion } from "motion/react";
import PageTransition from "../components/PageTransition.jsx";
import PageHeader from "../components/PageHeader.jsx";
import Card from "../components/ui/Card.jsx";
import Input from "../components/ui/Input.jsx";
import Button from "../components/ui/Button.jsx";
import { useToast } from "../components/ui/Toast.jsx";
import { useAuth } from "../context/AuthContext.jsx";
import { userApi } from "../api/endpoints.js";
import { extractError } from "../api/client.js";

const TABS = [
  { id: "profile", label: "Edit profile" },
  { id: "password", label: "Change password" },
  { id: "danger", label: "Danger zone" },
];

function ProfileSummary({ user }) {
  if (!user) return null;
  return (
    <div className="mb-5 rounded-xl border border-white/10 bg-white/5 p-4">
      <div className="font-semibold text-slate-100">{user.name}</div>
      <div className="text-sm text-slate-400">@{user.username}</div>
      <div className="mt-3 flex gap-6 text-sm text-slate-400">
        <span>{user.posts_count ?? 0} posts</span>
        <span>{user.followers_count ?? 0} followers</span>
        <span>{user.following_count ?? 0} following</span>
      </div>
    </div>
  );
}

function EditProfile({ profileUser }) {
  const [form, setForm] = useState({
    name: profileUser?.name ?? "",
    email: "",
    mobile_no: "",
    account_privacy: "",
  });
  const [loading, setLoading] = useState(false);
  const toast = useToast();

  useEffect(() => {
    if (profileUser?.name) {
      setForm((f) => ({ ...f, name: profileUser.name }));
    }
  }, [profileUser?.name]);

  const update = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = Object.fromEntries(
      Object.entries(form).filter(([, v]) => v !== "" && v !== null),
    );
    if (Object.keys(payload).length === 0) {
      toast.info("Change at least one field to update.");
      return;
    }
    setLoading(true);
    try {
      const { data } = await userApi.edit(payload);
      toast.success(data?.message || "Profile updated!");
    } catch (err) {
      toast.error(extractError(err, "Could not update profile."));
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      <Input label="Name" placeholder="New name" value={form.name} onChange={update("name")} />
      <Input
        label="Email"
        type="email"
        placeholder="new@example.com"
        value={form.email}
        onChange={update("email")}
      />
      <Input
        label="Mobile no."
        placeholder="+15551234567"
        value={form.mobile_no}
        onChange={update("mobile_no")}
      />
      <Input
        as="select"
        label="Account privacy"
        value={form.account_privacy}
        onChange={update("account_privacy")}
      >
        <option value="">No change</option>
        <option value="public">Public</option>
        <option value="private">Private</option>
      </Input>
      <Button type="submit" loading={loading} className="w-full">
        Save changes
      </Button>
    </form>
  );
}

function ChangePassword() {
  const [form, setForm] = useState({
    old_password: "",
    new_password: "",
    confirm_password: "",
  });
  const [loading, setLoading] = useState(false);
  const toast = useToast();

  const update = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (form.new_password !== form.confirm_password) {
      toast.error("New passwords do not match.");
      return;
    }
    setLoading(true);
    try {
      const { data } = await userApi.changePassword(form);
      toast.success(data?.message || "Password changed!");
      setForm({ old_password: "", new_password: "", confirm_password: "" });
    } catch (err) {
      toast.error(extractError(err, "Could not change password."));
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      <Input
        label="Current password"
        type="password"
        value={form.old_password}
        onChange={update("old_password")}
        required
      />
      <Input
        label="New password"
        type="password"
        value={form.new_password}
        onChange={update("new_password")}
        minLength={8}
        hint="8+ chars with upper, lower and a digit"
        required
      />
      <Input
        label="Confirm new password"
        type="password"
        value={form.confirm_password}
        onChange={update("confirm_password")}
        required
      />
      <Button type="submit" loading={loading} className="w-full">
        Update password
      </Button>
    </form>
  );
}

function DangerZone() {
  const [deactivating, setDeactivating] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const toast = useToast();
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleDeactivate = async () => {
    if (!window.confirm("Deactivate your account? You can reactivate by logging in again.")) {
      return;
    }
    setDeactivating(true);
    try {
      const { data } = await userApi.deactivate();
      toast.success(data?.message || "Account deactivated.");
      await logout();
      navigate("/login", { replace: true });
    } catch (err) {
      toast.error(extractError(err, "Could not deactivate account."));
    } finally {
      setDeactivating(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm("Delete your account? This is a soft delete on the server.")) {
      return;
    }
    setDeleting(true);
    try {
      const { data } = await userApi.deleteAccount();
      toast.success(data?.message || "Account deleted.");
      await logout();
      navigate("/login", { replace: true });
    } catch (err) {
      toast.error(extractError(err, "Could not delete account."));
    } finally {
      setDeleting(false);
    }
  };

  return (
    <div className="flex flex-col gap-5">
      <div className="rounded-xl border border-amber-400/20 bg-amber-500/10 p-4">
        <h3 className="text-sm font-semibold text-amber-100">Deactivate account</h3>
        <p className="mt-1 text-xs text-amber-100/70">
          Temporarily disable your account. Logging in again reactivates it.
        </p>
        <Button
          variant="ghost"
          loading={deactivating}
          onClick={handleDeactivate}
          className="mt-3"
        >
          Deactivate
        </Button>
      </div>
      <div className="rounded-xl border border-rose-400/20 bg-rose-500/10 p-4">
        <h3 className="text-sm font-semibold text-rose-100">Delete account</h3>
        <p className="mt-1 text-xs text-rose-100/70">
          Remove your account from Ping. This performs a soft delete on the server.
        </p>
        <Button variant="danger" loading={deleting} onClick={handleDelete} className="mt-3">
          Delete my account
        </Button>
      </div>
    </div>
  );
}

export default function AccountSettingsPage() {
  const [tab, setTab] = useState("profile");
  const [profileUser, setProfileUser] = useState(null);
  const toast = useToast();

  useEffect(() => {
    userApi
      .getProfile()
      .then(({ data }) => setProfileUser(data.user ?? null))
      .catch((err) => toast.error(extractError(err, "Could not load profile.")));
  }, [toast]);

  return (
    <PageTransition>
      <PageHeader title="Account settings" description="Manage your Ping account." />
      <div className="mx-auto max-w-xl">
        <ProfileSummary user={profileUser} />
        <div className="mb-5 flex gap-1 rounded-xl bg-white/5 p-1">
          {TABS.map((t) => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={`relative flex-1 rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                tab === t.id ? "text-white" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {tab === t.id && (
                <motion.span
                  layoutId="settings-tab"
                  className="absolute inset-0 rounded-lg bg-gradient-to-r from-brand/80 to-brand-2/80"
                  transition={{ type: "spring", stiffness: 400, damping: 30 }}
                />
              )}
              <span className="relative z-10">{t.label}</span>
            </button>
          ))}
        </div>
        <Card>
          <AnimatePresence mode="wait">
            <motion.div
              key={tab}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
            >
              {tab === "profile" && <EditProfile profileUser={profileUser} />}
              {tab === "password" && <ChangePassword />}
              {tab === "danger" && <DangerZone />}
            </motion.div>
          </AnimatePresence>
        </Card>
      </div>
    </PageTransition>
  );
}
