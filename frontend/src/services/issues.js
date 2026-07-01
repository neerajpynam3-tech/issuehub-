import api from "./api";

// `filters` maps directly to the query params the backend understands:
// q, status, priority, assignee, sort, page, page_size.
export function listIssues(projectId, filters = {}) {
  return api
    .get(`/projects/${projectId}/issues`, { params: filters })
    .then((res) => res.data);
}

export function createIssue(projectId, data) {
  return api.post(`/projects/${projectId}/issues`, data).then((res) => res.data);
}

export function getIssue(issueId) {
  return api.get(`/issues/${issueId}`).then((res) => res.data);
}

export function updateIssue(issueId, data) {
  return api.patch(`/issues/${issueId}`, data).then((res) => res.data);
}

export function deleteIssue(issueId) {
  return api.delete(`/issues/${issueId}`).then((res) => res.data);
}

export function enhanceDescription(data) {
  return api.post("/issues/enhance", data).then((res) => res.data);
}
