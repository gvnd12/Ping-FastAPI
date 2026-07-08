import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "motion/react";
import AuthShell, { AuthLink, fieldItem, fieldStagger } from "../components/AuthShell.jsx";
import Input from "../components/ui/Input.jsx";
import Button from "../components/ui/Button.jsx";
import { useToast } from "../components/ui/Toast.jsx";
import { userApi } from "../api/endpoints.js";
import { extractError } from "../api/client.js";

const EMPTY = {
  name: "",
  email: "",
  username: "",
  password: "",
  mobile_no: "",
  date_of_birth: "",
  gender: "male",
  account_privacy: "public",
};

export default function SignupPage() {
  const [form, setForm] = useState(EMPTY);
  const [loading, setLoading] = useState(false);
  const toast = useToast();
  const navigate = useNavigate();

  const update = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await userApi.signup({ ...form, username: form.username.trim().toLowerCase() });
      toast.success("Account created! Please sign in.");
      navigate("/login", { replace: true });
    } catch (err) {
      toast.error(extractError(err, "Could not create account."));
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthShell
      title="Create your account"
      subtitle="Join Ping in a minute"
      footer={<>Already have an account? <AuthLink to="/login">Sign in</AuthLink></>}
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
            label="Full name"
            placeholder="Jane Doe"
            value={form.name}
            onChange={update("name")}
            minLength={2}
            maxLength={50}
            required
          />
        </motion.div>
        <motion.div variants={fieldItem}>
          <Input
            label="Email"
            type="email"
            placeholder="jane@example.com"
            value={form.email}
            onChange={update("email")}
            required
          />
        </motion.div>
        <motion.div variants={fieldItem} className="grid grid-cols-2 gap-3">
          <Input
            label="Username"
            placeholder="janedoe"
            value={form.username}
            onChange={update("username")}
            pattern="[a-zA-Z0-9_.]+"
            minLength={3}
            maxLength={30}
            hint="Letters, numbers, _ and ."
            required
          />
          <Input
            label="Mobile no."
            placeholder="+15551234567"
            value={form.mobile_no}
            onChange={update("mobile_no")}
            pattern="\+?[0-9]{7,15}"
            required
          />
        </motion.div>
        <motion.div variants={fieldItem}>
          <Input
            label="Password"
            type="password"
            placeholder="At least 8 chars"
            value={form.password}
            onChange={update("password")}
            minLength={8}
            hint="8+ chars with upper, lower and a digit"
            required
          />
        </motion.div>
        <motion.div variants={fieldItem} className="grid grid-cols-2 gap-3">
          <Input
            label="Date of birth"
            type="date"
            value={form.date_of_birth}
            onChange={update("date_of_birth")}
            required
          />
          <Input
            as="select"
            label="Gender"
            value={form.gender}
            onChange={update("gender")}
          >
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </Input>
        </motion.div>
        <motion.div variants={fieldItem}>
          <Input
            as="select"
            label="Account privacy"
            value={form.account_privacy}
            onChange={update("account_privacy")}
          >
            <option value="public">Public</option>
            <option value="private">Private</option>
          </Input>
        </motion.div>
        <motion.div variants={fieldItem}>
          <Button type="submit" loading={loading} className="mt-2 w-full">
            Create account
          </Button>
        </motion.div>
      </motion.form>
    </AuthShell>
  );
}
