import { useState } from "react";
import { MessageSquare, Send } from "lucide-react";
import { Button } from "../components/ui/Button";

export function CopilotPage() {
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([
    { role: "assistant", content: "Hi! I'm your CloudWise Copilot. How can I help you optimize your AWS environment today?" },
  ]);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;
    setMessages([...messages, { role: "user", content: input }]);
    setInput("");
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "The AI Copilot is not configured yet. Please add your Anthropic API key in Settings." },
      ]);
    }, 1000);
  };

  return (
    <div className="flex flex-col h-full max-h-[800px] card">
      <div className="flex items-center gap-2 mb-4 border-b border-[var(--color-surface)] pb-4">
        <MessageSquare className="w-6 h-6 text-(--color-accent)" />
        <h2>AI Copilot</h2>
      </div>

      <div className="flex-1 overflow-y-auto flex flex-col gap-4 mb-4 pr-2">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            <div className={`max-w-[70%] p-3 rounded-lg ${msg.role === "user" ? "bg-(--color-accent) text-white" : "bg-(--color-surface)"}`}>
              <p className="text-sm">{msg.content}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          className="input-field flex-1"
          placeholder="Ask a question about your cloud costs..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <Button onClick={handleSend} className="px-4 py-2 flex items-center justify-center">
          <Send className="w-5 h-5" />
        </Button>
      </div>
    </div>
  );
}
