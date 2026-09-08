import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Sparkles } from 'lucide-react';

import { useFarms } from '../../context/FarmContext';
import { getFarmCrops } from '../../api/crops';
import { generateRecommendations } from '../../api/recommendations';

import type {
  CropResponse,
  RecommendationResponseUnknown,
} from '../../types';

import { Select } from '../../components/ui/Select';
import { LoadingSpinner } from '../../components/ui/LoadingSpinner';
import { ErrorMessage } from '../../components/ui/ErrorMessage';
import { EmptyState } from '../../components/ui/EmptyState';
import { RecommendationCard } from '../../components/dashboard/RecommendationCard';
import { normalizeError } from '../../api/client';

export function Recommendations() {
  const { selectedFarmId, farms } = useFarms();
  const [params] = useSearchParams();

  const [crops, setCrops] = useState<CropResponse[]>([]);

  const [selectedCropId, setSelectedCropId] = useState<number | null>(
    params.get('cropId') ? Number(params.get('cropId')) : null
  );

  const [loadingCrops, setLoadingCrops] = useState(false);

  const [result, setResult] =
    useState<RecommendationResponseUnknown | null>(null);

  const [generating, setGenerating] = useState(false);

  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!selectedFarmId) return;

    setLoadingCrops(true);
    setError(null);

    getFarmCrops(selectedFarmId)
      .then((data) => {
        setCrops(data);

        setSelectedCropId((current) => {
          if (current && data.some((crop) => crop.id === current)) {
            return current;
          }

          return data[0]?.id ?? null;
        });
      })
      .catch((err) => {
        setError(normalizeError(err).message);
      })
      .finally(() => {
        setLoadingCrops(false);
      });
  }, [selectedFarmId]);

  async function handleGenerate() {
    if (!selectedCropId) {
      setError('Please select a crop first.');
      return;
    }

    setGenerating(true);
    setError(null);
    setResult(null);

    try {
      console.log(
        'Generating recommendations for crop:',
        selectedCropId
      );

      const data = await generateRecommendations(selectedCropId);

      console.log('Recommendation API response:', data);

      setResult(data);
    } catch (err) {
      console.error('Recommendation error:', err);
      setError(normalizeError(err).message);
    } finally {
      setGenerating(false);
    }
  }

  if (farms.length === 0) {
    return (
      <EmptyState
        icon={Sparkles}
        title="Add a farm and crop first"
        description="Recommendations are generated per crop."
      />
    );
  }

  return (
    <div className="mx-auto flex max-w-2xl flex-col gap-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">
          Crop &amp; Fertilizer Recommendation
        </h1>

        <p className="text-sm text-gray-500">
          Generate crop guidance and fertilizer recommendations for a
          specific crop using the backend recommendation engine.
        </p>
      </div>

      <div className="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm">
        {loadingCrops ? (
          <LoadingSpinner />
        ) : crops.length === 0 ? (
          <EmptyState title="No crops on the selected farm yet" />
        ) : (
          <div className="flex flex-col gap-4">
            <Select
              label="Crop"
              options={crops.map((crop) => ({
                value: String(crop.id),
                label: `${crop.name} (${crop.season})`,
              }))}
              value={selectedCropId ?? ''}
              onChange={(e) => {
                setSelectedCropId(Number(e.target.value));
                setResult(null);
                setError(null);
              }}
            />

            <button
              onClick={handleGenerate}
              disabled={generating || !selectedCropId}
              className="inline-flex items-center justify-center gap-2 rounded-lg bg-primary-600 py-2.5 text-sm font-medium text-white hover:bg-primary-700 disabled:opacity-60"
            >
              <Sparkles className="h-4 w-4" />

              {generating
                ? 'Generating...'
                : 'Generate Recommendation'}
            </button>
          </div>
        )}
      </div>

      {generating && (
        <LoadingSpinner label="Asking the backend for recommendations..." />
      )}

      {error && (
        <ErrorMessage
          message={error}
          onRetry={handleGenerate}
        />
      )}

      {result && <RecommendationCard data={result} />}
    </div>
  );
}