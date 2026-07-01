import api from "./api";

export function listComments(issueId) {
  return api.get(`/issues/${issueId}/comments`).then((res) => res.data);
}

export function addComment(issueId, body) {
  return api.post(`/issues/${issueId}/comments`, { body }).then((res) => res.data);
}
