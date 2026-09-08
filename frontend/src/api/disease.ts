import apiClient from './client';
import type { DiseaseDetectionCreate, DiseaseDetectionUpdate, DiseaseDetectionResponse } from '../types';

export interface DiseasePrediction {
  class_name: string;
  plant: string;
  disease: string;
  confidence: number;
  description: string;
  treatment: string[];
  fertilizer: string;
  prevention: string[];
}

export interface DiseasePredictionResponse {
  detection: DiseaseDetectionResponse;
  prediction: DiseasePrediction;
  image_filename: string | null;
}

export async function predictDisease(farmId: number, cropId: number, image: File): Promise<DiseasePredictionResponse> {
  const formData = new FormData();
  formData.append('image', image);
  const { data } = await apiClient.post<DiseasePredictionResponse>(
    `/disease-detections/predict?farm_id=${farmId}&crop_id=${cropId}`,
    formData,
    { headers: { 'Content-Type': 'multipart/form-data' } },
  );
  return data;
}

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
