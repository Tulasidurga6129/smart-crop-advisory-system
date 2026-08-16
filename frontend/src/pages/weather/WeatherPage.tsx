import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Plus, CloudSun } from 'lucide-react';
import { useFarms } from '../../context/FarmContext';
import { getFarmWeather } from '../../api/weather';
import type { WeatherResponse } from '../../types';
import { LoadingSpinner } from '../../components/ui/LoadingSpinner';
import { ErrorMessage } from '../../components/ui/ErrorMessage';
import { EmptyState } from '../../components/ui/EmptyState';
import { WeatherCard } from '../../components/dashboard/WeatherCard';
import { normalizeError } from '../../api/client';

export function WeatherPage() {
  const { selectedFarmId, farms } = useFarms();
  const [records, setRecords] = useState<WeatherResponse[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    if (!selectedFarmId) return;
    setIsLoading(true);
    setError(null);
    try {
      const data = await getFarmWeather(selectedFarmId);
      setRecords(data.slice().sort((a, b) => (b.observed_at || b.created_at).localeCompare(a.observed_at || a.created_at)));
    } catch (err) {
      setError(normalizeError(err).message);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedFarmId]);

  if (farms.length === 0) {
    return <EmptyState icon={CloudSun} title="Add a farm first" description="Weather logs are tied to a specific farm." />;
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Weather</h1>
        <Link
          to={`/farms/${selectedFarmId}/weather/new`}
          className="inline-flex items-center gap-1.5 rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700"
        >
          <Plus className="h-4 w-4" /> Log Weather
        </Link>
      </div>

      {isLoading ? (
        <LoadingSpinner size="lg" />
      ) : error ? (
        <ErrorMessage message={error} onRetry={load} />
      ) : records.length === 0 ? (
        <EmptyState icon={CloudSun} title="No weather logged yet" description="Add a reading to start tracking conditions on this farm." />
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <WeatherCard weather={records[0]} />
          {records.slice(1).map((w) => (
            <div key={w.id} className="rounded-xl border border-gray-100 bg-white p-4 shadow-sm">
              <p className="mb-2 text-xs text-gray-400">
                {w.observed_at ? new Date(w.observed_at).toLocaleString() : new Date(w.created_at).toLocaleString()}
              </p>
              <div className="grid grid-cols-2 gap-2 text-sm">
                <p>Temp: {w.temperature ?? '—'}°C</p>
                <p>Humidity: {w.humidity ?? '—'}%</p>
                <p>Rainfall: {w.rainfall ?? '—'}mm</p>
                <p>Wind: {w.wind_speed ?? '—'}</p>
              </div>
              {w.weather_condition && <p className="mt-2 text-sm text-gray-500">{w.weather_condition}</p>}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
