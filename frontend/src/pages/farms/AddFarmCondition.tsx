import { useState, type FormEvent } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { createFarmCondition } from '../../api/conditions';
import { FormInput } from '../../components/ui/FormInput';
import { normalizeError, type ApiError } from '../../api/client';
import type { FarmConditionCreate } from '../../types';

const FIELDS: { key: keyof FarmConditionCreate; label: string; min?: number; max?: number }[] = [
  { key: 'soil_ph', label: 'Soil pH', min: 0, max: 14 },
  { key: 'nitrogen', label: 'Nitrogen', min: 0 },
  { key: 'phosphorus', label: 'Phosphorus', min: 0 },
  { key: 'potassium', label: 'Potassium', min: 0 },
  { key: 'organic_matter', label: 'Organic Matter', min: 0 },
  { key: 'soil_moisture', label: 'Soil Moisture (%)', min: 0, max: 100 },
  { key: 'temperature', label: 'Temperature (°C)' },
  { key: 'humidity', label: 'Humidity (%)', min: 0, max: 100 },
  { key: 'rainfall', label: 'Rainfall (mm)', min: 0 },
  { key: 'sunlight', label: 'Sunlight', min: 0 },
];

export function AddFarmCondition() {
  const { farmId } = useParams();
  const navigate = useNavigate();
  const [form, setForm] = useState<FarmConditionCreate>({});
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (!farmId) return;
    setError(null);
    setIsLoading(true);
    try {
      await createFarmCondition(Number(farmId), form);
      navigate(`/farms/${farmId}`);
    } catch (err) {
      setError(normalizeError(err));
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-2xl">
      <h1 className="mb-6 text-2xl font-semibold text-gray-900">Log Soil Conditions</h1>
      <form onSubmit={handleSubmit} className="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm">
        <div className="grid gap-4 sm:grid-cols-2">
          {FIELDS.map(({ key, label, min, max }) => (
            <FormInput
              key={key}
              label={label}
              type="number"
              step="any"
              min={min}
              max={max}
              value={(form[key] as number | undefined) ?? ''}
              onChange={(e) =>
                setForm((f) => ({ ...f, [key]: e.target.value === '' ? undefined : Number(e.target.value) }))
              }
            />
          ))}
        </div>
        {error && <p className="mt-4 text-sm text-red-600">{error.message}</p>}
        <button
          type="submit"
          disabled={isLoading}
          className="mt-5 rounded-lg bg-primary-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-primary-700 disabled:opacity-60"
        >
          {isLoading ? 'Saving…' : 'Save Conditions'}
        </button>
      </form>
    </div>
  );
}
