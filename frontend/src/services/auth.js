import api from "./api";

export function signup(data) {
  return api.post("/auth/signup", data).then((res) => res.data);
}

export function login(data) {
  return api.post("/auth/login", data).then((res) => res.data);
}

export function getMe() {
  return api.get("/me").then((res) => res.data);
}
