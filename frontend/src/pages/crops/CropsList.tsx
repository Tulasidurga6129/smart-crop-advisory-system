import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Plus, Sprout } from 'lucide-react';
import { useFarms } from '../../context/FarmContext';
import { getFarmCrops } from '../../api/crops';
import type { CropResponse } from '../../types';
import { LoadingSpinner } from '../../components/ui/LoadingSpinner';
import { ErrorMessage } from '../../components/ui/ErrorMessage';
import { EmptyState } from '../../components/ui/EmptyState';
import { StatusBadge } from '../../components/ui/StatusBadge';
import { normalizeError } from '../../api/client';

export function CropsList() {
  const { farms, selectedFarmId } = useFarms();
  const [crops, setCrops] = useState<CropResponse[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    if (!selectedFarmId) return;
    setIsLoading(true);
    setError(null);
    try {
      setCrops(await getFarmCrops(selectedFarmId));
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

  if (farms.length === 0) {
    return <EmptyState icon={Sprout} title="Add a farm first" description="Crops belong to a farm — add one to get started." />;
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Crops</h1>
        <Link
          to={`/crops/new?farmId=${selectedFarmId}`}
          className="inline-flex items-center gap-1.5 rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700"
        >
          <Plus className="h-4 w-4" /> Add Crop
        </Link>
      </div>

      {isLoading ? (
        <LoadingSpinner size="lg" />
      ) : error ? (
        <ErrorMessage message={error} onRetry={load} />
      ) : crops.length === 0 ? (
        <EmptyState icon={Sprout} title="No crops on this farm yet" />
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {crops.map((crop) => (
            <Link
              key={crop.id}
              to={`/crops/${crop.id}`}
              className="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm hover:border-primary-200"
            >
              <div className="mb-2 flex items-center justify-between">
                <p className="font-semibold text-gray-900">{crop.name}</p>
                <StatusBadge value={crop.status} />
              </div>
              <p className="text-sm text-gray-500">
                {crop.season} {crop.variety ? `· ${crop.variety}` : ''}
              </p>
              {crop.area != null && <p className="mt-2 text-xs text-gray-400">{crop.area} acres</p>}
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
