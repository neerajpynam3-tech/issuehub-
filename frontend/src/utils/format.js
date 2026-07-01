export function formatDateTime(isoString) {
  if (!isoString) return "";
  return new Date(isoString).toLocaleString(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  });
}
