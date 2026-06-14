import { Outlet } from "react-router-dom";
import { useState } from "react";
import { Sidebar } from "../components/layout/Sidebar";
import { TopNav } from "../components/layout/TopNav";

export function AppShell() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div style={{ display: "flex", height: "100vh", overflow: "hidden" }}>
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden", minWidth: 0 }}>
        <TopNav onMenuToggle={() => setSidebarOpen((o) => !o)} />
        <main style={{ flex: 1, overflowY: "auto", padding: "1.5rem" }}>
          <Outlet />
        </main>
      </div>
    </div>
  );
}
