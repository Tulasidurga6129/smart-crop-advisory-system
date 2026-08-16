import apiClient from './client';
import type { DiseaseDetectionCreate, DiseaseDetectionUpdate, DiseaseDetectionResponse } from '../types';

// NOTE: this backend endpoint takes a JSON body describing an already-known
// diagnosis (disease_name, severity, symptoms, etc.) — there is no image
// upload parameter in the OpenAPI spec, so this is a record-entry form, not
// an image-based ML analysis call.
export async function createDetection(payload: DiseaseDetectionCreate): Promise<DiseaseDetectionResponse> {
  const { data } = await apiClient.post<DiseaseDetectionResponse>('/disease-detections', payload);
  return data;
}

export async function getFarmDetections(farmId: number): Promise<DiseaseDetectionResponse[]> {
  const { data } = await apiClient.get<DiseaseDetectionResponse[]>(`/disease-detections/farm/${farmId}`);
  return data;
}

export async function getCropDetections(cropId: number): Promise<DiseaseDetectionResponse[]> {
  const { data } = await apiClient.get<DiseaseDetectionResponse[]>(`/disease-detections/crop/${cropId}`);
  return data;
}

export async function getDetection(detectionId: number): Promise<DiseaseDetectionResponse> {
  const { data } = await apiClient.get<DiseaseDetectionResponse>(`/disease-detections/${detectionId}`);
  return data;
}

export async function updateDetection(detectionId: number, payload: DiseaseDetectionUpdate): Promise<DiseaseDetectionResponse> {
  const { data } = await apiClient.put<DiseaseDetectionResponse>(`/disease-detections/${detectionId}`, payload);
  return data;
}

export async function deleteDetection(detectionId: number): Promise<void> {
  await apiClient.delete(`/disease-detections/${detectionId}`);
}
