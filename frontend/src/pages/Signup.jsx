import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";

import FormField from "../components/FormField";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";
import { signup } from "../services/auth";
import { getErrorMessage } from "../services/api";

export default function Signup() {
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
      await signup(values);
      // Log the new user straight in so they land on their projects.
      await login({ email: values.email, password: values.password });
      showToast("Welcome to IssueHub!");
      navigate("/projects");
    } catch (error) {
      showToast(getErrorMessage(error), "error");
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h1>Create your account</h1>
        <form onSubmit={handleSubmit(onSubmit)}>
          <FormField label="Name" error={errors.name?.message}>
            <input {...register("name", { required: "Name is required" })} />
          </FormField>
          <FormField label="Email" error={errors.email?.message}>
            <input
              type="email"
              {...register("email", { required: "Email is required" })}
            />
          </FormField>
          <FormField label="Password" error={errors.password?.message}>
            <input
              type="password"
              {...register("password", {
                required: "Password is required",
                minLength: { value: 8, message: "At least 8 characters" },
              })}
            />
          </FormField>
          <button type="submit" className="btn btn-primary btn-block" disabled={isSubmitting}>
            {isSubmitting ? "Creating..." : "Sign Up"}
          </button>
        </form>
        <p className="auth-switch">
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </div>
    </div>
  );
}
