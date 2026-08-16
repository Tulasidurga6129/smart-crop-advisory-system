import apiClient from './client';
import type { FarmDashboardResponse } from '../types';

export async function getFarmDashboard(farmId: number): Promise<FarmDashboardResponse> {
  const { data } = await apiClient.get<FarmDashboardResponse>(`/dashboard/farm/${farmId}`);
  return data;
}
