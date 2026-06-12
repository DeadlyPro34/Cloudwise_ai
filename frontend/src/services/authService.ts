/**
 * Auth API service - calls backend /api/v1/auth/* endpoints.
 */

import { apiClient } from "./apiClient";
import type { TokenResponse, RegisterPayload, LoginPayload, User } from "../types";

export async function registerUser(payload: RegisterPayload): Promise<TokenResponse> {
  const { data } = await apiClient.post<TokenResponse>("/auth/register", payload);
  return data;
}

export async function loginUser(payload: LoginPayload): Promise<TokenResponse> {
  const { data } = await apiClient.post<TokenResponse>("/auth/login", payload);
  return data;
}

export async function getCurrentUser(): Promise<User> {
  const { data } = await apiClient.get<User>("/auth/me");
  return data;
}
