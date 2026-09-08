import { useState, type FormEvent } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { createCrop } from '../../api/crops';
import { FormInput } from '../../components/ui/FormInput';
import { Select } from '../../components/ui/Select';
import { normalizeError, type ApiError } from '../../api/client';
import { fieldError } from '../../utils/errors';
import { useFarms } from '../../context/FarmContext';
import type { CropCreate } from '../../types';

const STATUS_OPTIONS = [
  { value: 'planned', label: 'Planned' },
  { value: 'active', label: 'Active' },
  { value: 'harvested', label: 'Harvested' },
];

export function AddCrop() {
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const { farms } = useFarms();
  const farmIdParam = params.get('farmId');

  const [form, setForm] = useState<CropCreate>({
    farm_id: farmIdParam ? Number(farmIdParam) : farms[0]?.id ?? 0,
    name: '',
    variety: '',
    season: '',
    sowing_date: null,
    expected_harvest_date: null,
    area: undefined,
    status: 'planned',
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setIsLoading(true);
    try {
      const crop = await createCrop(form);
      navigate(`/crops/${crop.id}`);
    } catch (err) {
      setError(normalizeError(err));
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-2xl">
      <h1 className="mb-6 text-2xl font-semibold text-gray-900">Add Crop</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 rounded-2xl border border-gray-100 bg-white p-6 shadow-sm">
        <Select
          label="Farm"
          required
          options={farms.map((f) => ({ value: String(f.id), label: f.farm_name }))}
          value={form.farm_id || ''}
          onChange={(e) => setForm((f) => ({ ...f, farm_id: Number(e.target.value) }))}
        />
        <FormInput
          label="Crop name"
          required
          value={form.name}
          onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
          error={fieldError(error, 'name')}
        />
        <div className="grid gap-4 sm:grid-cols-2">
          <FormInput
            label="Variety"
            value={form.variety ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, variety: e.target.value }))}
          />
          <FormInput
            label="Season"
            required
            value={form.season}
            onChange={(e) => setForm((f) => ({ ...f, season: e.target.value }))}
            error={fieldError(error, 'season')}
            placeholder="e.g. Kharif, Rabi"
          />
        </div>
        <div className="grid gap-4 sm:grid-cols-2">
          <FormInput
            label="Sowing date"
            type="date"
            value={form.sowing_date ?? ''}
            onChange={(e) =>setForm((f) => ({ ...f, sowing_date: e.target.value || null,}))}
          />
          <FormInput
            label="Expected harvest date"
            type="date"
            value={form.expected_harvest_date ?? ''}
            onChange={(e) =>setForm((f) => ({ ...f, expected_harvest_date: e.target.value || null, }))
}
          />
        </div>
        <div className="grid gap-4 sm:grid-cols-2">
          <FormInput
            label="Area"
            type="number"
            step="any"
            min={0.01}
            value={form.area ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, area: e.target.value === '' ? undefined : Number(e.target.value) }))}
            error={fieldError(error, 'area')}
          />
          <Select
            label="Status"
            options={STATUS_OPTIONS}
            value={form.status}
            onChange={(e) => setForm((f) => ({ ...f, status: e.target.value }))}
          />
        </div>
        {error && !error.fieldErrors && <p className="text-sm text-red-600">{error.message}</p>}
        <button
          type="submit"
          disabled={isLoading || !form.farm_id}
          className="mt-1 rounded-lg bg-primary-600 py-2.5 text-sm font-medium text-white hover:bg-primary-700 disabled:opacity-60"
        >
          {isLoading ? 'Saving…' : 'Add Crop'}
        </button>
      </form>
    </div>
  );
}
