import { Outlet } from "react-router-dom";
import { Sidebar } from "../components/layout/Sidebar";
import { TopNav } from "../components/layout/TopNav";

/**
 * AppShell - per UI/UX Brief Section 8:
 *
 * ┌─────────────────────────────────────┐
 * │            Top Navigation            │
 * ├────────────┬────────────────────────┤
 * │  Sidebar   │      Main Content       │
 * │            │                          │
 * └────────────┴────────────────────────┘
 */
export function AppShell() {
  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <TopNav />
        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
