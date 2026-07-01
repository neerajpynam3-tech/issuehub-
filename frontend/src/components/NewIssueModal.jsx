import { useState } from "react";
import { useForm } from "react-hook-form";

import FormField from "./FormField";
import { PRIORITIES, PRIORITY_LABELS } from "../utils/enums";
import { createIssue, enhanceDescription } from "../services/issues";
import { getErrorMessage } from "../services/api";
import { useToast } from "../context/ToastContext";

// Modal form for filing a new issue. Includes the bonus "AI Enhance" action,
// which rewrites the description into a structured bug report before submitting.
export default function NewIssueModal({ projectId, members, onClose, onCreated }) {
  const {
    register,
    handleSubmit,
    setValue,
    getValues,
    formState: { errors, isSubmitting },
  } = useForm({ defaultValues: { priority: "medium", assignee_id: "" } });
  const { showToast } = useToast();
  const [enhancing, setEnhancing] = useState(false);

  async function onSubmit(values) {
    try {
      const payload = {
        title: values.title,
        description: values.description || null,
        priority: values.priority,
        assignee_id: values.assignee_id ? Number(values.assignee_id) : null,
      };
      const issue = await createIssue(projectId, payload);
      showToast("Issue created");
      onCreated(issue);
    } catch (error) {
      showToast(getErrorMessage(error), "error");
    }
  }

  async function handleEnhance() {
    const { title, description } = getValues();
    if (!title || !description) {
      showToast("Add a title and description first", "error");
      return;
    }
    setEnhancing(true);
    try {
      const result = await enhanceDescription({ title, description });
      setValue("description", result.enhanced_description);
      showToast("Description enhanced");
    } catch (error) {
      showToast(getErrorMessage(error), "error");
    } finally {
      setEnhancing(false);
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <h2>New Issue</h2>
        <form onSubmit={handleSubmit(onSubmit)}>
          <FormField label="Title" error={errors.title?.message}>
            <input {...register("title", { required: "Title is required" })} />
          </FormField>

          <FormField label="Description">
            <textarea rows={6} {...register("description")} />
          </FormField>

          <button
            type="button"
            className="btn btn-ghost"
            onClick={handleEnhance}
            disabled={enhancing}
          >
            {enhancing ? "Enhancing..." : "✨ AI Enhance Description"}
          </button>

          <FormField label="Priority">
            <select {...register("priority")}>
              {PRIORITIES.map((priority) => (
                <option key={priority} value={priority}>
                  {PRIORITY_LABELS[priority]}
                </option>
              ))}
            </select>
          </FormField>

          <FormField label="Assignee">
            <select {...register("assignee_id")}>
              <option value="">Unassigned</option>
              {members.map((member) => (
                <option key={member.user.id} value={member.user.id}>
                  {member.user.name}
                </option>
              ))}
            </select>
          </FormField>

          <div className="modal-actions">
            <button type="button" className="btn btn-ghost" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
              {isSubmitting ? "Creating..." : "Create Issue"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
