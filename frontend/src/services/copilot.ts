/**
 * Copilot API service - calls backend /api/v1/copilot/* endpoints.
 */

import { apiClient } from "./apiClient";
import type { CopilotChatPayload, CopilotChatResponse, CopilotMessage } from "../types";

export async function sendMessage(payload: CopilotChatPayload): Promise<CopilotChatResponse> {
  const { data } = await apiClient.post<CopilotChatResponse>("/copilot/chat", payload);
  return data;
}

export async function getChatHistory(conversationId: string): Promise<CopilotMessage[]> {
  const { data } = await apiClient.get<CopilotMessage[]>("/copilot/history", {
    params: { conversation_id: conversationId },
  });
  return data;
}
