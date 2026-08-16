import { useState, type FormEvent } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { createFarmWeather } from '../../api/weather';
import { FormInput } from '../../components/ui/FormInput';
import { normalizeError, type ApiError } from '../../api/client';
import type { WeatherCreate } from '../../types';

export function AddWeather() {
  const { farmId } = useParams();
  const navigate = useNavigate();
  const [form, setForm] = useState<WeatherCreate>({});
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (!farmId) return;
    setError(null);
    setIsLoading(true);
    try {
      await createFarmWeather(Number(farmId), form);
      navigate(`/farms/${farmId}`);
    } catch (err) {
      setError(normalizeError(err));
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-2xl">
      <h1 className="mb-6 text-2xl font-semibold text-gray-900">Log Weather</h1>
      <form onSubmit={handleSubmit} className="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm">
        <div className="grid gap-4 sm:grid-cols-2">
          <FormInput
            label="Temperature (°C)"
            type="number"
            step="any"
            value={form.temperature ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, temperature: e.target.value === '' ? undefined : Number(e.target.value) }))}
          />
          <FormInput
            label="Humidity (%)"
            type="number"
            step="any"
            min={0}
            max={100}
            value={form.humidity ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, humidity: e.target.value === '' ? undefined : Number(e.target.value) }))}
          />
          <FormInput
            label="Rainfall (mm)"
            type="number"
            step="any"
            min={0}
            value={form.rainfall ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, rainfall: e.target.value === '' ? undefined : Number(e.target.value) }))}
          />
          <FormInput
            label="Wind speed"
            type="number"
            step="any"
            min={0}
            value={form.wind_speed ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, wind_speed: e.target.value === '' ? undefined : Number(e.target.value) }))}
          />
          <FormInput
            label="Weather condition"
            value={form.weather_condition ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, weather_condition: e.target.value }))}
          />
          <FormInput
            label="Observed at"
            type="datetime-local"
            value={form.observed_at ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, observed_at: e.target.value }))}
          />
        </div>
        {error && <p className="mt-4 text-sm text-red-600">{error.message}</p>}
        <button
          type="submit"
          disabled={isLoading}
          className="mt-5 rounded-lg bg-primary-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-primary-700 disabled:opacity-60"
        >
          {isLoading ? 'Saving…' : 'Save Weather'}
        </button>
      </form>
    </div>
  );
}
