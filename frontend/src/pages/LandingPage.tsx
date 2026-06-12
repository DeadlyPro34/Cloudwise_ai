import { Link } from "react-router-dom";
import { Cloud, TrendingUp, Lightbulb, MessageSquareText, Activity } from "lucide-react";

export function LandingPage() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Nav */}
      <header className="flex items-center justify-between px-6 py-4 border-b border-(--color-surface)">
        <div className="flex items-center gap-2">
          <Cloud className="w-6 h-6 text-(--color-accent-hover)" />
          <span className="text-lg font-semibold">CloudWise AI</span>
        </div>
        <div className="flex items-center gap-3">
          <Link to="/login" className="btn-secondary">Log In</Link>
          <Link to="/signup" className="btn-primary">Get Started</Link>
        </div>
      </header>

      {/* Hero */}
      <section className="flex-1 flex flex-col items-center justify-center text-center px-6 py-20">
        <span className="badge badge-accent mb-4">AI-Powered FinOps Copilot</span>
        <h1 className="max-w-3xl mb-4">
          Turn Cloud Costs Into <span className="text-(--color-accent-hover)">Cloud Intelligence</span>
        </h1>
        <p className="max-w-xl text-(--color-text-secondary) mb-8 text-lg">
          CloudWise AI connects to your AWS account, discovers waste, forecasts spending,
          and explains exactly what to fix — in plain English.
        </p>
        <div className="flex gap-3">
          <Link to="/signup" className="btn-primary px-6 py-3 text-lg">Get Started</Link>
          <Link to="/login" className="btn-secondary px-6 py-3 text-lg">Connect AWS</Link>
        </div>
      </section>

      {/* Features */}
      <section className="px-6 py-16 border-t border-(--color-surface)">
        <div className="max-w-5xl mx-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          <FeatureCard icon={Activity} title="Cost Analysis" desc="Real-time visibility into AWS spend" />
          <FeatureCard icon={TrendingUp} title="Forecasting" desc="Predict spend 7/30/90 days ahead" />
          <FeatureCard icon={Lightbulb} title="Recommendations" desc="Actionable optimization suggestions" />
          <FeatureCard icon={MessageSquareText} title="AI Copilot" desc="Ask questions in plain English" />
          <FeatureCard icon={Cloud} title="Health Score" desc="One number for cloud efficiency" />
        </div>
      </section>

      {/* Footer */}
      <footer className="px-6 py-6 border-t border-(--color-surface) text-center caption">
        CloudWise AI — Autonomous FinOps Copilot for AWS Infrastructure
      </footer>
    </div>
  );
}

function FeatureCard({
  icon: Icon,
  title,
  desc,
}: {
  icon: typeof Activity;
  title: string;
  desc: string;
}) {
  return (
    <div className="card text-left">
      <Icon className="w-6 h-6 text-(--color-accent-hover) mb-3" />
      <h4 className="mb-1">{title}</h4>
      <p className="caption">{desc}</p>
    </div>
  );
}
