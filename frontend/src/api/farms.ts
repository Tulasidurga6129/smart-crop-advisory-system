import apiClient from './client';
import type { FarmCreate, FarmUpdate, FarmResponse } from '../types';

export async function getMyFarms(): Promise<FarmResponse[]> {
  const { data } = await apiClient.get<FarmResponse[]>('/farms');
  return data;
}

export async function getFarm(farmId: number): Promise<FarmResponse> {
  const { data } = await apiClient.get<FarmResponse>(`/farms/${farmId}`);
  return data;
}

export async function createFarm(payload: FarmCreate): Promise<FarmResponse> {
  const { data } = await apiClient.post<FarmResponse>('/farms', payload);
  return data;
}

export async function updateFarm(farmId: number, payload: FarmUpdate): Promise<FarmResponse> {
  const { data } = await apiClient.put<FarmResponse>(`/farms/${farmId}`, payload);
  return data;
}

export async function deleteFarm(farmId: number): Promise<void> {
  await apiClient.delete(`/farms/${farmId}`);
}
