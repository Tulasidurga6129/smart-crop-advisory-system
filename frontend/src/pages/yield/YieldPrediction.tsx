import { useState, type FormEvent } from 'react';
import { Wheat } from 'lucide-react';
import { predictYield } from '../../api/yieldPrediction';
import type { YieldPredictionRequest, YieldPredictionResponse } from '../../types';
import { FormInput } from '../../components/ui/FormInput';
import { LoadingSpinner } from '../../components/ui/LoadingSpinner';
import { ErrorMessage } from '../../components/ui/ErrorMessage';
import { PredictionResult } from '../../components/dashboard/PredictionResult';
import { normalizeError, type ApiError } from '../../api/client';
import { fieldError } from '../../utils/errors';

const SEASON_OPTIONS = ['Kharif', 'Rabi', 'Whole Year', 'Summer', 'Winter', 'Autumn'];

const initialForm: YieldPredictionRequest = {
  crop: '',
  crop_year: new Date().getFullYear(),
  season: 'Kharif',
  state: '',
  area: 0,
  annual_rainfall: 0,
  fertilizer: 0,
  pesticide: 0,
  avg_temperature: 0,
  max_temperature: 0,
  min_temperature: 0,
};

export function YieldPrediction() {
  const [form, setForm] = useState<YieldPredictionRequest>(initialForm);
  const [result, setResult] = useState<YieldPredictionResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);

  function update<K extends keyof YieldPredictionRequest>(key: K, value: YieldPredictionRequest[K]) {
    setForm((f) => ({ ...f, [key]: value }));
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setResult(null);
    setIsLoading(true);
    try {
      const res = await predictYield(form);
      setResult(res);
    } catch (err) {
      setError(normalizeError(err));
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="mx-auto flex max-w-3xl flex-col gap-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Yield Prediction</h1>
        <p className="text-sm text-gray-500">Estimate crop yield using the backend's prediction model.</p>
      </div>

      <form onSubmit={handleSubmit} className="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm">
        <div className="grid gap-4 sm:grid-cols-2">
          <FormInput
            label="Crop"
            required
            value={form.crop}
            onChange={(e) => update('crop', e.target.value)}
            error={fieldError(error, 'crop')}
          />
          <div className="flex flex-col gap-1">
            <label className="text-sm font-medium text-gray-700">
              Season<span className="text-red-500"> *</span>
            </label>
            <select
              required
              value={form.season}
              onChange={(e) => update('season', e.target.value)}
              className="rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm outline-none focus:border-primary-500 focus:ring-2 focus:ring-primary-200"
            >
              {SEASON_OPTIONS.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
          </div>
          <FormInput
            label="Crop year"
            type="number"
            required
            value={form.crop_year}
            onChange={(e) => update('crop_year', Number(e.target.value))}
            error={fieldError(error, 'crop_year')}
          />
          <FormInput
            label="State"
            required
            value={form.state}
            onChange={(e) => update('state', e.target.value)}
            error={fieldError(error, 'state')}
          />
          <FormInput
            label="Area (hectares)"
            type="number"
            step="any"
            min={0.01}
            required
            value={form.area || ''}
            onChange={(e) => update('area', Number(e.target.value))}
            error={fieldError(error, 'area')}
          />
          <FormInput
            label="Annual rainfall (mm)"
            type="number"
            step="any"
            min={0}
            required
            value={form.annual_rainfall || ''}
            onChange={(e) => update('annual_rainfall', Number(e.target.value))}
            error={fieldError(error, 'annual_rainfall')}
          />
          <FormInput
            label="Fertilizer (kg)"
            type="number"
            step="any"
            min={0}
            required
            value={form.fertilizer || ''}
            onChange={(e) => update('fertilizer', Number(e.target.value))}
            error={fieldError(error, 'fertilizer')}
          />
          <FormInput
            label="Pesticide (kg)"
            type="number"
            step="any"
            min={0}
            required
            value={form.pesticide || ''}
            onChange={(e) => update('pesticide', Number(e.target.value))}
            error={fieldError(error, 'pesticide')}
          />
          <FormInput
            label="Avg temperature (°C)"
            type="number"
            step="any"
            required
            value={form.avg_temperature || ''}
            onChange={(e) => update('avg_temperature', Number(e.target.value))}
            error={fieldError(error, 'avg_temperature')}
          />
          <FormInput
            label="Max temperature (°C)"
            type="number"
            step="any"
            required
            value={form.max_temperature || ''}
            onChange={(e) => update('max_temperature', Number(e.target.value))}
            error={fieldError(error, 'max_temperature')}
          />
          <FormInput
            label="Min temperature (°C)"
            type="number"
            step="any"
            required
            value={form.min_temperature || ''}
            onChange={(e) => update('min_temperature', Number(e.target.value))}
            error={fieldError(error, 'min_temperature')}
          />
        </div>
        {error && !error.fieldErrors && <p className="mt-4 text-sm text-red-600">{error.message}</p>}
        <button
          type="submit"
          disabled={isLoading}
          className="mt-5 inline-flex items-center justify-center gap-2 rounded-lg bg-earth-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-earth-700 disabled:opacity-60"
        >
          <Wheat className="h-4 w-4" />
          {isLoading ? 'Predicting…' : 'Predict Yield'}
        </button>
      </form>

      {isLoading && <LoadingSpinner label="Running the prediction model…" />}
      {error && error.fieldErrors && <ErrorMessage message={error.message} />}
      {result && <PredictionResult predictedYield={result.predicted_yield} />}
    </div>
  );
}
