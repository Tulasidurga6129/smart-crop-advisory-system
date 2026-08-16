import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Plus, Tractor, MapPin } from 'lucide-react';
import { useFarms } from '../../context/FarmContext';
import { LoadingSpinner } from '../../components/ui/LoadingSpinner';
import { EmptyState } from '../../components/ui/EmptyState';
import { ErrorMessage } from '../../components/ui/ErrorMessage';

export function FarmsList() {
  const { farms, isLoading, error, refresh } = useFarms();
  const [retrying, setRetrying] = useState(false);

  if (isLoading) return <LoadingSpinner size="lg" label="Loading your farms…" />;
  if (error)
    return (
      <ErrorMessage
        message={error}
        onRetry={async () => {
          setRetrying(true);
          await refresh();
          setRetrying(false);
        }}
      />
    );

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">My Farms</h1>
        <Link
          to="/farms/new"
          className="inline-flex items-center gap-1.5 rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700"
        >
          <Plus className="h-4 w-4" /> Add Farm
        </Link>
      </div>

      {retrying ? (
        <LoadingSpinner />
      ) : farms.length === 0 ? (
        <EmptyState
          icon={Tractor}
          title="No farms yet"
          description="Add your first farm to start tracking crops, weather, and advisories."
          action={
            <Link
              to="/farms/new"
              className="mt-2 inline-flex items-center gap-1.5 rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700"
            >
              <Plus className="h-4 w-4" /> Add a farm
            </Link>
          }
        />
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {farms.map((farm) => (
            <Link
              key={farm.id}
              to={`/farms/${farm.id}`}
              className="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm transition hover:border-primary-200 hover:shadow"
            >
              <div className="mb-3 flex items-center gap-2">
                <div className="rounded-lg bg-primary-50 p-2">
                  <Tractor className="h-4 w-4 text-primary-600" />
                </div>
                <p className="font-semibold text-gray-900">{farm.farm_name}</p>
              </div>
              <p className="flex items-center gap-1 text-sm text-gray-500">
                <MapPin className="h-3.5 w-3.5" />
                {[farm.village, farm.district, farm.state].filter(Boolean).join(', ') || 'Location not set'}
              </p>
              <div className="mt-3 flex items-center justify-between text-sm">
                <span className="text-gray-500">
                  {farm.land_area} {farm.land_unit}
                </span>
                {farm.current_crop && (
                  <span className="rounded-full bg-primary-50 px-2.5 py-0.5 text-xs font-medium text-primary-700">
                    {farm.current_crop}
                  </span>
                )}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
