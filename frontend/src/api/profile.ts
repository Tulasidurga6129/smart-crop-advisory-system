import apiClient from './client';
import type { FarmerProfileCreate, FarmerProfileUpdate, FarmerProfileResponse } from '../types';

export async function getMyProfile(): Promise<FarmerProfileResponse> {
  const { data } = await apiClient.get<FarmerProfileResponse>('/api/v1/users/me/profile');
  return data;
}

export async function createMyProfile(payload: FarmerProfileCreate): Promise<FarmerProfileResponse> {
  const { data } = await apiClient.post<FarmerProfileResponse>('/api/v1/users/me/profile', payload);
  return data;
}

export async function updateMyProfile(payload: FarmerProfileUpdate): Promise<FarmerProfileResponse> {
  const { data } = await apiClient.put<FarmerProfileResponse>('/api/v1/users/me/profile', payload);
  return data;
}
