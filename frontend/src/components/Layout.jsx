import { Outlet } from "react-router-dom";

import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

export default function Layout() {
  return (
    <div className="layout">
      <Navbar />
      <div className="layout-body">
        <Sidebar />
        <main className="layout-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
