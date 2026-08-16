import apiClient from './client';
import type { CropCreate, CropUpdate, CropResponse } from '../types';

export async function getFarmCrops(farmId: number): Promise<CropResponse[]> {
  const { data } = await apiClient.get<CropResponse[]>(`/crops/farm/${farmId}`);
  return data;
}

export async function getCrop(cropId: number): Promise<CropResponse> {
  const { data } = await apiClient.get<CropResponse>(`/crops/${cropId}`);
  return data;
}

export async function createCrop(payload: CropCreate): Promise<CropResponse> {
  const { data } = await apiClient.post<CropResponse>('/crops', payload);
  return data;
}

export async function updateCrop(cropId: number, payload: CropUpdate): Promise<CropResponse> {
  const { data } = await apiClient.put<CropResponse>(`/crops/${cropId}`, payload);
  return data;
}

export async function deleteCrop(cropId: number): Promise<void> {
  await apiClient.delete(`/crops/${cropId}`);
}
