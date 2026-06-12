import { FileText, Download } from "lucide-react";
import { Button } from "../components/ui/Button";
import { useState } from "react";

export function ReportsPage() {
  const [loading, setLoading] = useState(false);

  const generateReport = () => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      alert("Report downloaded successfully!");
    }, 2000);
  };

  return (
    <div>
      <div className="flex items-center gap-2 mb-6">
        <FileText className="w-8 h-8 text-(--color-accent)" />
        <h2 className="mb-0">Reports</h2>
      </div>
      
      <div className="card max-w-2xl">
        <h4 className="mb-2">Executive Summary Report</h4>
        <p className="caption mb-6">
          Generate a comprehensive PDF report containing your cloud health score, cost trends, 
          top recommendations, and AI-generated insights. Perfect for sharing with stakeholders.
        </p>
        <Button onClick={generateReport} isLoading={loading} className="flex items-center gap-2">
          <Download className="w-4 h-4" />
          Generate & Download PDF
        </Button>
      </div>
    </div>
  );
}
