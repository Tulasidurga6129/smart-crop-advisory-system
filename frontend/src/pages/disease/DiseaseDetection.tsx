import { useEffect, useState, type FormEvent } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Bug, Plus } from 'lucide-react';
import { useFarms } from '../../context/FarmContext';
import { getFarmCrops } from '../../api/crops';
import { createDetection, getFarmDetections, deleteDetection } from '../../api/disease';
import type { CropResponse, DiseaseDetectionResponse, DiseaseDetectionCreate } from '../../types';
import { Select } from '../../components/ui/Select';
import { FormInput, FormTextarea } from '../../components/ui/FormInput';
import { LoadingSpinner } from '../../components/ui/LoadingSpinner';
import { ErrorMessage } from '../../components/ui/ErrorMessage';
import { EmptyState } from '../../components/ui/EmptyState';
import { StatusBadge } from '../../components/ui/StatusBadge';
import { Modal } from '../../components/ui/Modal';
import { normalizeError, type ApiError } from '../../api/client';

const SEVERITY_OPTIONS = [
  { value: 'low', label: 'Low' },
  { value: 'medium', label: 'Medium' },
  { value: 'high', label: 'High' },
  { value: 'critical', label: 'Critical' },
];

export function DiseaseDetection() {
  const { selectedFarmId, farms } = useFarms();
  const [params] = useSearchParams();
  const [crops, setCrops] = useState<CropResponse[]>([]);
  const [records, setRecords] = useState<DiseaseDetectionResponse[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formOpen, setFormOpen] = useState(false);

  async function load() {
    if (!selectedFarmId) return;
    setIsLoading(true);
    setError(null);
    try {
      const [c, d] = await Promise.all([getFarmCrops(selectedFarmId), getFarmDetections(selectedFarmId)]);
      setCrops(c);
      setRecords(d);
    } catch (err) {
      setError(normalizeError(err).message);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    load();
    if (params.get('cropId')) setFormOpen(true);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedFarmId]);

  async function handleDelete(id: number) {
    try {
      await deleteDetection(id);
      setRecords((r) => r.filter((rec) => rec.id !== id));
    } catch (err) {
      setError(normalizeError(err).message);
    }
  }

  if (farms.length === 0) {
    return <EmptyState icon={Bug} title="Add a farm first" description="Disease records are tied to a farm and crop." />;
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Disease Detection</h1>
          <p className="text-sm text-gray-500">Record and track crop disease diagnoses for this farm.</p>
        </div>
        <button
          onClick={() => setFormOpen(true)}
          disabled={crops.length === 0}
          className="inline-flex items-center gap-1.5 rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700 disabled:opacity-50"
        >
          <Plus className="h-4 w-4" /> New Record
        </button>
      </div>

      {isLoading ? (
        <LoadingSpinner size="lg" />
      ) : error ? (
        <ErrorMessage message={error} onRetry={load} />
      ) : records.length === 0 ? (
        <EmptyState icon={Bug} title="No disease records yet" description={crops.length === 0 ? 'Add a crop first.' : undefined} />
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          {records.map((rec) => (
            <div key={rec.id} className="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm">
              <div className="mb-2 flex items-center justify-between">
                <p className="font-semibold text-gray-900">{rec.disease_name}</p>
                <StatusBadge value={rec.severity} />
              </div>
              {rec.confidence != null && <p className="text-xs text-gray-400">Confidence: {(rec.confidence * 100).toFixed(0)}%</p>}
              {rec.symptoms && <p className="mt-2 text-sm text-gray-600">{rec.symptoms}</p>}
              {rec.recommended_treatment && (
                <p className="mt-2 text-sm text-primary-700">
                  <span className="font-medium">Treatment: </span>
                  {rec.recommended_treatment}
                </p>
              )}
              <div className="mt-3 flex items-center justify-between">
                <StatusBadge value={rec.status} />
                <button onClick={() => handleDelete(rec.id)} className="text-xs font-medium text-red-500 hover:underline">
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      <DetectionFormModal
        open={formOpen}
        onClose={() => setFormOpen(false)}
        crops={crops}
        farmId={selectedFarmId!}
        defaultCropId={params.get('cropId') ? Number(params.get('cropId')) : undefined}
        onCreated={(rec) => {
          setRecords((r) => [rec, ...r]);
          setFormOpen(false);
        }}
      />
    </div>
  );
}

function DetectionFormModal({
  open,
  onClose,
  crops,
  farmId,
  defaultCropId,
  onCreated,
}: {
  open: boolean;
  onClose: () => void;
  crops: CropResponse[];
  farmId: number;
  defaultCropId?: number;
  onCreated: (rec: DiseaseDetectionResponse) => void;
}) {
  const [form, setForm] = useState<DiseaseDetectionCreate>({
    disease_name: '',
    severity: 'medium',
    symptoms: '',
    recommended_treatment: '',
    preventive_measures: '',
    detection_source: 'manual',
    status: 'active',
    farm_id: farmId,
    crop_id: defaultCropId ?? crops[0]?.id ?? 0,
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);

  useEffect(() => {
    setForm((f) => ({ ...f, farm_id: farmId, crop_id: defaultCropId ?? crops[0]?.id ?? f.crop_id }));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [farmId, crops, defaultCropId, open]);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setIsLoading(true);
    try {
      const rec = await createDetection(form);
      onCreated(rec);
    } catch (err) {
      setError(normalizeError(err));
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <Modal open={open} onClose={onClose} title="New Disease Record">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <Select
          label="Crop"
          required
          options={crops.map((c) => ({ value: String(c.id), label: c.name }))}
          value={form.crop_id || ''}
          onChange={(e) => setForm((f) => ({ ...f, crop_id: Number(e.target.value) }))}
        />
        <FormInput
          label="Disease name"
          required
          value={form.disease_name}
          onChange={(e) => setForm((f) => ({ ...f, disease_name: e.target.value }))}
        />
        <div className="grid gap-4 sm:grid-cols-2">
          <Select
            label="Severity"
            options={SEVERITY_OPTIONS}
            value={form.severity ?? 'medium'}
            onChange={(e) => setForm((f) => ({ ...f, severity: e.target.value }))}
          />
          <FormInput
            label="Confidence (0-1)"
            type="number"
            step="0.01"
            min={0}
            max={1}
            value={form.confidence ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, confidence: e.target.value === '' ? undefined : Number(e.target.value) }))}
          />
        </div>
        <FormTextarea
          label="Symptoms"
          value={form.symptoms ?? ''}
          onChange={(e) => setForm((f) => ({ ...f, symptoms: e.target.value }))}
        />
        <FormTextarea
          label="Recommended treatment"
          value={form.recommended_treatment ?? ''}
          onChange={(e) => setForm((f) => ({ ...f, recommended_treatment: e.target.value }))}
        />
        <FormTextarea
          label="Preventive measures"
          value={form.preventive_measures ?? ''}
          onChange={(e) => setForm((f) => ({ ...f, preventive_measures: e.target.value }))}
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
