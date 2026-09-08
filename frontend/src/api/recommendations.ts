import apiClient from './client';
import type { RecommendationResponseUnknown } from '../types';

/**
 * Generate crop recommendations/advisories for a crop.
 *
 * Backend endpoint:
 * POST /recommendations/{crop_id}
 *
 * The backend returns an array of advisory objects.
 * Authentication is handled automatically by apiClient.
 */
export const generateRecommendations = async (
  cropId: number
): Promise<RecommendationResponseUnknown> => {
  const response = await apiClient.post<RecommendationResponseUnknown>(
    `/recommendations/${cropId}`,
    {}
  );

  return response.data;
};