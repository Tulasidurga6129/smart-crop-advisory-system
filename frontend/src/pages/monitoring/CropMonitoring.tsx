import { useEffect, useState, type FormEvent } from 'react';
import { useSearchParams } from 'react-router-dom';
import { LineChart, Plus } from 'lucide-react';
import { useFarms } from '../../context/FarmContext';
import { getFarmCrops } from '../../api/crops';
import { getCropMonitoringRecords, createMonitoring } from '../../api/monitoring';
import type { CropResponse, CropMonitoringResponse, CropMonitoringCreate } from '../../types';
import { Select } from '../../components/ui/Select';
import { FormInput, FormTextarea } from '../../components/ui/FormInput';
import { LoadingSpinner } from '../../components/ui/LoadingSpinner';
import { ErrorMessage } from '../../components/ui/ErrorMessage';
import { EmptyState } from '../../components/ui/EmptyState';
import { Modal } from '../../components/ui/Modal';
import { normalizeError, type ApiError } from '../../api/client';

export function CropMonitoring() {
  const { selectedFarmId, farms } = useFarms();
  const [params] = useSearchParams();
  const [crops, setCrops] = useState<CropResponse[]>([]);
  const [selectedCropId, setSelectedCropId] = useState<number | null>(
    params.get('cropId') ? Number(params.get('cropId')) : null
  );
  const [records, setRecords] = useState<CropMonitoringResponse[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formOpen, setFormOpen] = useState(false);

  useEffect(() => {
    if (!selectedFarmId) return;
    getFarmCrops(selectedFarmId).then((data) => {
      setCrops(data);
      setSelectedCropId((current) => current ?? data[0]?.id ?? null);
    });
  }, [selectedFarmId]);

  async function load() {
    if (!selectedCropId) return;
    setIsLoading(true);
    setError(null);
    try {
      const data = await getCropMonitoringRecords(selectedCropId);
      setRecords(data.slice().sort((a, b) => b.monitoring_date.localeCompare(a.monitoring_date)));
    } catch (err) {
      setError(normalizeError(err).message);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedCropId]);

  if (farms.length === 0) {
    return <EmptyState icon={LineChart} title="Add a farm and crop first" description="Monitoring records are tied to a crop." />;
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Crop Monitoring</h1>
          <p className="text-sm text-gray-500">Track growth stage and health over time.</p>
        </div>
        <div className="flex items-center gap-3">
          {crops.length > 0 && (
            <Select
              label=""
              options={crops.map((c) => ({ value: String(c.id), label: c.name }))}
              value={selectedCropId ?? ''}
              onChange={(e) => setSelectedCropId(Number(e.target.value))}
              className="min-w-[10rem]"
            />
          )}
          <button
            onClick={() => setFormOpen(true)}
            disabled={!selectedCropId}
            className="inline-flex items-center gap-1.5 rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700 disabled:opacity-50"
          >
            <Plus className="h-4 w-4" /> Add Record
          </button>
        </div>
      </div>

      {isLoading ? (
        <LoadingSpinner size="lg" />
      ) : error ? (
        <ErrorMessage message={error} onRetry={load} />
      ) : records.length === 0 ? (
        <EmptyState icon={LineChart} title="No monitoring records yet" description={crops.length === 0 ? 'Add a crop first.' : undefined} />
      ) : (
        <div className="relative flex flex-col gap-3 border-l-2 border-primary-100 pl-5">
          {records.map((rec) => (
            <div key={rec.id} className="relative rounded-xl border border-gray-100 bg-white p-4 shadow-sm">
              <span className="absolute -left-[27px] top-5 h-3 w-3 rounded-full bg-primary-500" />
              <div className="flex items-center justify-between">
                <p className="font-medium text-gray-900">{rec.growth_stage}</p>
                <p className="text-xs text-gray-400">{new Date(rec.monitoring_date).toLocaleDateString()}</p>
              </div>
              <div className="mt-2 flex flex-wrap gap-3 text-xs text-gray-500">
                {rec.plant_height != null && <span>Height: {rec.plant_height}cm</span>}
                {rec.crop_health && <span>Health: {rec.crop_health}</span>}
                {rec.pest_observed && <span className="text-amber-600">Pest observed</span>}
                {rec.disease_observed && <span className="text-red-600">Disease observed</span>}
              </div>
              {rec.observation_notes && <p className="mt-2 text-sm text-gray-600">{rec.observation_notes}</p>}
            </div>
          ))}
        </div>
      )}

      {selectedCropId && (
        <MonitoringFormModal
          open={formOpen}
          onClose={() => setFormOpen(false)}
          cropId={selectedCropId}
          onCreated={(rec) => {
            setRecords((r) => [rec, ...r]);
            setFormOpen(false);
          }}
        />
      )}
    </div>
  );
}

function MonitoringFormModal({
  open,
  onClose,
  cropId,
  onCreated,
}: {
  open: boolean;
  onClose: () => void;
  cropId: number;
  onCreated: (rec: CropMonitoringResponse) => void;
}) {
  const [form, setForm] = useState<CropMonitoringCreate>({
    crop_id: cropId,
    monitoring_date: new Date().toISOString().slice(0, 10),
    growth_stage: '',
    plant_height: undefined,
    crop_health: '',
    pest_observed: false,
    disease_observed: false,
    observation_notes: '',
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);

  useEffect(() => {
    setForm((f) => ({ ...f, crop_id: cropId }));
  }, [cropId]);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setIsLoading(true);
    try {
      const rec = await createMonitoring(form);
      onCreated(rec);
    } catch (err) {
      setError(normalizeError(err));
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <Modal open={open} onClose={onClose} title="Add Monitoring Record">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div className="grid gap-4 sm:grid-cols-2">
          <FormInput
            label="Date"
            type="date"
            required
            value={form.monitoring_date}
            onChange={(e) => setForm((f) => ({ ...f, monitoring_date: e.target.value }))}
          />
          <FormInput
            label="Growth stage"
            required
            value={form.growth_stage}
            onChange={(e) => setForm((f) => ({ ...f, growth_stage: e.target.value }))}
            placeholder="e.g. Flowering"
          />
        </div>
        <div className="grid gap-4 sm:grid-cols-2">
          <FormInput
            label="Plant height (cm)"
            type="number"
            step="any"
            value={form.plant_height ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, plant_height: e.target.value === '' ? undefined : Number(e.target.value) }))}
          />
          <FormInput
            label="Crop health"
            value={form.crop_health ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, crop_health: e.target.value }))}
            placeholder="e.g. Good"
          />
        </div>
        <div className="flex gap-6">
          <label className="flex items-center gap-2 text-sm text-gray-700">
            <input
              type="checkbox"
              checked={form.pest_observed ?? false}
              onChange={(e) => setForm((f) => ({ ...f, pest_observed: e.target.checked }))}
            />
            Pest observed
          </label>
          <label className="flex items-center gap-2 text-sm text-gray-700">
            <input
              type="checkbox"
              checked={form.disease_observed ?? false}
              onChange={(e) => setForm((f) => ({ ...f, disease_observed: e.target.checked }))}
            />
            Disease observed
          </label>
        </div>
        <FormTextarea
          label="Observation notes"
          value={form.observation_notes ?? ''}
          onChange={(e) => setForm((f) => ({ ...f, observation_notes: e.target.value }))}
        />
        {error && <p className="text-sm text-red-600">{error.message}</p>}
        <button
          type="submit"
          disabled={isLoading}
          className="rounded-lg bg-primary-600 py-2.5 text-sm font-medium text-white hover:bg-primary-700 disabled:opacity-60"
        >
          {isLoading ? 'Saving…' : 'Save Record'}
        </button>
      </form>
    </Modal>
  );
}
