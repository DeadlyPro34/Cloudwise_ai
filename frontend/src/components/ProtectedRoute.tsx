import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../store/AuthContext";

/**
 * ProtectedRoute - per AFD Section 19:
 * Unauthorized users redirect to /login for all app pages.
 */
export function ProtectedRoute() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="skeleton w-32 h-8" />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}
