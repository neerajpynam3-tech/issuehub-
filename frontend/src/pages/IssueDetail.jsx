import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import Badge from "../components/Badge";
import CommentComposer from "../components/CommentComposer";
import CommentList from "../components/CommentList";
import Spinner from "../components/Spinner";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";
import { addComment, listComments } from "../services/comments";
import { deleteIssue, getIssue, updateIssue } from "../services/issues";
import { listMembers } from "../services/projects";
import { getErrorMessage } from "../services/api";
import {
  PRIORITY_COLORS,
  PRIORITY_LABELS,
  STATUSES,
  STATUS_COLORS,
  STATUS_LABELS,
} from "../utils/enums";
import { formatDateTime } from "../utils/format";

export default function IssueDetail() {
  const { issueId } = useParams();
  const { user } = useAuth();
  const { showToast } = useToast();
  const navigate = useNavigate();

  const [issue, setIssue] = useState(null);
  const [comments, setComments] = useState([]);
  const [members, setMembers] = useState([]);
  const [loading, setLoading] = useState(true);

  const isMaintainer =
    members.find((m) => m.user.id === user?.id)?.role === "maintainer";

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const loadedIssue = await getIssue(issueId);
        setIssue(loadedIssue);
        const [loadedComments, loadedMembers] = await Promise.all([
          listComments(issueId),
          listMembers(loadedIssue.project_id),
        ]);
        setComments(loadedComments);
        setMembers(loadedMembers);
      } catch (error) {
        showToast(getErrorMessage(error), "error");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [issueId, showToast]);

  // Maintainer-only: change status or assignee, then refresh the issue.
  async function patchIssue(changes) {
    try {
      const updated = await updateIssue(issueId, changes);
      setIssue(updated);
      showToast("Issue updated");
    } catch (error) {
      showToast(getErrorMessage(error), "error");
    }
  }

  async function handleAddComment(body) {
    try {
      const comment = await addComment(issueId, body);
      setComments((prev) => [...prev, comment]);
    } catch (error) {
      showToast(getErrorMessage(error), "error");
    }
  }

  async function handleDelete() {
    if (!window.confirm("Delete this issue? This cannot be undone.")) return;
    try {
      await deleteIssue(issueId);
      showToast("Issue deleted");
      navigate(`/projects/${issue.project_id}/issues`);
    } catch (error) {
      showToast(getErrorMessage(error), "error");
    }
  }

  if (loading) return <Spinner />;
  if (!issue) return <p className="muted">Issue not found.</p>;

  return (
    <div className="page issue-detail">
      <button className="btn btn-ghost" onClick={() => navigate(-1)}>
        ← Back
      </button>

      <div className="page-header">
        <h1>{issue.title}</h1>
        {isMaintainer && (
          <button className="btn btn-danger" onClick={handleDelete}>
            Delete
          </button>
        )}
      </div>

      <div className="issue-meta">
        <div>
          <span className="muted">Status</span>
          {isMaintainer ? (
            <select
              value={issue.status}
              onChange={(e) => patchIssue({ status: e.target.value })}
            >
              {STATUSES.map((status) => (
                <option key={status} value={status}>
                  {STATUS_LABELS[status]}
                </option>
              ))}
            </select>
          ) : (
            <Badge label={STATUS_LABELS[issue.status]} color={STATUS_COLORS[issue.status]} />
          )}
        </div>

        <div>
          <span className="muted">Priority</span>
          <Badge
            label={PRIORITY_LABELS[issue.priority]}
            color={PRIORITY_COLORS[issue.priority]}
          />
        </div>

        <div>
          <span className="muted">Assignee</span>
          {isMaintainer ? (
            <select
              value={issue.assignee?.id || ""}
              onChange={(e) =>
                patchIssue({ assignee_id: e.target.value ? Number(e.target.value) : null })
              }
            >
              <option value="">Unassigned</option>
              {members.map((member) => (
                <option key={member.user.id} value={member.user.id}>
                  {member.user.name}
                </option>
              ))}
            </select>
          ) : (
            <span>{issue.assignee ? issue.assignee.name : "Unassigned"}</span>
          )}
        </div>

        <div>
          <span className="muted">Reporter</span>
          <span>{issue.reporter.name}</span>
        </div>

        <div>
          <span className="muted">Created</span>
          <span>{formatDateTime(issue.created_at)}</span>
        </div>
      </div>

      <section className="issue-description">
        <h3>Description</h3>
        <p>{issue.description || "No description provided."}</p>
      </section>

      <section className="comments-section">
        <h3>Comments</h3>
        <CommentList comments={comments} />
        <CommentComposer onSubmit={handleAddComment} />
      </section>
    </div>
  );
}
