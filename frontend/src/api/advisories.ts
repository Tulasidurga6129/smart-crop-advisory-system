import apiClient from './client';
import type { CropAdvisoryCreate, CropAdvisoryUpdate, CropAdvisoryResponse } from '../types';

export async function createAdvisory(payload: CropAdvisoryCreate): Promise<CropAdvisoryResponse> {
  const { data } = await apiClient.post<CropAdvisoryResponse>('/crop-advisories', payload);
  return data;
}

export async function getFarmAdvisories(farmId: number): Promise<CropAdvisoryResponse[]> {
  const { data } = await apiClient.get<CropAdvisoryResponse[]>(`/crop-advisories/farm/${farmId}`);
  return data;
}

export async function getActiveFarmAdvisories(farmId: number): Promise<CropAdvisoryResponse[]> {
  const { data } = await apiClient.get<CropAdvisoryResponse[]>(`/crop-advisories/farm/${farmId}/active`);
  return data;
}

export async function getCropAdvisories(cropId: number): Promise<CropAdvisoryResponse[]> {
  const { data } = await apiClient.get<CropAdvisoryResponse[]>(`/crop-advisories/crop/${cropId}`);
  return data;
}

export async function resolveAdvisory(advisoryId: number): Promise<CropAdvisoryResponse> {
  const { data } = await apiClient.post<CropAdvisoryResponse>(`/crop-advisories/${advisoryId}/resolve`);
  return data;
}

export async function dismissAdvisory(advisoryId: number): Promise<CropAdvisoryResponse> {
  const { data } = await apiClient.post<CropAdvisoryResponse>(`/crop-advisories/${advisoryId}/dismiss`);
  return data;
}

export async function getAdvisory(advisoryId: number): Promise<CropAdvisoryResponse> {
  const { data } = await apiClient.get<CropAdvisoryResponse>(`/crop-advisories/${advisoryId}`);
  return data;
}

export async function updateAdvisory(advisoryId: number, payload: CropAdvisoryUpdate): Promise<CropAdvisoryResponse> {
  const { data } = await apiClient.put<CropAdvisoryResponse>(`/crop-advisories/${advisoryId}`, payload);
  return data;
}

export async function deleteAdvisory(advisoryId: number): Promise<void> {
  await apiClient.delete(`/crop-advisories/${advisoryId}`);
}
