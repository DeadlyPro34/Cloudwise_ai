/**
 * AWS API service - calls backend /api/v1/aws/* endpoints.
 */

import { apiClient } from "./apiClient";
import type {
  AWSConnectPayload,
  AWSConnectResponse,
  AWSScanResponse,
  Resource,
} from "../types";

export async function connectAWS(payload: AWSConnectPayload): Promise<AWSConnectResponse> {
  const { data } = await apiClient.post<AWSConnectResponse>("/aws/connect", payload);
  return data;
}

export async function scanAWS(): Promise<AWSScanResponse> {
  const { data } = await apiClient.post<AWSScanResponse>("/aws/scan");
  return data;
}

export async function getResources(): Promise<Resource[]> {
  const { data } = await apiClient.get<Resource[]>("/aws/resources");
  return data;
}
