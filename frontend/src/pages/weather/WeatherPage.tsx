import { useEffect, useState } from 'react';
import { CloudSun } from 'lucide-react';
import { useFarms } from '../../context/FarmContext';
import {
  getFarmWeather,
  syncFarmWeather,
  getTomorrowWeather,
} from '../../api/weather';
import type {
  WeatherResponse,
  TomorrowWeatherResponse,
} from '../../types';
import { LoadingSpinner } from '../../components/ui/LoadingSpinner';
import { ErrorMessage } from '../../components/ui/ErrorMessage';
import { EmptyState } from '../../components/ui/EmptyState';
import { WeatherCard } from '../../components/dashboard/WeatherCard';
import { normalizeError } from '../../api/client';

export function WeatherPage() {
  const { selectedFarmId, farms } = useFarms();

  const [records, setRecords] = useState<WeatherResponse[]>([]);
  const [tomorrowForecast, setTomorrowForecast] =
    useState<TomorrowWeatherResponse | null>(null);

  const [isLoading, setIsLoading] = useState(false);
  const [isTomorrowLoading, setIsTomorrowLoading] = useState(false);

  const [error, setError] = useState<string | null>(null);
  const [tomorrowError, setTomorrowError] =
    useState<string | null>(null);

  async function load() {
    if (!selectedFarmId) return;

    setIsLoading(true);
    setError(null);

    try {
      // Existing current-weather functionality
      await syncFarmWeather(selectedFarmId);

      const data = await getFarmWeather(selectedFarmId);

      setRecords(
        data
          .slice()
          .sort((a, b) =>
            (b.observed_at || b.created_at).localeCompare(
              a.observed_at || a.created_at
            )
          )
      );

      // Tomorrow's forecast
      setIsTomorrowLoading(true);
      setTomorrowError(null);

      const forecast = await getTomorrowWeather(selectedFarmId);

      setTomorrowForecast(forecast);
    } catch (err) {
      setError(normalizeError(err).message);
      setTomorrowForecast(null);
    } finally {
      setIsLoading(false);
      setIsTomorrowLoading(false);
    }
  }

  useEffect(() => {
    load();

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedFarmId]);

  if (farms.length === 0) {
    return (
      <EmptyState
        icon={CloudSun}
        title="Add a farm first"
        description="Weather data is tied to a specific farm."
      />
    );
  }

  return (
    <div className="flex flex-col gap-6">
      {/* Page Header */}
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">
          Weather
        </h1>

        <p className="mt-1 text-sm text-gray-500">
          Current weather and tomorrow's forecast for your farm.
        </p>
      </div>

      {/* Current Weather */}
      {isLoading ? (
        <LoadingSpinner size="lg" />
      ) : error ? (
        <ErrorMessage
          message={error}
          onRetry={load}
        />
      ) : records.length === 0 ? (
        <EmptyState
          icon={CloudSun}
          title="No weather data available"
          description="Weather data could not be retrieved for this farm."
        />
      ) : (
        <div>
          <h2 className="mb-3 text-lg font-semibold text-gray-900">
            Current Weather
          </h2>

          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <WeatherCard weather={records[0]} />

            {records.slice(1).map((w) => (
              <div
                key={w.id}
                className="rounded-xl border border-gray-100 bg-white p-4 shadow-sm"
              >
                <p className="mb-2 text-xs text-gray-400">
                  {w.observed_at
                    ? new Date(w.observed_at).toLocaleString()
                    : new Date(w.created_at).toLocaleString()}
                </p>

                <div className="grid grid-cols-2 gap-2 text-sm">
                  <p>
                    Temp: {w.temperature ?? '—'}°C
                  </p>

                  <p>
                    Humidity: {w.humidity ?? '—'}%
                  </p>

                  <p>
                    Rainfall: {w.rainfall ?? '—'} mm
                  </p>

                  <p>
                    Wind: {w.wind_speed ?? '—'} km/h
                  </p>
                </div>

                {w.weather_condition && (
                  <p className="mt-2 text-sm text-gray-500">
                    {w.weather_condition}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tomorrow's Weather */}
      <div>
        <h2 className="mb-3 text-lg font-semibold text-gray-900">
          Tomorrow's Weather
        </h2>

        {isTomorrowLoading ? (
          <LoadingSpinner size="lg" />
        ) : tomorrowError ? (
          <ErrorMessage
            message={tomorrowError}
            onRetry={load}
          />
        ) : tomorrowForecast ? (
          <div className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
            <div className="mb-4">
              <p className="text-sm text-gray-500">
                {new Date(
                  `${tomorrowForecast.date}T00:00:00`
                ).toLocaleDateString(undefined, {
                  weekday: 'long',
                  day: 'numeric',
                  month: 'long',
                  year: 'numeric',
                })}
              </p>

              <p className="mt-1 text-xl font-semibold text-gray-900">
                {tomorrowForecast.weather_condition}
              </p>
            </div>

            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
              <div>
                <p className="text-xs text-gray-500">
                  Temperature
                </p>

                <p className="mt-1 text-sm font-medium">
                  {tomorrowForecast.temperature_min ?? '—'}°C
                  {' – '}
                  {tomorrowForecast.temperature_max ?? '—'}°C
                </p>
              </div>

              <div>
                <p className="text-xs text-gray-500">
                  Humidity
                </p>

                <p className="mt-1 text-sm font-medium">
                  {tomorrowForecast.humidity ?? '—'}%
                </p>
              </div>

              <div>
                <p className="text-xs text-gray-500">
                  Rainfall
                </p>

                <p className="mt-1 text-sm font-medium">
                  {tomorrowForecast.rainfall ?? '—'} mm
                </p>
              </div>

              <div>
                <p className="text-xs text-gray-500">
                  Rain Probability
                </p>

                <p className="mt-1 text-sm font-medium">
                  {tomorrowForecast.precipitation_probability ?? '—'}%
                </p>
              </div>

              <div>
                <p className="text-xs text-gray-500">
                  Forecast
                </p>

                <p className="mt-1 text-sm font-medium">
                  {tomorrowForecast.weather_condition}
                </p>
              </div>
            </div>
          </div>
        ) : (
          <div className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
            <p className="text-sm text-gray-500">
              Tomorrow's forecast is not available.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}