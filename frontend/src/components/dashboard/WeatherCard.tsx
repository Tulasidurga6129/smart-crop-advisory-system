import { CloudRain, Droplets, Thermometer, Wind } from 'lucide-react';
import type { DashboardWeatherResponse, WeatherResponse } from '../../types';

export function WeatherCard({ weather }: { weather: DashboardWeatherResponse | WeatherResponse | null }) {
  if (!weather) {
    return (
      <div className="rounded-2xl border border-gray-100 bg-white p-5 text-center text-sm text-gray-400 shadow-sm">
        No weather logged for this farm yet.
      </div>
    );
  }

  const date = 'observed_at' in weather && weather.observed_at ? weather.observed_at : undefined;

  return (
    <div className="rounded-2xl border border-gray-100 bg-gradient-to-br from-sky-50 to-white p-5 shadow-sm">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-gray-400">Latest weather</p>
          <p className="text-2xl font-semibold text-gray-900">
            {weather.temperature != null ? `${weather.temperature}°C` : '—'}
          </p>
          {weather.weather_condition && <p className="text-sm text-gray-500">{weather.weather_condition}</p>}
        </div>
        <CloudRain className="h-10 w-10 text-sky-400" />
      </div>
      <div className="mt-4 grid grid-cols-3 gap-3 text-xs text-gray-600">
        <div className="flex flex-col items-center gap-1 rounded-lg bg-white/70 py-2">
          <Droplets className="h-4 w-4 text-sky-500" />
          {weather.humidity != null ? `${weather.humidity}%` : '—'}
          <span className="text-[10px] text-gray-400">Humidity</span>
        </div>
        <div className="flex flex-col items-center gap-1 rounded-lg bg-white/70 py-2">
          <CloudRain className="h-4 w-4 text-sky-500" />
          {weather.rainfall != null ? `${weather.rainfall}mm` : '—'}
          <span className="text-[10px] text-gray-400">Rainfall</span>
        </div>
        <div className="flex flex-col items-center gap-1 rounded-lg bg-white/70 py-2">
          <Wind className="h-4 w-4 text-sky-500" />
          {weather.wind_speed != null ? `${weather.wind_speed}` : '—'}
          <span className="text-[10px] text-gray-400">Wind</span>
        </div>
      </div>
      {date && <p className="mt-3 text-right text-[11px] text-gray-400">{new Date(date).toLocaleString()}</p>}
      {!date && <Thermometer className="hidden" />}
    </div>
  );
}
