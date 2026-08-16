import { useEffect, useState, type ReactNode } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { Pencil, Trash2, Plus, MapPin } from 'lucide-react';
import { getFarm, deleteFarm } from '../../api/farms';
import { getFarmCrops } from '../../api/crops';
import { getFarmConditions } from '../../api/conditions';
import { getFarmWeather } from '../../api/weather';
import { getFarmAdvisories } from '../../api/advisories';
import type { FarmResponse, CropResponse, FarmConditionResponse, WeatherResponse, CropAdvisoryResponse } from '../../types';
import { useFarms } from '../../context/FarmContext';
import { LoadingSpinner } from '../../components/ui/LoadingSpinner';
import { ErrorMessage } from '../../components/ui/ErrorMessage';
import { EmptyState } from '../../components/ui/EmptyState';
import { StatusBadge } from '../../components/ui/StatusBadge';
import { ConfirmationDialog } from '../../components/ui/ConfirmationDialog';
import { normalizeError } from '../../api/client';

type Tab = 'crops' | 'conditions' | 'weather' | 'advisories';

export function FarmDetails() {
  const { farmId } = useParams();
  const navigate = useNavigate();
  const { refresh } = useFarms();
  const id = Number(farmId);

  const [farm, setFarm] = useState<FarmResponse | null>(null);
  const [crops, setCrops] = useState<CropResponse[]>([]);
  const [conditions, setConditions] = useState<FarmConditionResponse[]>([]);
  const [weather, setWeather] = useState<WeatherResponse[]>([]);
  const [advisories, setAdvisories] = useState<CropAdvisoryResponse[]>([]);
  const [tab, setTab] = useState<Tab>('crops');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [deleting, setDeleting] = useState(false);

  async function load() {
    setIsLoading(true);
    setError(null);
    try {
      const [f, c, cond, w, a] = await Promise.all([
        getFarm(id),
        getFarmCrops(id),
        getFarmConditions(id),
        getFarmWeather(id),
        getFarmAdvisories(id),
      ]);
      setFarm(f);
      setCrops(c);
      setConditions(cond);
      setWeather(w);
      setAdvisories(a);
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
      await deleteFarm(id);
      await refresh();
      navigate('/farms');
    } catch (err) {
      setError(normalizeError(err).message);
      setDeleting(false);
      setConfirmDelete(false);
    }
  }

  if (isLoading) return <LoadingSpinner size="lg" />;
  if (error && !farm) return <ErrorMessage message={error} onRetry={load} />;
  if (!farm) return null;

  const tabs: { key: Tab; label: string; count: number }[] = [
    { key: 'crops', label: 'Crops', count: crops.length },
    { key: 'conditions', label: 'Soil Conditions', count: conditions.length },
    { key: 'weather', label: 'Weather', count: weather.length },
    { key: 'advisories', label: 'Advisories', count: advisories.length },
  ];

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">{farm.farm_name}</h1>
          <p className="flex items-center gap-1 text-sm text-gray-500">
            <MapPin className="h-3.5 w-3.5" />
            {[farm.village, farm.district, farm.state].filter(Boolean).join(', ') || 'Location not set'}
            {' · '}
            {farm.land_area} {farm.land_unit}
          </p>
        </div>
        <div className="flex gap-2">
          <Link
            to={`/farms/${id}/edit`}
            className="inline-flex items-center gap-1.5 rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            <Pencil className="h-4 w-4" /> Edit
          </Link>
          <button
            onClick={() => setConfirmDelete(true)}
            className="inline-flex items-center gap-1.5 rounded-lg border border-red-200 bg-white px-3 py-2 text-sm font-medium text-red-600 hover:bg-red-50"
          >
            <Trash2 className="h-4 w-4" /> Delete
          </button>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4 text-sm">
        <InfoStat label="Soil type" value={farm.soil_type} />
        <InfoStat label="Irrigation" value={farm.irrigation_type} />
        <InfoStat label="Current crop" value={farm.current_crop} />
        <InfoStat label="Land area" value={`${farm.land_area} ${farm.land_unit}`} />
      </div>

      <div className="border-b border-gray-100">
        <nav className="-mb-px flex gap-6">
          {tabs.map((t) => (
            <button
              key={t.key}
              onClick={() => setTab(t.key)}
              className={`border-b-2 px-1 pb-3 text-sm font-medium ${
                tab === t.key ? 'border-primary-600 text-primary-700' : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              {t.label} <span className="text-xs text-gray-400">({t.count})</span>
            </button>
          ))}
        </nav>
      </div>

      {tab === 'crops' && (
        <TabSection
          isEmpty={crops.length === 0}
          emptyTitle="No crops yet"
          addTo={`/crops/new?farmId=${id}`}
          addLabel="Add Crop"
        >
          <div className="grid gap-3 sm:grid-cols-2">
            {crops.map((crop) => (
              <Link
                key={crop.id}
                to={`/crops/${crop.id}`}
                className="rounded-xl border border-gray-100 bg-white p-4 shadow-sm hover:border-primary-200"
              >
                <div className="flex items-center justify-between">
                  <p className="font-medium text-gray-900">{crop.name}</p>
                  <StatusBadge value={crop.status} />
                </div>
                <p className="mt-1 text-xs text-gray-400">{crop.season}</p>
              </Link>
            ))}
          </div>
        </TabSection>
      )}

      {tab === 'conditions' && (
        <TabSection isEmpty={conditions.length === 0} emptyTitle="No soil conditions logged" addTo={`/farms/${id}/conditions/new`} addLabel="Log Condition">
          <div className="flex flex-col gap-3">
            {conditions.map((c) => (
              <div key={c.id} className="rounded-xl border border-gray-100 bg-white p-4 shadow-sm">
                <p className="mb-2 text-xs text-gray-400">{new Date(c.recorded_at).toLocaleString()}</p>
                <div className="grid grid-cols-3 gap-2 text-sm sm:grid-cols-5">
                  <Metric label="pH" value={c.soil_ph} />
                  <Metric label="N" value={c.nitrogen} />
                  <Metric label="P" value={c.phosphorus} />
                  <Metric label="K" value={c.potassium} />
                  <Metric label="Moisture" value={c.soil_moisture} unit="%" />
                </div>
              </div>
            ))}
          </div>
        </TabSection>
      )}

      {tab === 'weather' && (
        <TabSection isEmpty={weather.length === 0} emptyTitle="No weather logged" addTo={`/farms/${id}/weather/new`} addLabel="Log Weather">
          <div className="flex flex-col gap-3">
            {weather.map((w) => (
              <div key={w.id} className="rounded-xl border border-gray-100 bg-white p-4 shadow-sm">
                <p className="mb-2 text-xs text-gray-400">
                  {w.observed_at ? new Date(w.observed_at).toLocaleString() : new Date(w.created_at).toLocaleString()}
                </p>
                <div className="grid grid-cols-3 gap-2 text-sm sm:grid-cols-5">
                  <Metric label="Temp" value={w.temperature} unit="°C" />
                  <Metric label="Humidity" value={w.humidity} unit="%" />
                  <Metric label="Rainfall" value={w.rainfall} unit="mm" />
                  <Metric label="Wind" value={w.wind_speed} />
                  <span className="text-gray-500">{w.weather_condition ?? '—'}</span>
                </div>
              </div>
            ))}
          </div>
        </TabSection>
      )}

      {tab === 'advisories' && (
        <TabSection isEmpty={advisories.length === 0} emptyTitle="No advisories for this farm" addTo={`/advisories/new?farmId=${id}`} addLabel="Create Advisory">
          <div className="flex flex-col gap-3">
            {advisories.map((a) => (
              <Link key={a.id} to={`/advisories/${a.id}`} className="rounded-xl border border-gray-100 bg-white p-4 shadow-sm hover:border-primary-200">
                <div className="flex items-center justify-between">
                  <p className="font-medium text-gray-900">{a.title}</p>
                  <div className="flex gap-2">
                    <StatusBadge value={a.priority} />
                    <StatusBadge value={a.status} />
                  </div>
                </div>
                <p className="mt-1 text-sm text-gray-500">{a.message}</p>
              </Link>
            ))}
          </div>
        </TabSection>
      )}

      <ConfirmationDialog
        open={confirmDelete}
        onClose={() => setConfirmDelete(false)}
        onConfirm={handleDelete}
        title="Delete this farm?"
        message="This will permanently remove the farm. Crops and related records tied to it may also be affected."
        confirmLabel="Delete Farm"
        danger
        isLoading={deleting}
      />
    </div>
  );
}

function InfoStat({ label, value }: { label: string; value: string | null | undefined }) {
  return (
    <div className="rounded-xl border border-gray-100 bg-white p-3">
      <p className="text-xs text-gray-400">{label}</p>
      <p className="font-medium text-gray-800">{value || '—'}</p>
    </div>
  );
}

function Metric({ label, value, unit }: { label: string; value: number | null | undefined; unit?: string }) {
  return (
    <div>
      <p className="text-xs text-gray-400">{label}</p>
      <p className="font-medium text-gray-800">{value != null ? `${value}${unit ?? ''}` : '—'}</p>
    </div>
  );
}

function TabSection({
  children,
  isEmpty,
  emptyTitle,
  addTo,
  addLabel,
}: {
  children: ReactNode;
  isEmpty: boolean;
  emptyTitle: string;
  addTo: string;
  addLabel: string;
}) {
  return (
    <div className="flex flex-col gap-3">
      <div className="flex justify-end">
        <Link
          to={addTo}
          className="inline-flex items-center gap-1.5 rounded-lg bg-primary-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-primary-700"
        >
          <Plus className="h-4 w-4" /> {addLabel}
        </Link>
      </div>
      {isEmpty ? <EmptyState title={emptyTitle} /> : children}
    </div>
  );
}
