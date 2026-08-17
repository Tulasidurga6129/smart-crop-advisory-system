import apiClient from './client';
import type {
  WeatherCreate,
  WeatherUpdate,
  WeatherResponse,
  TomorrowWeatherResponse,
} from '../types';

export async function getFarmWeather(farmId: number): Promise<WeatherResponse[]> {
  const { data } = await apiClient.get<WeatherResponse[]>(`/weather/farm/${farmId}`);
  return data;
}
export async function syncFarmWeather(farmId: number): Promise<WeatherResponse> {
  const { data } = await apiClient.post<WeatherResponse>(
    `/weather/farm/${farmId}/sync`
  );
  return data;
}
export async function getTomorrowWeather(
  farmId: number
): Promise<TomorrowWeatherResponse> {
  const { data } = await apiClient.get<TomorrowWeatherResponse>(
    `/weather/farm/${farmId}/tomorrow`
  );

  return data;
}

export async function createFarmWeather(farmId: number, payload: WeatherCreate): Promise<WeatherResponse> {
  const { data } = await apiClient.post<WeatherResponse>(`/weather/farm/${farmId}`, payload);
  return data;
}

export async function getWeather(weatherId: number): Promise<WeatherResponse> {
  const { data } = await apiClient.get<WeatherResponse>(`/weather/${weatherId}`);
  return data;
}

export async function updateWeather(weatherId: number, payload: WeatherUpdate): Promise<WeatherResponse> {
  const { data } = await apiClient.put<WeatherResponse>(`/weather/${weatherId}`, payload);
  return data;
}

export async function deleteWeather(weatherId: number): Promise<void> {
  await apiClient.delete(`/weather/${weatherId}`);
}
