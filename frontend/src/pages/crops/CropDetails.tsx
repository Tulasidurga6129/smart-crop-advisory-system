import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { Pencil, Trash2, Sparkles, Bug, LineChart, ClipboardList } from 'lucide-react';
import { getCrop, deleteCrop, updateCrop } from '../../api/crops';
import type { CropResponse, CropUpdate } from '../../types';
import { LoadingSpinner } from '../../components/ui/LoadingSpinner';
import { ErrorMessage } from '../../components/ui/ErrorMessage';
import { StatusBadge } from '../../components/ui/StatusBadge';
import { ConfirmationDialog } from '../../components/ui/ConfirmationDialog';
import { Modal } from '../../components/ui/Modal';
import { FormInput } from '../../components/ui/FormInput';
import { Select } from '../../components/ui/Select';
import { normalizeError } from '../../api/client';

const STATUS_OPTIONS = [
  { value: 'planned', label: 'Planned' },
  { value: 'active', label: 'Active' },
  { value: 'harvested', label: 'Harvested' },
];

export function CropDetails() {
  const { cropId } = useParams();
  const navigate = useNavigate();
  const id = Number(cropId);

  const [crop, setCrop] = useState<CropResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [editOpen, setEditOpen] = useState(false);
  const [editForm, setEditForm] = useState<CropUpdate>({});
  const [saving, setSaving] = useState(false);

  async function load() {
    setIsLoading(true);
    setError(null);
    try {
      const data = await getCrop(id);
      setCrop(data);
      setEditForm({
        name: data.name,
        variety: data.variety ?? '',
        season: data.season,
        sowing_date: data.sowing_date ?? '',
        expected_harvest_date: data.expected_harvest_date ?? '',
        area: data.area ?? undefined,
        status: data.status,
      });
    } catch (err) {
      setError(normalizeError(err).message);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    if (id) load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  async function handleDelete() {
    setDeleting(true);
    try {
      await deleteCrop(id);
      navigate('/crops');
    } catch (err) {
      setError(normalizeError(err).message);
      setDeleting(false);
      setConfirmDelete(false);
    }
  }

  async function handleSaveEdit() {
    setSaving(true);
    try {
      const updated = await updateCrop(id, editForm);
      setCrop(updated);
      setEditOpen(false);
    } catch (err) {
      setError(normalizeError(err).message);
    } finally {
      setSaving(false);
    }
  }

  if (isLoading) return <LoadingSpinner size="lg" />;
  if (error && !crop) return <ErrorMessage message={error} onRetry={load} />;
  if (!crop) return null;

  const quickLinks = [
    { to: `/recommendations?cropId=${id}`, icon: Sparkles, label: 'Get Recommendation', tone: 'bg-primary-50 text-primary-600' },
    { to: `/disease-detection?cropId=${id}`, icon: Bug, label: 'Disease Detection', tone: 'bg-red-50 text-red-600' },
    { to: `/crop-monitoring?cropId=${id}`, icon: LineChart, label: 'Monitoring', tone: 'bg-sky-100 text-sky-600' },
    { to: `/advisories?cropId=${id}&farmId=${crop.farm_id}`, icon: ClipboardList, label: 'Advisories', tone: 'bg-amber-50 text-amber-600' },
  ];

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-semibold text-gray-900">{crop.name}</h1>
            <StatusBadge value={crop.status} />
          </div>
          <p className="text-sm text-gray-500">
            {crop.season} {crop.variety ? `· ${crop.variety}` : ''}
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setEditOpen(true)}
            className="inline-flex items-center gap-1.5 rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            <Pencil className="h-4 w-4" /> Edit
          </button>
          <button
            onClick={() => setConfirmDelete(true)}
            className="inline-flex items-center gap-1.5 rounded-lg border border-red-200 bg-white px-3 py-2 text-sm font-medium text-red-600 hover:bg-red-50"
          >
            <Trash2 className="h-4 w-4" /> Delete
          </button>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4 text-sm">
        <Info label="Sowing date" value={crop.sowing_date} />
        <Info label="Expected harvest" value={crop.expected_harvest_date} />
        <Info label="Area" value={crop.area != null ? `${crop.area} acres` : null} />
        <Info label="Farm" value={String(crop.farm_id)} />
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {quickLinks.map(({ to, icon: Icon, label, tone }) => (
          <Link key={to} to={to} className="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm hover:border-primary-200">
            <div className={`mb-3 w-fit rounded-xl p-2.5 ${tone}`}>
              <Icon className="h-5 w-5" />
            </div>
            <p className="font-medium text-gray-900">{label}</p>
          </Link>
        ))}
      </div>

      <ConfirmationDialog
        open={confirmDelete}
        onClose={() => setConfirmDelete(false)}
        onConfirm={handleDelete}
        title="Delete this crop?"
        message="This will permanently remove the crop and cannot be undone."
        confirmLabel="Delete Crop"
        danger
        isLoading={deleting}
      />

      <Modal open={editOpen} onClose={() => setEditOpen(false)} title="Edit Crop">
        <div className="flex flex-col gap-4">
          <FormInput label="Name" value={editForm.name ?? ''} onChange={(e) => setEditForm((f) => ({ ...f, name: e.target.value }))} />
          <div className="grid gap-4 sm:grid-cols-2">
            <FormInput label="Variety" value={editForm.variety ?? ''} onChange={(e) => setEditForm((f) => ({ ...f, variety: e.target.value }))} />
            <FormInput label="Season" value={editForm.season ?? ''} onChange={(e) => setEditForm((f) => ({ ...f, season: e.target.value }))} />
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            <FormInput
              label="Sowing date"
              type="date"
              value={editForm.sowing_date ?? ''}
              onChange={(e) => setEditForm((f) => ({ ...f, sowing_date: e.target.value }))}
            />
            <FormInput
              label="Expected harvest"
              type="date"
              value={editForm.expected_harvest_date ?? ''}
              onChange={(e) => setEditForm((f) => ({ ...f, expected_harvest_date: e.target.value }))}
            />
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            <FormInput
              label="Area"
              type="number"
              step="any"
              value={editForm.area ?? ''}
              onChange={(e) => setEditForm((f) => ({ ...f, area: e.target.value === '' ? undefined : Number(e.target.value) }))}
            />
            <Select
              label="Status"
              options={STATUS_OPTIONS}
              value={editForm.status ?? ''}
              onChange={(e) => setEditForm((f) => ({ ...f, status: e.target.value }))}
            />
          </div>
          <button
            onClick={handleSaveEdit}
            disabled={saving}
            className="rounded-lg bg-primary-600 py-2.5 text-sm font-medium text-white hover:bg-primary-700 disabled:opacity-60"
          >
            {saving ? 'Saving…' : 'Save Changes'}
          </button>
        </div>
      </Modal>
    </div>
  );
}

function Info({ label, value }: { label: string; value: string | null | undefined }) {
  return (
    <div className="rounded-xl border border-gray-100 bg-white p-3">
      <p className="text-xs text-gray-400">{label}</p>
      <p className="font-medium text-gray-800">{value || '—'}</p>
    </div>
  );
}
