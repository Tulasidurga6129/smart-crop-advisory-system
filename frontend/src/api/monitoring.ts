import apiClient from './client';
import type { CropMonitoringCreate, CropMonitoringUpdate, CropMonitoringResponse } from '../types';

export async function createMonitoring(payload: CropMonitoringCreate): Promise<CropMonitoringResponse> {
  const { data } = await apiClient.post<CropMonitoringResponse>('/crop-monitoring', payload);
  return data;
}

export async function getCropMonitoringRecords(cropId: number): Promise<CropMonitoringResponse[]> {
  const { data } = await apiClient.get<CropMonitoringResponse[]>(`/crop-monitoring/crop/${cropId}`);
  return data;
}

export async function getMonitoring(monitoringId: number): Promise<CropMonitoringResponse> {
  const { data } = await apiClient.get<CropMonitoringResponse>(`/crop-monitoring/${monitoringId}`);
  return data;
}

export async function updateMonitoring(monitoringId: number, payload: CropMonitoringUpdate): Promise<CropMonitoringResponse> {
  const { data } = await apiClient.put<CropMonitoringResponse>(`/crop-monitoring/${monitoringId}`, payload);
  return data;
}

export async function deleteMonitoring(monitoringId: number): Promise<void> {
  await apiClient.delete(`/crop-monitoring/${monitoringId}`);
}
