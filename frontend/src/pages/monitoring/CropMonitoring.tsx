import { useEffect, useMemo, useState, type FormEvent } from 'react';
import { useSearchParams } from 'react-router-dom';
import {
  LineChart,
  Plus,
  RefreshCw,
  Sprout,
  CalendarDays,
  Clock,
  HeartPulse,
  Ruler,
  Bug,
  ShieldAlert,
} from 'lucide-react';

import { useFarms } from '../../context/FarmContext';
import { getFarmCrops } from '../../api/crops';
import {
  getCropMonitoringRecords,
  createMonitoring,
} from '../../api/monitoring';

import type {
  CropResponse,
  CropMonitoringResponse,
  CropMonitoringCreate,
} from '../../types';

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
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formOpen, setFormOpen] = useState(false);

  const selectedCrop = useMemo(
    () => crops.find((crop) => crop.id === selectedCropId) ?? null,
    [crops, selectedCropId]
  );

  async function loadCrops() {
    if (!selectedFarmId) return;

    try {
      setError(null);

      const data = await getFarmCrops(selectedFarmId);

      setCrops(data);

      setSelectedCropId((current) => {
        if (current && data.some((crop) => crop.id === current)) {
          return current;
        }

        return data[0]?.id ?? null;
      });
    } catch (err) {
      setError(normalizeError(err).message);
    }
  }

  async function loadRecords(cropId: number) {
    setIsLoading(true);
    setError(null);

    try {
      const data = await getCropMonitoringRecords(cropId);

      setRecords(
        data
          .slice()
          .sort((a, b) =>
            b.monitoring_date.localeCompare(a.monitoring_date)
          )
      );
    } catch (err) {
      setError(normalizeError(err).message);
    } finally {
      setIsLoading(false);
    }
  }

  async function refreshMonitoring() {
    if (!selectedCropId) return;

    setIsRefreshing(true);

    try {
      await loadCrops();
      await loadRecords(selectedCropId);
    } finally {
      setIsRefreshing(false);
    }
  }

  useEffect(() => {
    if (!selectedFarmId) return;

    loadCrops();
  }, [selectedFarmId]);

  useEffect(() => {
    if (!selectedCropId) {
      setRecords([]);
      return;
    }

    loadRecords(selectedCropId);
  }, [selectedCropId]);

  if (farms.length === 0) {
    return (
      <EmptyState
        icon={LineChart}
        title="Add a farm first"
        description="Crop monitoring is available after adding a farm and crop."
      />
    );
  }

  if (crops.length === 0) {
    return (
      <EmptyState
        icon={Sprout}
        title="Add a crop first"
        description="Select or add a crop before monitoring its growth."
      />
    );
  }

  return (
    <div className="flex flex-col gap-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">
            Crop Monitoring
          </h1>

          <p className="text-sm text-gray-500">
            Monitor crop growth and record field observations.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Select
            label=""
            options={crops.map((crop) => ({
              value: String(crop.id),
              label: crop.name,
            }))}
            value={selectedCropId ?? ''}
            onChange={(e) => setSelectedCropId(Number(e.target.value))}
            className="min-w-[11rem]"
          />

          <button
            onClick={refreshMonitoring}
            disabled={isRefreshing}
            title="Refresh monitoring"
            className="inline-flex items-center gap-1.5 rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
          >
            <RefreshCw
              className={`h-4 w-4 ${isRefreshing ? 'animate-spin' : ''}`}
            />
            Refresh
          </button>

          <button
            onClick={() => setFormOpen(true)}
            disabled={!selectedCropId}
            className="inline-flex items-center gap-1.5 rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700 disabled:opacity-50"
          >
            <Plus className="h-4 w-4" />
            Add Observation
          </button>
        </div>
      </div>

      {error && (
        <ErrorMessage
          message={error}
          onRetry={() =>
            selectedCropId
              ? loadRecords(selectedCropId)
              : loadCrops()
          }
        />
      )}

      {/* Automatic Crop Information */}
      {selectedCrop && (
        <AutomaticCropInformation crop={selectedCrop} />
      )}

      {/* Latest Observation */}
      {!isLoading && records.length > 0 && (
        <LatestObservation record={records[0]} />
      )}

      {/* Monitoring History */}
      <div>
        <div className="mb-3 flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-gray-900">
              Monitoring History
            </h2>

            <p className="text-sm text-gray-500">
              Farmer observations recorded for this crop.
            </p>
          </div>
        </div>

        {isLoading ? (
          <LoadingSpinner size="lg" />
        ) : records.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-gray-200 bg-white p-8 text-center">
            <LineChart className="mx-auto h-8 w-8 text-gray-400" />

            <h3 className="mt-3 font-medium text-gray-900">
              No observations yet
            </h3>

            <p className="mt-1 text-sm text-gray-500">
              The crop information above is automatic. Add an observation
              when you want to record what you see in the field.
            </p>

            <button
              onClick={() => setFormOpen(true)}
              className="mt-4 inline-flex items-center gap-1.5 rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700"
            >
              <Plus className="h-4 w-4" />
              Add Observation
            </button>
          </div>
        ) : (
          <div className="relative flex flex-col gap-3 border-l-2 border-primary-100 pl-5">
            {records.map((record) => (
              <MonitoringHistoryCard
                key={record.id}
                record={record}
              />
            ))}
          </div>
        )}
      </div>

      {/* Observation Modal */}
      {selectedCropId && (
        <MonitoringFormModal
          open={formOpen}
          onClose={() => setFormOpen(false)}
          cropId={selectedCropId}
          crop={selectedCrop}
          onCreated={(record) => {
            setRecords((current) =>
              [record, ...current].sort((a, b) =>
                b.monitoring_date.localeCompare(a.monitoring_date)
              )
            );

            setFormOpen(false);
          }}
        />
      )}
    </div>
  );
}

/* -------------------------------------------------------------------------- */
/* Automatic Crop Information                                                */
/* -------------------------------------------------------------------------- */

function AutomaticCropInformation({
  crop,
}: {
  crop: CropResponse;
}) {
  return (
    <div className="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm">
      <div className="mb-5">
        <div className="flex items-center gap-2">
          <Sprout className="h-5 w-5 text-primary-600" />

          <h2 className="text-lg font-semibold text-gray-900">
            {crop.name}
          </h2>
        </div>

        <p className="mt-1 text-sm text-gray-500">
          Current crop information calculated by the system.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <InfoCard
          icon={Clock}
          label="Crop Age"
          value={
            crop.crop_age_days != null
              ? `${crop.crop_age_days} days`
              : 'Not available'
          }
        />

        <InfoCard
          icon={Sprout}
          label="Growth Stage"
          value={crop.growth_stage || 'Not available'}
        />

        <InfoCard
          icon={CalendarDays}
          label="Sowing Date"
          value={
            crop.sowing_date
              ? formatDate(crop.sowing_date)
              : 'Not available'
          }
        />

        <InfoCard
          icon={CalendarDays}
          label="Expected Harvest"
          value={
            crop.expected_harvest_date
              ? formatDate(crop.expected_harvest_date)
              : 'Not available'
          }
        />
      </div>

      <div className="mt-4 grid gap-4 sm:grid-cols-2">
        <div className="rounded-xl bg-gray-50 p-4">
          <p className="text-xs font-medium uppercase tracking-wide text-gray-500">
            Crop Status
          </p>

          <p className="mt-1 font-semibold capitalize text-gray-900">
            {crop.status || 'Unknown'}
          </p>
        </div>

        <div className="rounded-xl bg-gray-50 p-4">
          <p className="text-xs font-medium uppercase tracking-wide text-gray-500">
            Harvest Countdown
          </p>

          <p className="mt-1 font-semibold text-gray-900">
            {crop.days_to_harvest != null
              ? crop.days_to_harvest > 0
                ? `${crop.days_to_harvest} days remaining`
                : 'Harvest due'
              : 'Not available'}
          </p>
        </div>
      </div>
    </div>
  );
}

/* -------------------------------------------------------------------------- */
/* Info Card                                                                  */
/* -------------------------------------------------------------------------- */

function InfoCard({
  icon: Icon,
  label,
  value,
}: {
  icon: typeof Clock;
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-xl border border-gray-100 bg-gray-50 p-4">
      <div className="flex items-center gap-2 text-gray-500">
        <Icon className="h-4 w-4" />

        <span className="text-xs font-medium uppercase tracking-wide">
          {label}
        </span>
      </div>

      <p className="mt-2 font-semibold text-gray-900">
        {value}
      </p>
    </div>
  );
}

/* -------------------------------------------------------------------------- */
/* Latest Observation                                                         */
/* -------------------------------------------------------------------------- */

function LatestObservation({
  record,
}: {
  record: CropMonitoringResponse;
}) {
  return (
    <div className="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div>
          <h2 className="text-lg font-semibold text-gray-900">
            Latest Observation
          </h2>

          <p className="text-sm text-gray-500">
            Recorded on {formatDate(record.monitoring_date)}
          </p>
        </div>

        {record.crop_health && (
          <span className="rounded-full bg-primary-50 px-3 py-1 text-xs font-medium text-primary-700">
            {record.crop_health}
          </span>
        )}
      </div>

      <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        {record.plant_height != null && (
          <ObservationItem
            icon={Ruler}
            label="Plant Height"
            value={`${record.plant_height} cm`}
          />
        )}

        {record.crop_health && (
          <ObservationItem
            icon={HeartPulse}
            label="Crop Health"
            value={record.crop_health}
          />
        )}

        <ObservationItem
          icon={Bug}
          label="Pest"
          value={record.pest_observed ? 'Observed' : 'Not observed'}
        />

        <ObservationItem
          icon={ShieldAlert}
          label="Disease"
          value={record.disease_observed ? 'Observed' : 'Not observed'}
        />
      </div>

      {record.observation_notes && (
        <div className="mt-4 rounded-xl bg-gray-50 p-4">
          <p className="text-xs font-medium uppercase tracking-wide text-gray-500">
            Notes
          </p>

          <p className="mt-1 text-sm text-gray-700">
            {record.observation_notes}
          </p>
        </div>
      )}
    </div>
  );
}

/* -------------------------------------------------------------------------- */
/* Observation Item                                                           */
/* -------------------------------------------------------------------------- */

function ObservationItem({
  icon: Icon,
  label,
  value,
}: {
  icon: typeof Ruler;
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-xl border border-gray-100 p-3">
      <div className="flex items-center gap-2 text-gray-500">
        <Icon className="h-4 w-4" />

        <span className="text-xs">{label}</span>
      </div>

      <p className="mt-1 text-sm font-semibold text-gray-900">
        {value}
      </p>
    </div>
  );
}

/* -------------------------------------------------------------------------- */
/* Monitoring History                                                         */
/* -------------------------------------------------------------------------- */

function MonitoringHistoryCard({
  record,
}: {
  record: CropMonitoringResponse;
}) {
  return (
    <div className="relative rounded-xl border border-gray-100 bg-white p-4 shadow-sm">
      <span className="absolute -left-[27px] top-5 h-3 w-3 rounded-full bg-primary-500" />

      <div className="flex flex-wrap items-center justify-between gap-2">
        <div>
          <p className="font-medium text-gray-900">
            {record.growth_stage}
          </p>

          <p className="text-xs text-gray-400">
            {formatDate(record.monitoring_date)}
          </p>
        </div>

        {record.crop_health && (
          <span className="rounded-full bg-gray-100 px-2.5 py-1 text-xs text-gray-700">
            {record.crop_health}
          </span>
        )}
      </div>

      <div className="mt-3 flex flex-wrap gap-3 text-xs text-gray-500">
        {record.plant_height != null && (
          <span>Height: {record.plant_height} cm</span>
        )}

        <span>
          Pest: {record.pest_observed ? 'Yes' : 'No'}
        </span>

        <span>
          Disease: {record.disease_observed ? 'Yes' : 'No'}
        </span>
      </div>

      {record.observation_notes && (
        <p className="mt-2 text-sm text-gray-600">
          {record.observation_notes}
        </p>
      )}
    </div>
  );
}

/* -------------------------------------------------------------------------- */
/* Add Observation Modal                                                      */
/* -------------------------------------------------------------------------- */

function MonitoringFormModal({
  open,
  onClose,
  cropId,
  crop,
  onCreated,
}: {
  open: boolean;
  onClose: () => void;
  cropId: number;
  crop: CropResponse | null;
  onCreated: (record: CropMonitoringResponse) => void;
}) {
  const [form, setForm] = useState<CropMonitoringCreate>({
    crop_id: cropId,
    monitoring_date: new Date().toISOString().slice(0, 10),
    growth_stage: crop?.growth_stage || 'Not specified',
    plant_height: undefined,
    crop_health: '',
    pest_observed: false,
    disease_observed: false,
    observation_notes: '',
  });

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);

  useEffect(() => {
    setForm((current) => ({
      ...current,
      crop_id: cropId,
      growth_stage: crop?.growth_stage || 'Not specified',
    }));
  }, [cropId, crop?.growth_stage]);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();

    setError(null);
    setIsLoading(true);

    try {
      const record = await createMonitoring(form);

      onCreated(record);
    } catch (err) {
      setError(normalizeError(err));
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Add Crop Observation"
    >
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        {/* Automatic stage information */}
        <div className="rounded-xl bg-primary-50 p-4">
          <div className="flex items-center gap-2">
            <Sprout className="h-4 w-4 text-primary-600" />

            <p className="text-sm font-medium text-primary-800">
              Current Growth Stage
            </p>
          </div>

          <p className="mt-1 text-sm text-primary-700">
            {crop?.growth_stage || 'Not available'}
          </p>

          <p className="mt-2 text-xs text-primary-600">
            Growth stage is calculated automatically from the crop's
            sowing date.
          </p>
        </div>

        <FormInput
          label="Observation date"
          type="date"
          required
          value={form.monitoring_date}
          onChange={(e) =>
            setForm((current) => ({
              ...current,
              monitoring_date: e.target.value,
            }))
          }
        />

        <FormInput
          label="Plant height (cm)"
          type="number"
          step="any"
          min="0"
          value={form.plant_height ?? ''}
          onChange={(e) =>
            setForm((current) => ({
              ...current,
              plant_height:
                e.target.value === ''
                  ? undefined
                  : Number(e.target.value),
            }))
          }
          placeholder="e.g. 24"
        />

        <FormInput
          label="Crop health"
          value={form.crop_health ?? ''}
          onChange={(e) =>
            setForm((current) => ({
              ...current,
              crop_health: e.target.value,
            }))
          }
          placeholder="e.g. Good, Moderate, Poor"
        />

        <div className="flex flex-col gap-3">
          <label className="flex items-center gap-2 text-sm text-gray-700">
            <input
              type="checkbox"
              checked={form.pest_observed ?? false}
              onChange={(e) =>
                setForm((current) => ({
                  ...current,
                  pest_observed: e.target.checked,
                }))
              }
            />

            Pest observed
          </label>

          <label className="flex items-center gap-2 text-sm text-gray-700">
            <input
              type="checkbox"
              checked={form.disease_observed ?? false}
              onChange={(e) =>
                setForm((current) => ({
                  ...current,
                  disease_observed: e.target.checked,
                }))
              }
            />

            Disease observed
          </label>
        </div>

        <FormTextarea
          label="Observation notes"
          value={form.observation_notes ?? ''}
          onChange={(e) =>
            setForm((current) => ({
              ...current,
              observation_notes: e.target.value,
            }))
          }
          placeholder="Describe anything unusual you observed in the field..."
        />

        {error && (
          <p className="text-sm text-red-600">
            {error.message}
          </p>
        )}

        <button
          type="submit"
          disabled={isLoading}
          className="rounded-lg bg-primary-600 py-2.5 text-sm font-medium text-white hover:bg-primary-700 disabled:opacity-60"
        >
          {isLoading ? 'Saving…' : 'Save Observation'}
        </button>
      </form>
    </Modal>
  );
}

/* -------------------------------------------------------------------------- */
/* Helpers                                                                    */
/* -------------------------------------------------------------------------- */

function formatDate(date: string) {
  return new Date(`${date}T00:00:00`).toLocaleDateString();
}