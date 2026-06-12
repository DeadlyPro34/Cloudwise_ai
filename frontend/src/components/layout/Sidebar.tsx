import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Server,
  Lightbulb,
  MessageSquareText,
  FileText,
  Settings,
  Cloud,
} from "lucide-react";

// Navigation items per UI/UX Brief Section 9
const NAV_ITEMS = [
  { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/resources", label: "Resources", icon: Server },
  { to: "/recommendations", label: "Recommendations", icon: Lightbulb },
  { to: "/copilot", label: "Copilot", icon: MessageSquareText },
  { to: "/reports", label: "Reports", icon: FileText },
  { to: "/settings", label: "Settings", icon: Settings },
];

export function Sidebar() {
  return (
    <aside className="w-[260px] h-screen flex flex-col border-r border-(--color-surface) bg-(--color-bg-secondary) px-3 py-4">
      {/* Logo */}
      <div className="flex items-center gap-2 px-3 py-3 mb-4">
        <Cloud className="w-6 h-6 text-(--color-accent-hover)" />
        <span className="text-lg font-semibold">CloudWise AI</span>
      </div>

      {/* Navigation */}
      <nav className="flex flex-col gap-1">
        {NAV_ITEMS.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `nav-item ${isActive ? "nav-item-active" : ""}`
            }
          >
            <Icon className="w-5 h-5" />
            {label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
