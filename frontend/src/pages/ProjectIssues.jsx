import { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import IssueFilters from "../components/IssueFilters";
import IssueRow from "../components/IssueRow";
import NewIssueModal from "../components/NewIssueModal";
import Spinner from "../components/Spinner";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../context/ToastContext";
import { listIssues } from "../services/issues";
import { addMember, listMembers } from "../services/projects";
import { getErrorMessage } from "../services/api";

const PAGE_SIZE = 10;
const EMPTY_FILTERS = { q: "", status: "", priority: "", assignee: "", sort: "created_at" };

export default function ProjectIssues() {
  const { projectId } = useParams();
  const { user } = useAuth();
  const { showToast } = useToast();

  const [filters, setFilters] = useState(EMPTY_FILTERS);
  const [page, setPage] = useState(1);
  const [data, setData] = useState({ items: [], total: 0 });
  const [loading, setLoading] = useState(true);
  const [members, setMembers] = useState([]);
  const [showNewIssue, setShowNewIssue] = useState(false);
  const [newMemberEmail, setNewMemberEmail] = useState("");

  // Am I a maintainer of this project? Drives the "Add member" control.
  const myMembership = members.find((m) => m.user.id === user?.id);
  const isMaintainer = myMembership?.role === "maintainer";

  const loadIssues = useCallback(() => {
    setLoading(true);
    // Drop empty filter values so we don't send blank query params.
    const params = { sort: filters.sort, page, page_size: PAGE_SIZE };
    if (filters.q) params.q = filters.q;
    if (filters.status) params.status = filters.status;
    if (filters.priority) params.priority = filters.priority;
    if (filters.assignee) params.assignee = filters.assignee;

    listIssues(projectId, params)
      .then(setData)
      .catch((err) => showToast(getErrorMessage(err), "error"))
      .finally(() => setLoading(false));
  }, [projectId, filters, page, showToast]);

  // Debounce so typing in the search box doesn't fire a request per keystroke.
  useEffect(() => {
    const timer = setTimeout(loadIssues, 300);
    return () => clearTimeout(timer);
  }, [loadIssues]);

  useEffect(() => {
    listMembers(projectId)
      .then(setMembers)
      .catch((err) => showToast(getErrorMessage(err), "error"));
  }, [projectId, showToast]);

  function handleFilterChange(field, value) {
    setPage(1); // any filter change resets to the first page
    setFilters((prev) => ({ ...prev, [field]: value }));
  }

  async function handleAddMember(event) {
    event.preventDefault();
    if (!newMemberEmail.trim()) return;
    try {
      await addMember(projectId, { email: newMemberEmail.trim(), role: "member" });
      showToast("Member added");
      setNewMemberEmail("");
      const updated = await listMembers(projectId);
      setMembers(updated);
    } catch (error) {
      showToast(getErrorMessage(error), "error");
    }
  }

  const totalPages = Math.max(1, Math.ceil(data.total / PAGE_SIZE));

  return (
    <div className="page">
      <div className="page-header">
        <h1>Issues</h1>
        <button className="btn btn-primary" onClick={() => setShowNewIssue(true)}>
          New Issue
        </button>
      </div>

      {isMaintainer && (
        <form className="add-member" onSubmit={handleAddMember}>
          <input
            type="email"
            placeholder="Add member by email"
            value={newMemberEmail}
            onChange={(e) => setNewMemberEmail(e.target.value)}
          />
          <button type="submit" className="btn btn-ghost">
            Add Member
          </button>
        </form>
      )}

      <IssueFilters filters={filters} members={members} onChange={handleFilterChange} />

      {loading ? (
        <Spinner />
      ) : data.items.length === 0 ? (
        <p className="muted">No issues match your filters.</p>
      ) : (
        <table className="issues-table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Status</th>
              <th>Priority</th>
              <th>Assignee</th>
              <th>Reporter</th>
            </tr>
          </thead>
          <tbody>
            {data.items.map((issue) => (
              <IssueRow key={issue.id} issue={issue} />
            ))}
          </tbody>
        </table>
      )}

      <div className="pagination">
        <button
          className="btn btn-ghost"
          disabled={page <= 1}
          onClick={() => setPage((p) => p - 1)}
        >
          Previous
        </button>
        <span>
          Page {page} of {totalPages} ({data.total} issues)
        </span>
        <button
          className="btn btn-ghost"
          disabled={page >= totalPages}
          onClick={() => setPage((p) => p + 1)}
        >
          Next
        </button>
      </div>

      {showNewIssue && (
        <NewIssueModal
          projectId={projectId}
          members={members}
          onClose={() => setShowNewIssue(false)}
          onCreated={() => {
            setShowNewIssue(false);
            loadIssues();
          }}
        />
      )}
    </div>
  );
}
