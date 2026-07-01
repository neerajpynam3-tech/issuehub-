import { useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

import FormField from "../components/FormField";
import Spinner from "../components/Spinner";
import { useProjects } from "../hooks/useProjects";
import { useToast } from "../context/ToastContext";
import { createProject } from "../services/projects";
import { getErrorMessage } from "../services/api";

export default function Projects() {
  const { projects, loading, reload } = useProjects();
  const { showToast } = useToast();
  const navigate = useNavigate();
  const [showForm, setShowForm] = useState(false);
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm();

  async function onCreate(values) {
    try {
      await createProject(values);
      showToast("Project created");
      reset();
      setShowForm(false);
      reload();
    } catch (error) {
      showToast(getErrorMessage(error), "error");
    }
  }

  if (loading) return <Spinner />;

  return (
    <div className="page">
      <div className="page-header">
        <h1>Projects</h1>
        <button className="btn btn-primary" onClick={() => setShowForm((v) => !v)}>
          {showForm ? "Close" : "New Project"}
        </button>
      </div>

      {showForm && (
        <form className="card" onSubmit={handleSubmit(onCreate)}>
          <FormField label="Name" error={errors.name?.message}>
            <input {...register("name", { required: "Name is required" })} />
          </FormField>
          <FormField label="Key (2-10 letters/numbers)" error={errors.key?.message}>
            <input
              {...register("key", {
                required: "Key is required",
                pattern: { value: /^[A-Za-z0-9]{2,10}$/, message: "2-10 letters or numbers" },
              })}
            />
          </FormField>
          <FormField label="Description">
            <textarea rows={3} {...register("description")} />
          </FormField>
          <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
            {isSubmitting ? "Creating..." : "Create Project"}
          </button>
        </form>
      )}

      {projects.length === 0 ? (
        <p className="muted">No projects yet. Create one to get started.</p>
      ) : (
        <div className="project-grid">
          {projects.map((project) => (
            <div
              key={project.id}
              className="project-card"
              onClick={() => navigate(`/projects/${project.id}/issues`)}
            >
              <div className="project-key">{project.key}</div>
              <h3>{project.name}</h3>
              <p className="muted">{project.description || "No description"}</p>
              <span className="role-tag">{project.my_role}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
