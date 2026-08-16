import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Sprout, CloudSun, ClipboardList, AlertTriangle, Plus, MapPin } from 'lucide-react';
import { useFarms } from '../context/FarmContext';
import { getFarmDashboard } from '../api/dashboard';
import type { FarmDashboardResponse } from '../types';
import { DashboardCard } from '../components/ui/DashboardCard';
import { WeatherCard } from '../components/dashboard/WeatherCard';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';
import { ErrorMessage } from '../components/ui/ErrorMessage';
import { EmptyState } from '../components/ui/EmptyState';
import { StatusBadge } from '../components/ui/StatusBadge';
import { normalizeError } from '../api/client';

export function Dashboard() {
  const { farms, selectedFarmId, isLoading: farmsLoading } = useFarms();
  const [data, setData] = useState<FarmDashboardResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    if (!selectedFarmId) return;
    setIsLoading(true);
    setError(null);
    try {
      const res = await getFarmDashboard(selectedFarmId);
      setData(res);
    } catch (err) {
      setError(normalizeError(err).message);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedFarmId]);

  if (farmsLoading) return <LoadingSpinner size="lg" label="Loading your farms…" />;

  if (farms.length === 0) {
    return (
      <EmptyState
        icon={Sprout}
        title="No farms yet"
        description="Add your first farm to start seeing your dashboard, weather, and advisories."
        action={
          <Link
            to="/farms/new"
            className="mt-2 inline-flex items-center gap-1.5 rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700"
          >
            <Plus className="h-4 w-4" /> Add a farm
          </Link>
        }
      />
    );
  }

  if (isLoading) return <LoadingSpinner size="lg" label="Loading dashboard…" />;
  if (error) return <ErrorMessage message={error} onRetry={load} />;
  if (!data) return null;

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">{data.farm.farm_name}</h1>
        <p className="flex items-center gap-1 text-sm text-gray-500">
          <MapPin className="h-3.5 w-3.5" />
          {[data.farm.village, data.farm.district, data.farm.state].filter(Boolean).join(', ') || 'Location not set'}
        </p>
      </div>

      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <DashboardCard icon={Sprout} label="Active Crops" value={data.crops.length} tone="primary" />
        <DashboardCard
          icon={ClipboardList}
          label="Advisories"
          value={data.summary.total}
          sub={data.summary.top_priority ? `Top priority: ${data.summary.top_priority}` : undefined}
          tone="amber"
        />
        <DashboardCard icon={AlertTriangle} label="High Priority" value={data.summary.high} tone="red" />
        <DashboardCard
          icon={CloudSun}
          label="Land Area"
          value={`${data.farm.land_area} ${data.farm.land_unit}`}
          tone="earth"
        />
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2 flex flex-col gap-6">
          <div>
            <div className="mb-3 flex items-center justify-between">
              <h2 className="font-semibold text-gray-900">Crops on this farm</h2>
              <Link to="/crops" className="text-sm font-medium text-primary-600 hover:underline">
                View all
              </Link>
            </div>
            {data.crops.length === 0 ? (
              <EmptyState title="No crops added yet" description="Add a crop to this farm to start tracking it." />
            ) : (
              <div className="grid gap-3 sm:grid-cols-2">
                {data.crops.map((crop) => (
                  <Link
                    key={crop.id}
                    to={`/crops/${crop.id}`}
                    className="rounded-xl border border-gray-100 bg-white p-4 shadow-sm hover:border-primary-200"
                  >
                    <div className="flex items-center justify-between">
                      <p className="font-medium text-gray-900">{crop.name}</p>
                      <StatusBadge value={crop.status} />
                    </div>
                    <p className="mt-1 text-xs text-gray-400">
                      {crop.season} {crop.variety ? `· ${crop.variety}` : ''}
                    </p>
                  </Link>
                ))}
              </div>
            )}
          </div>

          <div>
            <div className="mb-3 flex items-center justify-between">
              <h2 className="font-semibold text-gray-900">Active advisories</h2>
              <Link to="/advisories" className="text-sm font-medium text-primary-600 hover:underline">
                View all
              </Link>
            </div>
            {data.active_advisories.length === 0 ? (
              <EmptyState title="No active advisories" description="You're all caught up for this farm." />
            ) : (
              <div className="flex flex-col gap-2">
                {data.active_advisories.map((a) => (
                  <div key={a.id} className="rounded-xl border border-gray-100 bg-white p-4 shadow-sm">
                    <div className="flex items-center justify-between">
                      <p className="font-medium text-gray-900">{a.title}</p>
                      <StatusBadge value={a.priority} />
                    </div>
                    <p className="mt-1 text-sm text-gray-500">{a.message}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="flex flex-col gap-6">
          <WeatherCard weather={data.latest_weather} />
          {data.latest_condition && (
            <div className="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm">
              <p className="mb-3 text-xs font-medium uppercase tracking-wide text-gray-400">Latest soil conditions</p>
              <dl className="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <dt className="text-xs text-gray-400">Soil pH</dt>
                  <dd className="font-medium text-gray-800">{data.latest_condition.soil_ph ?? '—'}</dd>
                </div>
                <div>
                  <dt className="text-xs text-gray-400">Nitrogen</dt>
                  <dd className="font-medium text-gray-800">{data.latest_condition.nitrogen ?? '—'}</dd>
                </div>
                <div>
                  <dt className="text-xs text-gray-400">Phosphorus</dt>
                  <dd className="font-medium text-gray-800">{data.latest_condition.phosphorus ?? '—'}</dd>
                </div>
                <div>
                  <dt className="text-xs text-gray-400">Potassium</dt>
                  <dd className="font-medium text-gray-800">{data.latest_condition.potassium ?? '—'}</dd>
                </div>
              </dl>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
