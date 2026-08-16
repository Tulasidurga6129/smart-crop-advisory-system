import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { FarmForm } from '../../components/farm/FarmForm';
import { getFarm, updateFarm } from '../../api/farms';
import { useFarms } from '../../context/FarmContext';
import type { FarmResponse, FarmCreate } from '../../types';
import { LoadingSpinner } from '../../components/ui/LoadingSpinner';
import { ErrorMessage } from '../../components/ui/ErrorMessage';
import { normalizeError } from '../../api/client';

export function EditFarm() {
  const { farmId } = useParams();
  const navigate = useNavigate();
  const { refresh } = useFarms();
  const [farm, setFarm] = useState<FarmResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!farmId) return;
    getFarm(Number(farmId))
      .then(setFarm)
      .catch((err) => setError(normalizeError(err).message))
      .finally(() => setIsLoading(false));
  }, [farmId]);

  async function handleSubmit(payload: FarmCreate) {
    if (!farmId) return;
    await updateFarm(Number(farmId), payload);
    await refresh();
    navigate(`/farms/${farmId}`);
  }

  if (isLoading) return <LoadingSpinner size="lg" />;
  if (error || !farm) return <ErrorMessage message={error || 'Farm not found.'} />;

  return (
    <div className="mx-auto max-w-2xl">
      <h1 className="mb-6 text-2xl font-semibold text-gray-900">Edit Farm</h1>
      <div className="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm">
        <FarmForm initial={farm} onSubmit={handleSubmit} submitLabel="Save Changes" />
      </div>
    </div>
  );
}
