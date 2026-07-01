import { useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <header className="navbar">
      <div className="navbar-brand">IssueHub</div>
      <div className="navbar-right">
        <span className="navbar-user">{user?.name}</span>
        <button className="btn btn-ghost" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </header>
  );
}
