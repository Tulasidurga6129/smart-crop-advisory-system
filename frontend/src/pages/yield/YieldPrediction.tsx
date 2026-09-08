import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Wheat, Sprout, Plus, CloudSun, Droplets, Thermometer, ThermometerSun, ThermometerSnowflake, CheckCircle2 } from 'lucide-react';
import { useFarms } from '../../context/FarmContext';
import { getFarmCrops } from '../../api/crops';
import { getYieldPrediction } from '../../api/yieldPrediction';
import type { CropResponse, YieldPredictionResponse } from '../../types';
import { LoadingSpinner } from '../../components/ui/LoadingSpinner';
import { ErrorMessage } from '../../components/ui/ErrorMessage';
import { EmptyState } from '../../components/ui/EmptyState';
import { StatusBadge } from '../../components/ui/StatusBadge';
import { PredictionResult } from '../../components/dashboard/PredictionResult';
import { normalizeError } from '../../api/client';

export function YieldPrediction() {
  const { farms, selectedFarmId, isLoading: farmsLoading } = useFarms();

  const [crops, setCrops] = useState<CropResponse[]>([]);
  const [cropsLoading, setCropsLoading] = useState(false);
  const [cropsError, setCropsError] = useState<string | null>(null);

  const [selectedCropId, setSelectedCropId] = useState<number | null>(null);
  const [result, setResult] = useState<YieldPredictionResponse | null>(null);
  const [isPredicting, setIsPredicting] = useState(false);
  const [predictionError, setPredictionError] = useState<string | null>(null);

  async function loadCrops() {
    if (!selectedFarmId) return;
    setCropsLoading(true);
    setCropsError(null);
    try {
      const data = await getFarmCrops(selectedFarmId);
      setCrops(data);
      setSelectedCropId((current) => (current && data.some((c) => c.id === current) ? current : data[0]?.id ?? null));
    } catch (err) {
      setCropsError(normalizeError(err).message);
    } finally {
      setCropsLoading(false);
    }
  }

  useEffect(() => {
    loadCrops();
    setResult(null);
    setPredictionError(null);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedFarmId]);

  function selectCrop(cropId: number) {
    setSelectedCropId(cropId);
    setResult(null);
    setPredictionError(null);
  }

  async function handlePredict() {
    if (!selectedCropId) return;
    setIsPredicting(true);
    setPredictionError(null);
    setResult(null);
    try {
      const res = await getYieldPrediction(selectedCropId);
      setResult(res);
    } catch (err) {
      setPredictionError(normalizeError(err).message);
    } finally {
      setIsPredicting(false);
    }
  }

  if (farmsLoading) return <LoadingSpinner size="lg" label="Loading your farms…" />;

  if (farms.length === 0) {
    return (
      <EmptyState
        icon={Sprout}
        title="Add a farm first"
        description="Yield predictions are generated for crops on your farms — add a farm to get started."
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

  return (
    <div className="mx-auto flex max-w-4xl flex-col gap-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Yield Prediction</h1>
        <p className="text-sm text-gray-500">
          Predict the expected yield of your selected crop using crop, farm and automatically collected weather
          data.
        </p>
      </div>

      {/* Crop selection */}
      <div className="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm">
        <p className="mb-3 text-sm font-medium text-gray-700">Select a crop</p>

        {cropsLoading ? (
          <LoadingSpinner label="Loading your crops…" />
        ) : cropsError ? (
          <ErrorMessage message={cropsError} onRetry={loadCrops} />
        ) : crops.length === 0 ? (
          <EmptyState
            icon={Sprout}
            title="No crops on this farm yet"
            description="Add a crop to this farm before predicting its yield."
            action={
              <Link
                to={`/crops/new?farmId=${selectedFarmId}`}
                className="mt-2 inline-flex items-center gap-1.5 rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700"
              >
                <Plus className="h-4 w-4" /> Add Crop
              </Link>
            }
          />
        ) : (
          <div className="grid gap-3 sm:grid-cols-2">
            {crops.map((crop) => {
              const isSelected = crop.id === selectedCropId;
              return (
                <button
                  key={crop.id}
                  type="button"
                  onClick={() => selectCrop(crop.id)}
                  className={`flex flex-col gap-2 rounded-xl border p-4 text-left transition ${
                    isSelected
                      ? 'border-primary-500 bg-primary-50/60 ring-2 ring-primary-200'
                      : 'border-gray-100 bg-white hover:border-primary-200'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <p className="font-semibold capitalize text-gray-900">{crop.name}</p>
                    <StatusBadge value={crop.status} />
                  </div>
                  <p className="text-sm text-gray-500">
                    {crop.variety ? `${crop.variety} · ` : ''}
                    {crop.season}
                  </p>
                  {crop.area != null && <p className="text-xs text-gray-400">{crop.area} acres</p>}
                </button>
              );
            })}
          </div>
        )}

        {crops.length > 0 && (
          <button
            type="button"
            onClick={handlePredict}
            disabled={!selectedCropId || isPredicting}
            className="mt-5 inline-flex items-center justify-center gap-2 rounded-lg bg-earth-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-earth-700 disabled:opacity-60"
          >
            <Wheat className="h-4 w-4" />
            {isPredicting ? 'Predicting…' : 'Predict Yield'}
          </button>
        )}
      </div>

      {isPredicting && <LoadingSpinner size="lg" label="Running the prediction model…" />}
      {predictionError && !isPredicting && <ErrorMessage message={predictionError} onRetry={handlePredict} />}

      {result && !isPredicting && (
        <>
          <PredictionResult predictedYield={result.predicted_yield} />

          {/* Weather / climate information — automatically collected */}
          <div className="rounded-2xl border border-sky-100 bg-gradient-to-br from-sky-50 to-white p-5 shadow-sm">
            <div className="mb-4 flex items-center gap-2 text-sm font-medium text-sky-700">
              <CheckCircle2 className="h-4 w-4" />
              Weather data automatically collected for this prediction
            </div>
            <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
              <div className="flex flex-col items-center gap-1 rounded-lg bg-white/70 py-3 text-center">
                <Droplets className="h-4 w-4 text-sky-500" />
                <span className="text-sm font-semibold text-gray-900">{result.annual_rainfall} mm</span>
                <span className="text-[11px] text-gray-400">Annual Rainfall</span>
              </div>
              <div className="flex flex-col items-center gap-1 rounded-lg bg-white/70 py-3 text-center">
                <Thermometer className="h-4 w-4 text-sky-500" />
                <span className="text-sm font-semibold text-gray-900">{result.avg_temperature}°C</span>
                <span className="text-[11px] text-gray-400">Average Temperature</span>
              </div>
              <div className="flex flex-col items-center gap-1 rounded-lg bg-white/70 py-3 text-center">
                <ThermometerSun className="h-4 w-4 text-sky-500" />
                <span className="text-sm font-semibold text-gray-900">{result.max_temperature}°C</span>
                <span className="text-[11px] text-gray-400">Maximum Temperature</span>
              </div>
              <div className="flex flex-col items-center gap-1 rounded-lg bg-white/70 py-3 text-center">
                <ThermometerSnowflake className="h-4 w-4 text-sky-500" />
                <span className="text-sm font-semibold text-gray-900">{result.min_temperature}°C</span>
                <span className="text-[11px] text-gray-400">Minimum Temperature</span>
              </div>
            </div>
          </div>

          {/* Crop information */}
          <div className="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm">
            <div className="mb-4 flex items-center gap-2 text-sm font-medium text-gray-700">
              <CloudSun className="h-4 w-4 text-primary-600" />
              Crop Information
            </div>
            <dl className="grid grid-cols-2 gap-4 sm:grid-cols-3">
              <div>
                <dt className="text-[11px] uppercase tracking-wide text-gray-400">Crop</dt>
                <dd className="text-sm font-medium capitalize text-gray-900">{result.crop}</dd>
              </div>
              <div>
                <dt className="text-[11px] uppercase tracking-wide text-gray-400">Crop Year</dt>
                <dd className="text-sm font-medium text-gray-900">{result.crop_year}</dd>
              </div>
              <div>
                <dt className="text-[11px] uppercase tracking-wide text-gray-400">Season</dt>
                <dd className="text-sm font-medium text-gray-900">{result.season}</dd>
              </div>
              <div>
                <dt className="text-[11px] uppercase tracking-wide text-gray-400">State</dt>
                <dd className="text-sm font-medium text-gray-900">{result.state}</dd>
              </div>
              <div>
                <dt className="text-[11px] uppercase tracking-wide text-gray-400">Area</dt>
                <dd className="text-sm font-medium text-gray-900">{result.area} acres</dd>
              </div>
            </dl>
          </div>
        </>
      )}
    </div>
  );
}
