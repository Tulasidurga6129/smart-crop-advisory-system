import apiClient from './client';
import type { YieldPredictionRequest, YieldPredictionResponse } from '../types';

// This endpoint has no auth requirement in the OpenAPI spec — it works
// whether or not the user is logged in.
export async function predictYield(payload: YieldPredictionRequest): Promise<YieldPredictionResponse> {
  const { data } = await apiClient.post<YieldPredictionResponse>('/yield-prediction/predict', payload);
  return data;
}
