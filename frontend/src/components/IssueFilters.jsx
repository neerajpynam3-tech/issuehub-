import {
  PRIORITIES,
  PRIORITY_LABELS,
  SORT_OPTIONS,
  STATUSES,
  STATUS_LABELS,
} from "../utils/enums";

// Search box + status/priority/assignee filters + sort dropdown.
// Fully controlled: it reports every change up via `onChange(field, value)`.
export default function IssueFilters({ filters, members, onChange }) {
  return (
    <div className="filters">
      <input
        type="text"
        placeholder="Search title..."
        value={filters.q}
        onChange={(e) => onChange("q", e.target.value)}
      />

      <select value={filters.status} onChange={(e) => onChange("status", e.target.value)}>
        <option value="">All statuses</option>
        {STATUSES.map((status) => (
          <option key={status} value={status}>
            {STATUS_LABELS[status]}
          </option>
        ))}
      </select>

      <select value={filters.priority} onChange={(e) => onChange("priority", e.target.value)}>
        <option value="">All priorities</option>
        {PRIORITIES.map((priority) => (
          <option key={priority} value={priority}>
            {PRIORITY_LABELS[priority]}
          </option>
        ))}
      </select>

      <select value={filters.assignee} onChange={(e) => onChange("assignee", e.target.value)}>
        <option value="">All assignees</option>
        {members.map((member) => (
          <option key={member.user.id} value={member.user.id}>
            {member.user.name}
          </option>
        ))}
      </select>

      <select value={filters.sort} onChange={(e) => onChange("sort", e.target.value)}>
        {SORT_OPTIONS.map((option) => (
          <option key={option.value} value={option.value}>
            Sort: {option.label}
          </option>
        ))}
      </select>
    </div>
  );
}
