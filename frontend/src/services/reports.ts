/**
 * Reports API service - calls backend /api/v1/reports/generate.
 * Returns a Blob (PDF) for client-side download.
 */

import { apiClient } from "./apiClient";

export async function generateReport(): Promise<Blob> {
  const { data } = await apiClient.post("/reports/generate", null, {
    responseType: "blob",
  });
  return data;
}
