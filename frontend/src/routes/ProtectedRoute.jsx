import { Navigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";
import Spinner from "../components/Spinner";

// Gate protected pages: send guests to /login once the session check is done.
export default function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();

  if (loading) return <Spinner />;
  if (!user) return <Navigate to="/login" replace />;

  return children;
}
