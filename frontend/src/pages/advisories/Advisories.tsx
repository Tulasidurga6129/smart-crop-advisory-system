import { useEffect, useState, type FormEvent } from 'react';
import { useSearchParams } from 'react-router-dom';
import { ClipboardList, Plus, Check, X as XIcon, Trash2 } from 'lucide-react';
import { useFarms } from '../../context/FarmContext';
import { getFarmCrops } from '../../api/crops';
import {
  getFarmAdvisories,
  createAdvisory,
  resolveAdvisory,
  dismissAdvisory,
  deleteAdvisory,
} from '../../api/advisories';
import type { CropResponse, CropAdvisoryResponse, CropAdvisoryCreate } from '../../types';
import { Select } from '../../components/ui/Select';
import { FormInput, FormTextarea } from '../../components/ui/FormInput';
import { LoadingSpinner } from '../../components/ui/LoadingSpinner';
import { ErrorMessage } from '../../components/ui/ErrorMessage';
import { EmptyState } from '../../components/ui/EmptyState';
import { StatusBadge } from '../../components/ui/StatusBadge';
import { Modal } from '../../components/ui/Modal';
import { normalizeError, type ApiError } from '../../api/client';

const ADVISORY_TYPES = [
  { value: 'general', label: 'General' },
  { value: 'irrigation', label: 'Irrigation' },
  { value: 'fertilizer', label: 'Fertilizer' },
  { value: 'pest', label: 'Pest' },
  { value: 'disease', label: 'Disease' },
  { value: 'weather', label: 'Weather' },
];

const PRIORITY_OPTIONS = [
  { value: 'low', label: 'Low' },
  { value: 'medium', label: 'Medium' },
  { value: 'high', label: 'High' },
];

export function Advisories({ filterType }: { filterType?: string }) {
  const { selectedFarmId, farms } = useFarms();
  const [params] = useSearchParams();
  const [crops, setCrops] = useState<CropResponse[]>([]);
  const [advisories, setAdvisories] = useState<CropAdvisoryResponse[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formOpen, setFormOpen] = useState(false);

  async function load() {
    if (!selectedFarmId) return;
    setIsLoading(true);
    setError(null);
    try {
      const [c, a] = await Promise.all([getFarmCrops(selectedFarmId), getFarmAdvisories(selectedFarmId)]);
      setCrops(c);
      setAdvisories(a);
    } catch (err) {
      setError(normalizeError(err).message);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    load();
    if (params.get('cropId') || filterType) setFormOpen(false);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedFarmId]);

  const visible = filterType ? advisories.filter((a) => a.advisory_type === filterType) : advisories;

  async function handleResolve(id: number) {
    try {
      const updated = await resolveAdvisory(id);
      setAdvisories((list) => list.map((a) => (a.id === id ? updated : a)));
    } catch (err) {
      setError(normalizeError(err).message);
    }
  }

  async function handleDismiss(id: number) {
    try {
      const updated = await dismissAdvisory(id);
      setAdvisories((list) => list.map((a) => (a.id === id ? updated : a)));
    } catch (err) {
      setError(normalizeError(err).message);
    }
  }

  async function handleDelete(id: number) {
    try {
      await deleteAdvisory(id);
      setAdvisories((list) => list.filter((a) => a.id !== id));
    } catch (err) {
      setError(normalizeError(err).message);
    }
  }

  if (farms.length === 0) {
    return <EmptyState icon={ClipboardList} title="Add a farm first" description="Advisories are tied to a farm and crop." />;
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">{filterType === 'irrigation' ? 'Irrigation Advisory' : 'Crop Advisories'}</h1>
          <p className="text-sm text-gray-500">
            {filterType === 'irrigation'
              ? "Irrigation-related advisories for this farm's crops."
              : 'Advisories and alerts for this farm.'}
          </p>
        </div>
        <button
          onClick={() => setFormOpen(true)}
          disabled={crops.length === 0}
          className="inline-flex items-center gap-1.5 rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700 disabled:opacity-50"
        >
          <Plus className="h-4 w-4" /> New Advisory
        </button>
      </div>

      {isLoading ? (
        <LoadingSpinner size="lg" />
      ) : error ? (
        <ErrorMessage message={error} onRetry={load} />
      ) : visible.length === 0 ? (
        <EmptyState icon={ClipboardList} title="No advisories found" />
      ) : (
        <div className="flex flex-col gap-3">
          {visible.map((a) => (
            <div key={a.id} className="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <div className="flex items-center gap-2">
                    <p className="font-semibold text-gray-900">{a.title}</p>
                    <StatusBadge value={a.priority} />
                    <StatusBadge value={a.status} />
                  </div>
                  <p className="mt-1 text-xs text-gray-400">{a.advisory_type}</p>
                </div>
                <div className="flex shrink-0 gap-1">
                  {a.status === 'active' && (
                    <>
                      <button onClick={() => handleResolve(a.id)} title="Resolve" className="rounded-lg p-2 text-gray-400 hover:bg-primary-50 hover:text-primary-600">
                        <Check className="h-4 w-4" />
                      </button>
                      <button onClick={() => handleDismiss(a.id)} title="Dismiss" className="rounded-lg p-2 text-gray-400 hover:bg-gray-100">
                        <XIcon className="h-4 w-4" />
                      </button>
                    </>
                  )}
                  <button onClick={() => handleDelete(a.id)} title="Delete" className="rounded-lg p-2 text-gray-400 hover:bg-red-50 hover:text-red-600">
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
              <p className="mt-2 text-sm text-gray-600">{a.message}</p>
              {a.valid_until && <p className="mt-2 text-xs text-gray-400">Valid until {new Date(a.valid_until).toLocaleString()}</p>}
            </div>
          ))}
        </div>
      )}

      <AdvisoryFormModal
        open={formOpen}
        onClose={() => setFormOpen(false)}
        crops={crops}
        farmId={selectedFarmId!}
        defaultType={filterType}
        onCreated={(a) => {
          setAdvisories((list) => [a, ...list]);
          setFormOpen(false);
        }}
      />
    </div>
  );
}

function AdvisoryFormModal({
  open,
  onClose,
  crops,
  farmId,
  defaultType,
  onCreated,
}: {
  open: boolean;
  onClose: () => void;
  crops: CropResponse[];
  farmId: number;
  defaultType?: string;
  onCreated: (a: CropAdvisoryResponse) => void;
}) {
  const [form, setForm] = useState<CropAdvisoryCreate>({
    advisory_type: defaultType ?? 'general',
    title: '',
    message: '',
    priority: 'medium',
    status: 'active',
    valid_until: '',
    farm_id: farmId,
    crop_id: crops[0]?.id ?? 0,
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);

  useEffect(() => {
    setForm((f) => ({ ...f, farm_id: farmId, crop_id: crops[0]?.id ?? f.crop_id, advisory_type: defaultType ?? f.advisory_type }));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [farmId, crops, open]);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setIsLoading(true);
    try {
      const a = await createAdvisory(form);
      onCreated(a);
    } catch (err) {
      setError(normalizeError(err));
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <Modal open={open} onClose={onClose} title="New Advisory">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <Select
          label="Crop"
          required
          options={crops.map((c) => ({ value: String(c.id), label: c.name }))}
          value={form.crop_id || ''}
          onChange={(e) => setForm((f) => ({ ...f, crop_id: Number(e.target.value) }))}
        />
        <div className="grid gap-4 sm:grid-cols-2">
          <Select
            label="Type"
            options={ADVISORY_TYPES}
            value={form.advisory_type}
            onChange={(e) => setForm((f) => ({ ...f, advisory_type: e.target.value }))}
          />
          <Select
            label="Priority"
            options={PRIORITY_OPTIONS}
            value={form.priority ?? 'medium'}
            onChange={(e) => setForm((f) => ({ ...f, priority: e.target.value }))}
          />
        </div>
        <FormInput label="Title" required value={form.title} onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))} />
        <FormTextarea label="Message" required value={form.message} onChange={(e) => setForm((f) => ({ ...f, message: e.target.value }))} />
        <FormInput
          label="Valid until"
          type="datetime-local"
          value={form.valid_until ?? ''}
          onChange={(e) => setForm((f) => ({ ...f, valid_until: e.target.value }))}
        />
        {error && <p className="text-sm text-red-600">{error.message}</p>}
        <button
          type="submit"
          disabled={isLoading}
          className="rounded-lg bg-primary-600 py-2.5 text-sm font-medium text-white hover:bg-primary-700 disabled:opacity-60"
        >
          {isLoading ? 'Saving…' : 'Create Advisory'}
        </button>
      </form>
    </Modal>
  );
}
