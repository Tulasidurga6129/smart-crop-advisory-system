import apiClient from './client';
import type { YieldPredictionResponse } from '../types';

// GET /yield-predictions/crop/{crop_id} — authenticated (JWT attached
// automatically by the apiClient request interceptor, see api/client.ts).
// The backend derives crop year, season, farm state, crop area, and all
// weather/climate values itself; we only ever send the crop_id.
export async function getYieldPrediction(cropId: number): Promise<YieldPredictionResponse> {
  const { data } = await apiClient.get<YieldPredictionResponse>(`/yield-predictions/crop/${cropId}`);
  return data;
}
