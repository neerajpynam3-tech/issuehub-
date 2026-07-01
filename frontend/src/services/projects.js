import api from "./api";

export function listProjects() {
  return api.get("/projects").then((res) => res.data);
}

export function createProject(data) {
  return api.post("/projects", data).then((res) => res.data);
}

export function listMembers(projectId) {
  return api.get(`/projects/${projectId}/members`).then((res) => res.data);
}

export function addMember(projectId, data) {
  return api.post(`/projects/${projectId}/members`, data).then((res) => res.data);
}
