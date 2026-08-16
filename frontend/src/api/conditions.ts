import apiClient from './client';
import type { FarmConditionCreate, FarmConditionUpdate, FarmConditionResponse } from '../types';

export async function getFarmConditions(farmId: number): Promise<FarmConditionResponse[]> {
  const { data } = await apiClient.get<FarmConditionResponse[]>(`/conditions/farm/${farmId}`);
  return data;
}

export async function createFarmCondition(farmId: number, payload: FarmConditionCreate): Promise<FarmConditionResponse> {
  const { data } = await apiClient.post<FarmConditionResponse>(`/conditions/farm/${farmId}`, payload);
  return data;
}

export async function getCondition(conditionId: number): Promise<FarmConditionResponse> {
  const { data } = await apiClient.get<FarmConditionResponse>(`/conditions/${conditionId}`);
  return data;
}

export async function updateCondition(conditionId: number, payload: FarmConditionUpdate): Promise<FarmConditionResponse> {
  const { data } = await apiClient.put<FarmConditionResponse>(`/conditions/${conditionId}`, payload);
  return data;
}

export async function deleteCondition(conditionId: number): Promise<void> {
  await apiClient.delete(`/conditions/${conditionId}`);
}
