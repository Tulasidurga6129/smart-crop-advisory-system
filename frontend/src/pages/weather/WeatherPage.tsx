import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Plus,
  CloudSun,
  CloudRain,
  Droplets,
  Thermometer,
  Umbrella,
} from 'lucide-react';

import { useFarms } from '../../context/FarmContext';
import {
  getFarmWeather,
  getTomorrowWeather,
  type TomorrowWeatherResponse,
} from '../../api/weather';

import type { WeatherResponse } from '../../types';

import { LoadingSpinner } from '../../components/ui/LoadingSpinner';
import { ErrorMessage } from '../../components/ui/ErrorMessage';
import { EmptyState } from '../../components/ui/EmptyState';
import { WeatherCard } from '../../components/dashboard/WeatherCard';
import { normalizeError } from '../../api/client';

export function WeatherPage() {
  const { selectedFarmId, farms } = useFarms();

  const [records, setRecords] = useState<WeatherResponse[]>([]);
  const [tomorrowWeather, setTomorrowWeather] =
    useState<TomorrowWeatherResponse | null>(null);

  const [isLoading, setIsLoading] = useState(false);
  const [isTomorrowLoading, setIsTomorrowLoading] = useState(false);

  const [error, setError] = useState<string | null>(null);
  const [tomorrowError, setTomorrowError] = useState<string | null>(null);

  async function load() {
    if (!selectedFarmId) return;

    setIsLoading(true);
    setError(null);

    try {
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
    } catch (err) {
      setError(normalizeError(err).message);
    } finally {
      setIsLoading(false);
    }
  }

  async function loadTomorrowWeather() {
    if (!selectedFarmId) return;

    setIsTomorrowLoading(true);
    setTomorrowError(null);

    try {
      const data = await getTomorrowWeather(selectedFarmId);
      setTomorrowWeather(data);
    } catch (err) {
      setTomorrowError(normalizeError(err).message);
      setTomorrowWeather(null);
    } finally {
      setIsTomorrowLoading(false);
    }
  }

  useEffect(() => {
    load();
    loadTomorrowWeather();

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedFarmId]);

  if (farms.length === 0) {
    return (
      <EmptyState
        icon={CloudSun}
        title="Add a farm first"
        description="Weather logs are tied to a specific farm."
      />
    );
  }

  return (
    <div className="flex flex-col gap-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">
            Weather
          </h1>

          <p className="mt-1 text-sm text-gray-500">
            Current conditions and tomorrow's forecast for your farm.
          </p>
        </div>

        <Link
          to={`/farms/${selectedFarmId}/weather/new`}
          className="inline-flex items-center gap-1.5 rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700"
        >
          <Plus className="h-4 w-4" />
          Log Weather
        </Link>
      </div>

      {/* Tomorrow Weather */}
      <section className="rounded-2xl border border-primary-100 bg-primary-50/40 p-5 shadow-sm">
        <div className="mb-4 flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-gray-900">
              Tomorrow's Weather
            </h2>

            <p className="text-sm text-gray-500">
              Forecast used for future-aware irrigation recommendations.
            </p>
          </div>

          <CloudRain className="h-7 w-7 text-primary-600" />
        </div>

        {isTomorrowLoading ? (
          <LoadingSpinner size="lg" />
        ) : tomorrowError ? (
          <div className="rounded-lg border border-red-100 bg-red-50 p-4">
            <p className="text-sm font-medium text-red-700">
              Unable to load tomorrow's weather.
            </p>

            <p className="mt-1 text-xs text-red-600">
              {tomorrowError}
            </p>

            <button
              onClick={loadTomorrowWeather}
              className="mt-3 rounded-lg bg-red-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-red-700"
            >
              Retry
            </button>
          </div>
        ) : tomorrowWeather ? (
          <>
            <div className="mb-4 rounded-xl bg-white p-4">
              <p className="text-sm font-medium text-gray-900">
                {new Date(
                  `${tomorrowWeather.date}T00:00:00`
                ).toLocaleDateString(undefined, {
                  weekday: 'long',
                  month: 'short',
                  day: 'numeric',
                  year: 'numeric',
                })}
              </p>

              <p className="mt-1 text-sm text-gray-500">
                {tomorrowWeather.weather_condition}
              </p>
            </div>

            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
              {/* Temperature */}
              <div className="rounded-xl bg-white p-4 shadow-sm">
                <div className="flex items-center gap-2">
                  <Thermometer className="h-5 w-5 text-orange-500" />

                  <p className="text-xs font-medium text-gray-500">
                    Temperature
                  </p>
                </div>

                <p className="mt-2 text-lg font-semibold text-gray-900">
                  {tomorrowWeather.temperature_min}°C –{' '}
                  {tomorrowWeather.temperature_max}°C
                </p>
              </div>

              {/* Rainfall */}
              <div className="rounded-xl bg-white p-4 shadow-sm">
                <div className="flex items-center gap-2">
                  <CloudRain className="h-5 w-5 text-blue-500" />

                  <p className="text-xs font-medium text-gray-500">
                    Rainfall
                  </p>
                </div>

                <p className="mt-2 text-lg font-semibold text-gray-900">
                  {tomorrowWeather.rainfall.toFixed(1)} mm
                </p>
              </div>

              {/* Rain probability */}
              <div className="rounded-xl bg-white p-4 shadow-sm">
                <div className="flex items-center gap-2">
                  <Umbrella className="h-5 w-5 text-primary-600" />

                  <p className="text-xs font-medium text-gray-500">
                    Rain Probability
                  </p>
                </div>

                <p className="mt-2 text-lg font-semibold text-gray-900">
                  {tomorrowWeather.precipitation_probability != null
                    ? `${tomorrowWeather.precipitation_probability}%`
                    : '—'}
                </p>
              </div>

              {/* Humidity */}
              <div className="rounded-xl bg-white p-4 shadow-sm">
                <div className="flex items-center gap-2">
                  <Droplets className="h-5 w-5 text-cyan-500" />

                  <p className="text-xs font-medium text-gray-500">
                    Humidity
                  </p>
                </div>

                <p className="mt-2 text-lg font-semibold text-gray-900">
                  {tomorrowWeather.humidity != null
                    ? `${tomorrowWeather.humidity.toFixed(0)}%`
                    : '—'}
                </p>
              </div>

              {/* Condition */}
              <div className="rounded-xl bg-white p-4 shadow-sm">
                <div className="flex items-center gap-2">
                  <CloudSun className="h-5 w-5 text-yellow-500" />

                  <p className="text-xs font-medium text-gray-500">
                    Condition
                  </p>
                </div>

                <p className="mt-2 text-sm font-semibold text-gray-900">
                  {tomorrowWeather.weather_condition}
                </p>
              </div>
            </div>
          </>
        ) : (
          <div className="rounded-lg bg-white p-4">
            <p className="text-sm text-gray-500">
              Tomorrow's weather forecast is not available.
            </p>
          </div>
        )}
      </section>

      {/* Current / Logged Weather */}
      <section>
        <div className="mb-4">
          <h2 className="text-lg font-semibold text-gray-900">
            Current & Logged Weather
          </h2>

          <p className="text-sm text-gray-500">
            Weather readings recorded for this farm.
          </p>
        </div>

        {isLoading ? (
          <LoadingSpinner size="lg" />
        ) : error ? (
          <ErrorMessage message={error} onRetry={load} />
        ) : records.length === 0 ? (
          <EmptyState
            icon={CloudSun}
            title="No weather logged yet"
            description="Add a reading to start tracking conditions on this farm."
          />
        ) : (
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
                    Rainfall: {w.rainfall ?? '—'}mm
                  </p>

                  <p>
                    Wind: {w.wind_speed ?? '—'}
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
        )}
      </section>
    </div>
  );
}