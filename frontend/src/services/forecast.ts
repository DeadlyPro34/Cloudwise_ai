/**
 * Forecast API service - calls backend /api/v1/forecast.
 */

import { apiClient } from "./apiClient";
import type { ForecastData } from "../types";

export async function getForecasts(): Promise<ForecastData[]> {
  const { data } = await apiClient.get<ForecastData[]>("/forecast");
  return data;
}
