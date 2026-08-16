import { useState, type FormEvent } from 'react';
import type { FarmCreate, FarmResponse } from '../../types';
import { FormInput } from '../../components/ui/FormInput';
import { Select } from '../../components/ui/Select';
import { normalizeError, type ApiError } from '../../api/client';
import { fieldError } from '../../utils/errors';

const LAND_UNITS = [
  { value: 'acres', label: 'Acres' },
  { value: 'hectares', label: 'Hectares' },
  { value: 'bigha', label: 'Bigha' },
];

export function FarmForm({
  initial,
  onSubmit,
  submitLabel = 'Save Farm',
}: {
  initial?: Partial<FarmResponse>;
  onSubmit: (payload: FarmCreate) => Promise<void>;
  submitLabel?: string;
}) {
  const [form, setForm] = useState<FarmCreate>({
    farm_name: initial?.farm_name ?? '',
    location: initial?.location ?? '',
    village: initial?.village ?? '',
    district: initial?.district ?? '',
    state: initial?.state ?? '',
    land_area: initial?.land_area ?? 0,
    land_unit: initial?.land_unit ?? 'acres',
    soil_type: initial?.soil_type ?? '',
    irrigation_type: initial?.irrigation_type ?? '',
    current_crop: initial?.current_crop ?? '',
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);

  function update<K extends keyof FarmCreate>(key: K, value: FarmCreate[K]) {
    setForm((f) => ({ ...f, [key]: value }));
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    if (form.land_area <= 0) {
      setError({ status: null, message: 'Land area must be a positive number.' });
      return;
    }
    setIsLoading(true);
    try {
      await onSubmit(form);
    } catch (err) {
      setError(normalizeError(err));
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      <FormInput
        label="Farm name"
        required
        value={form.farm_name}
        onChange={(e) => update('farm_name', e.target.value)}
        error={fieldError(error, 'farm_name')}
      />
      <div className="grid gap-4 sm:grid-cols-2">
        <FormInput
          label="Land area"
          type="number"
          step="any"
          min={0.01}
          required
          value={form.land_area || ''}
          onChange={(e) => update('land_area', Number(e.target.value))}
          error={fieldError(error, 'land_area')}
        />
        <Select
          label="Land unit"
          options={LAND_UNITS}
          value={form.land_unit}
          onChange={(e) => update('land_unit', e.target.value)}
        />
      </div>
      <FormInput
        label="Location"
        value={form.location ?? ''}
        onChange={(e) => update('location', e.target.value)}
        error={fieldError(error, 'location')}
      />
      <div className="grid gap-4 sm:grid-cols-3">
        <FormInput label="Village" value={form.village ?? ''} onChange={(e) => update('village', e.target.value)} />
        <FormInput label="District" value={form.district ?? ''} onChange={(e) => update('district', e.target.value)} />
        <FormInput label="State" value={form.state ?? ''} onChange={(e) => update('state', e.target.value)} />
      </div>
      <div className="grid gap-4 sm:grid-cols-3">
        <FormInput label="Soil type" value={form.soil_type ?? ''} onChange={(e) => update('soil_type', e.target.value)} />
        <FormInput
          label="Irrigation type"
          value={form.irrigation_type ?? ''}
          onChange={(e) => update('irrigation_type', e.target.value)}
        />
        <FormInput
          label="Current crop"
          value={form.current_crop ?? ''}
          onChange={(e) => update('current_crop', e.target.value)}
        />
      </div>
      {error && !error.fieldErrors && <p className="text-sm text-red-600">{error.message}</p>}
      <button
        type="submit"
        disabled={isLoading}
        className="mt-1 rounded-lg bg-primary-600 py-2.5 text-sm font-medium text-white hover:bg-primary-700 disabled:opacity-60"
      >
        {isLoading ? 'Saving…' : submitLabel}
      </button>
    </form>
  );
}
