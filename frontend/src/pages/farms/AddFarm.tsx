import { useNavigate } from 'react-router-dom';
import { FarmForm } from '../../components/farm/FarmForm';
import { createFarm } from '../../api/farms';
import { useFarms } from '../../context/FarmContext';
import type { FarmCreate } from '../../types';

export function AddFarm() {
  const navigate = useNavigate();
  const { refresh, setSelectedFarmId } = useFarms();

  async function handleSubmit(payload: FarmCreate) {
    const farm = await createFarm(payload);
    await refresh();
    setSelectedFarmId(farm.id);
    navigate(`/farms/${farm.id}`);
  }

  return (
    <div className="mx-auto max-w-2xl">
      <h1 className="mb-6 text-2xl font-semibold text-gray-900">Add Farm</h1>
      <div className="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm">
        <FarmForm onSubmit={handleSubmit} submitLabel="Create Farm" />
      </div>
    </div>
  );
}
