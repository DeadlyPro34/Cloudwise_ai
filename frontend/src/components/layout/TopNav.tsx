import { Search, Bell, LogOut } from "lucide-react";
import { useAuth } from "../../store/AuthContext";

export function TopNav() {
  const { user, logout } = useAuth();

  const initials = user
    ? `${user.first_name?.[0] ?? ""}${user.last_name?.[0] ?? ""}`.toUpperCase() ||
      user.email[0].toUpperCase()
    : "?";

  return (
    <header className="h-16 flex items-center justify-between px-6 border-b border-(--color-surface) bg-(--color-bg-primary)">
      {/* Search */}
      <div className="flex items-center gap-2 bg-(--color-surface) rounded-lg px-3 py-2 w-80 max-w-full">
        <Search className="w-4 h-4 text-(--color-text-secondary)" />
        <input
          type="text"
          placeholder="Search resources, recommendations..."
          className="bg-transparent outline-none text-sm w-full placeholder:text-(--color-text-secondary)"
        />
      </div>

      {/* Right side */}
      <div className="flex items-center gap-4">
        <button className="relative p-2 rounded-lg hover:bg-(--color-surface) transition-colors">
          <Bell className="w-5 h-5 text-(--color-text-secondary)" />
        </button>

        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-full bg-(--color-accent) flex items-center justify-center text-sm font-semibold">
            {initials}
          </div>
          <div className="text-sm hidden sm:block">
            <p className="font-medium leading-tight">
              {user?.first_name ? `${user.first_name} ${user.last_name ?? ""}`.trim() : user?.email}
            </p>
          </div>
          <button
            onClick={logout}
            title="Log out"
            className="p-2 rounded-lg hover:bg-(--color-surface) transition-colors text-(--color-text-secondary)"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
}
