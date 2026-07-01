// Single source of truth for the option lists and their display colors.
// Keeping labels/colors here avoids scattering magic strings across components.

export const STATUSES = ["open", "in_progress", "resolved", "closed"];
export const PRIORITIES = ["low", "medium", "high", "critical"];

export const STATUS_LABELS = {
  open: "Open",
  in_progress: "In Progress",
  resolved: "Resolved",
  closed: "Closed",
};

export const PRIORITY_LABELS = {
  low: "Low",
  medium: "Medium",
  high: "High",
  critical: "Critical",
};

export const STATUS_COLORS = {
  open: "#2563eb",
  in_progress: "#d97706",
  resolved: "#059669",
  closed: "#6b7280",
};

export const PRIORITY_COLORS = {
  low: "#6b7280",
  medium: "#2563eb",
  high: "#d97706",
  critical: "#dc2626",
};

export const SORT_OPTIONS = [
  { value: "created_at", label: "Newest" },
  { value: "priority", label: "Priority" },
  { value: "status", label: "Status" },
];
