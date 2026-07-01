import { Navigate, Route, Routes } from "react-router-dom";

import Layout from "../components/Layout";
import ProtectedRoute from "./ProtectedRoute";
import Login from "../pages/Login";
import Signup from "../pages/Signup";
import Projects from "../pages/Projects";
import ProjectIssues from "../pages/ProjectIssues";
import IssueDetail from "../pages/IssueDetail";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />

      <Route
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route path="/projects" element={<Projects />} />
        <Route path="/projects/:projectId/issues" element={<ProjectIssues />} />
        <Route path="/issues/:issueId" element={<IssueDetail />} />
      </Route>

      <Route path="*" element={<Navigate to="/projects" replace />} />
    </Routes>
  );
}
