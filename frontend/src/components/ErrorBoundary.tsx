import { ErrorBoundary as ReactErrorBoundary, type FallbackProps } from "react-error-boundary";
import { AlertTriangle, RefreshCw } from "lucide-react";

function ErrorFallback({ error, resetErrorBoundary }: FallbackProps) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 p-4">
      <div className="max-w-md w-full bg-white dark:bg-gray-800 rounded-xl shadow-xl overflow-hidden border border-gray-100 dark:border-gray-700">
        <div className="p-6 sm:p-8">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-red-100 dark:bg-red-900/30 mb-6">
            <AlertTriangle className="h-6 w-6 text-red-600 dark:text-red-400" />
          </div>
          
          <h2 className="text-xl font-bold text-center text-gray-900 dark:text-white mb-2">
            Something went wrong
          </h2>
          
          <p className="text-sm text-center text-gray-500 dark:text-gray-400 mb-6">
            An unexpected error occurred in the application.
          </p>
          
          <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4 mb-6 overflow-auto max-h-40 border border-gray-100 dark:border-gray-800">
            <pre className="text-xs text-red-600 dark:text-red-400 font-mono whitespace-pre-wrap">
              {error instanceof Error ? error.message : String(error)}
            </pre>
          </div>
          
          <button
            onClick={resetErrorBoundary}
            className="w-full flex justify-center items-center gap-2 py-2.5 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors"
          >
            <RefreshCw className="h-4 w-4" />
            Try Again
          </button>
        </div>
      </div>
    </div>
  );
}

export function GlobalErrorBoundary({ children }: { children: React.ReactNode }) {
  return (
    <ReactErrorBoundary
      FallbackComponent={ErrorFallback}
      onReset={() => {
        window.location.href = "/";
      }}
    >
      {children}
    </ReactErrorBoundary>
  );
}
