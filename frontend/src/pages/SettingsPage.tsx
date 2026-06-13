import { Settings, Key, User, Cloud } from "lucide-react";
import { useAuth } from "../store/AuthContext";
import { Button } from "../components/ui/Button";

export function SettingsPage() {
  const { user } = useAuth();

  return (
    <div>
      <div className="flex items-center gap-2 mb-6">
        <Settings className="w-8 h-8 text-(--color-accent)" />
        <h2 className="mb-0">Settings</h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card">
          <div className="flex items-center gap-2 mb-4 pb-2 border-b border-[var(--color-surface)]">
            <User className="w-5 h-5 text-(--color-accent)" />
            <h4>Profile</h4>
          </div>
          <div className="space-y-4">
            <div>
              <label className="block text-sm text-(--color-text-secondary) mb-1">Email</label>
              <div className="p-2 bg-(--color-surface) rounded-md text-sm">{user?.email || "user@example.com"}</div>
            </div>
            <div>
              <label className="block text-sm text-(--color-text-secondary) mb-1">Name</label>
              <div className="p-2 bg-(--color-surface) rounded-md text-sm">{user?.first_name} {user?.last_name}</div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center gap-2 mb-4 pb-2 border-b border-[var(--color-surface)]">
            <Cloud className="w-5 h-5 text-(--color-accent)" />
            <h4>AWS Connection</h4>
          </div>
          <div className="space-y-4">
            <div>
              <label className="block text-sm text-(--color-text-secondary) mb-1">Status</label>
              <div className="flex items-center gap-2">
                <span className="badge badge-success">Connected</span>
                <span className="text-sm">Account ID: 123456789012</span>
              </div>
            </div>
            <Button variant="secondary" className="w-full">Disconnect AWS Account</Button>
          </div>
        </div>

        <div className="card md:col-span-2">
          <div className="flex items-center gap-2 mb-4 pb-2 border-b border-[var(--color-surface)]">
            <Key className="w-5 h-5 text-(--color-accent)" />
            <h4>API Configuration</h4>
          </div>
          <div className="space-y-4 max-w-lg">
            <div>
              <label className="block text-sm text-(--color-text-secondary) mb-1">Groq API Key (for Copilot)</label>
              <div className="flex gap-2">
                <input type="password" value="gsk_..." readOnly className="input-field flex-1 opacity-50" />
                <Button variant="secondary">Update</Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
