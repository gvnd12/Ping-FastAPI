import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "motion/react";
import AuthShell, { AuthLink, fieldItem, fieldStagger } from "../components/AuthShell.jsx";
import Input from "../components/ui/Input.jsx";
import Button from "../components/ui/Button.jsx";
import { useAuth } from "../context/AuthContext.jsx";
import { useToast } from "../components/ui/Toast.jsx";
import { authApi } from "../api/endpoints.js";
import { extractError } from "../api/client.js";
import { getUserType } from "../utils/jwt.js";

export default function LoginPage() {
  const [form, setForm] = useState({ username: "", password: "" });
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const toast = useToast();
  const navigate = useNavigate();

  const update = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const { data } = await authApi.login(form.username.trim(), form.password);
      const token = data.access_token;
      login(token);
      toast.success("Welcome back!");
      navigate(getUserType(token) === "ADMIN" ? "/admin/users" : "/app/profile", {
        replace: true,
      });
    } catch (err) {
      toast.error(extractError(err, "Invalid credentials!"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthShell
      subtitle="Sign In"
      footer={<>New to Ping? <AuthLink to="/signup">Create an account</AuthLink></>}
    >
      <motion.form
        variants={fieldStagger}
        initial="hidden"
        animate="show"
        onSubmit={handleSubmit}
        className="flex flex-col gap-4"
      >
        <motion.div variants={fieldItem}>
          <Input
            label="Username"
            placeholder="username"
            autoComplete="username"
            value={form.username}
            onChange={update("username")}
            required
          />
        </motion.div>
        <motion.div variants={fieldItem}>
          <Input
            label="Password"
            type="password"
            placeholder="********"
            autoComplete="current-password"
            value={form.password}
            onChange={update("password")}
            required
          />
        </motion.div>
        <motion.div variants={fieldItem}>
          <Button type="submit" loading={loading} className="mt-2 w-full">
            Sign in
          </Button>
        </motion.div>
      </motion.form>
    </AuthShell>
  );
}
