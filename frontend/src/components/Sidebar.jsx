import { NavLink } from "react-router-dom";

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <nav>
        <NavLink to="/projects" className="sidebar-link">
          Projects
        </NavLink>
      </nav>
    </aside>
  );
}
