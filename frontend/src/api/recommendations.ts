import apiClient from './client';
import type { RecommendationResponseUnknown } from '../types';

// POST /recommendations/{crop_id} takes no request body — the backend
// derives the recommendation from the crop_id alone. Response schema is not
// declared in the OpenAPI spec, so we treat it as an arbitrary JSON object
// and render it defensively (see RecommendationCard component).
export async function generateCropRecommendations(cropId: number): Promise<RecommendationResponseUnknown> {
  const { data } = await apiClient.post<RecommendationResponseUnknown>(`/recommendations/${cropId}`);
  return data;
}
