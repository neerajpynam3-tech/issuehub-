import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";

import FormField from "../components/FormField";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";
import { getErrorMessage } from "../services/api";

export default function Login() {
  const { login } = useAuth();
  const { showToast } = useToast();
  const navigate = useNavigate();
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm();

  async function onSubmit(values) {
    try {
      await login(values);
      navigate("/projects");
    } catch (error) {
      showToast(getErrorMessage(error), "error");
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h1>Sign in to IssueHub</h1>
        <form onSubmit={handleSubmit(onSubmit)}>
          <FormField label="Email" error={errors.email?.message}>
            <input
              type="email"
              {...register("email", { required: "Email is required" })}
            />
          </FormField>
          <FormField label="Password" error={errors.password?.message}>
            <input
              type="password"
              {...register("password", { required: "Password is required" })}
            />
          </FormField>
          <button type="submit" className="btn btn-primary btn-block" disabled={isSubmitting}>
            {isSubmitting ? "Signing in..." : "Sign In"}
          </button>
        </form>
        <p className="auth-switch">
          No account? <Link to="/signup">Sign up</Link>
        </p>
      </div>
    </div>
  );
}
