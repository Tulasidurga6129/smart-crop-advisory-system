import { useCallback, useEffect, useState } from 'react';
import {
  AlertTriangle,
  CheckCircle2,
  CloudRain,
  Droplets,
  FlaskConical,
  Leaf,
  RefreshCw,
  Thermometer,
  X,
} from 'lucide-react';

import { useFarms } from '../../context/FarmContext';
import { getFarmCrops } from '../../api/crops';

import {
  getFarmAdvisories,
  generateRecommendations,
  resolveAdvisory,
  dismissAdvisory,
} from '../../api/advisories';

import type {
  CropResponse,
  CropAdvisoryResponse,
} from '../../types';

import { LoadingSpinner } from '../../components/ui/LoadingSpinner';
import { ErrorMessage } from '../../components/ui/ErrorMessage';
import { EmptyState } from '../../components/ui/EmptyState';
import { StatusBadge } from '../../components/ui/StatusBadge';
import { normalizeError } from '../../api/client';

interface AdvisoriesProps {
  filterType?: string;
}

export function Advisories({
  filterType,
}: AdvisoriesProps) {
  const { selectedFarmId, farms } = useFarms();

  const [crops, setCrops] = useState<CropResponse[]>([]);
  const [advisories, setAdvisories] = useState<
    CropAdvisoryResponse[]
  >([]);

  const [isLoading, setIsLoading] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Load crops and existing advisories.
   */
  const loadData = useCallback(async () => {
    if (!selectedFarmId) {
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const [cropData, advisoryData] =
        await Promise.all([
          getFarmCrops(selectedFarmId),
          getFarmAdvisories(selectedFarmId),
        ]);

      setCrops(cropData);
      setAdvisories(advisoryData);
    } catch (err) {
      setError(normalizeError(err).message);
    } finally {
      setIsLoading(false);
    }
  }, [selectedFarmId]);

  /**
   * Automatically generate recommendations
   * for all crops belonging to the selected farm.
   */
  const generateAutomaticAdvisories =
    useCallback(async () => {
      if (!selectedFarmId) {
        return;
      }

      setIsGenerating(true);
      setError(null);

      try {
        const cropData =
          await getFarmCrops(selectedFarmId);

        setCrops(cropData);

        /*
         * Generate recommendations for every crop.
         *
         * Backend endpoint:
         * POST /recommendations/{crop_id}
         */
        for (const crop of cropData) {
          try {
            await generateRecommendations(crop.id);
          } catch (err) {
            /*
             * One crop failing should not stop
             * recommendations for other crops.
             */
            console.error(
              `Recommendation generation failed for crop ${crop.id}`,
              err
            );
          }
        }

        /*
         * Fetch the newly generated advisories.
         */
        const advisoryData =
          await getFarmAdvisories(selectedFarmId);

        setAdvisories(advisoryData);
      } catch (err) {
        setError(normalizeError(err).message);
      } finally {
        setIsGenerating(false);
      }
    }, [selectedFarmId]);

  /**
   * When farm changes:
   *
   * 1. Load existing data.
   * 2. Automatically generate fresh recommendations.
   */
  useEffect(() => {
    if (!selectedFarmId) {
      return;
    }

    loadData().then(() => {
      generateAutomaticAdvisories();
    });
  }, [
    selectedFarmId,
    loadData,
    generateAutomaticAdvisories,
  ]);

  /**
   * Resolve advisory.
   */
  async function handleResolve(id: number) {
    try {
      const updated = await resolveAdvisory(id);

      setAdvisories((current) =>
        current.map((advisory) =>
          advisory.id === id
            ? updated
            : advisory
        )
      );
    } catch (err) {
      setError(normalizeError(err).message);
    }
  }

  /**
   * Dismiss advisory.
   */
  async function handleDismiss(id: number) {
    try {
      const updated = await dismissAdvisory(id);

      setAdvisories((current) =>
        current.map((advisory) =>
          advisory.id === id
            ? updated
            : advisory
        )
      );
    } catch (err) {
      setError(normalizeError(err).message);
    }
  }

  /**
   * Filter advisories.
   */
  const visibleAdvisories = filterType
    ? advisories.filter(
        (advisory) =>
          advisory.advisory_type === filterType
      )
    : advisories;

  /**
   * No farms.
   */
  if (farms.length === 0) {
    return (
      <EmptyState
        icon={Leaf}
        title="Add a farm first"
        description="Add a farm to receive automatic crop recommendations."
      />
    );
  }

  /**
   * No farm selected.
   */
  if (!selectedFarmId) {
    return (
      <EmptyState
        icon={Leaf}
        title="Select a farm"
        description="Select a farm to view automatic advisories."
      />
    );
  }

  return (
    <div className="flex flex-col gap-6">

      {/* Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">

        <div>
          <h1 className="text-2xl font-semibold text-gray-900">
            {filterType === 'irrigation'
              ? 'Irrigation Advisory'
              : 'Crop Advisories'}
          </h1>

          <p className="mt-1 text-sm text-gray-500">
            {filterType === 'irrigation'
              ? 'Automatic irrigation recommendations based on soil moisture and weather.'
              : 'Automatic recommendations based on crop stage, soil, weather, irrigation and nutrients.'}
          </p>
        </div>

        {/* Refresh button */}
        <button
          type="button"
          onClick={generateAutomaticAdvisories}
          disabled={isGenerating}
          className="inline-flex items-center justify-center gap-2 rounded-lg bg-primary-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-primary-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          <RefreshCw
            className={`h-4 w-4 ${
              isGenerating ? 'animate-spin' : ''
            }`}
          />

          {isGenerating
            ? 'Generating...'
            : 'Refresh Recommendations'}
        </button>
      </div>

      {/* Automatic information banner */}
      <div className="rounded-2xl border border-primary-100 bg-primary-50 p-4">
        <div className="flex gap-3">

          <CheckCircle2 className="mt-0.5 h-5 w-5 shrink-0 text-primary-600" />

          <div>
            <p className="font-medium text-primary-900">
              Automatic Advisory System
            </p>

            <p className="mt-1 text-sm text-primary-700">
              Recommendations are generated automatically
              from your crop lifecycle, soil conditions,
              soil moisture, weather and nutrient data.
            </p>
          </div>

        </div>
      </div>

      {/* Loading */}
      {isLoading || isGenerating ? (
        <div className="flex justify-center py-12">
          <LoadingSpinner size="lg" />
        </div>
      ) : error ? (
        <ErrorMessage
          message={error}
          onRetry={generateAutomaticAdvisories}
        />
      ) : visibleAdvisories.length === 0 ? (

        <EmptyState
          icon={Leaf}
          title={
            filterType === 'irrigation'
              ? 'No irrigation advisory available'
              : 'No advisories available'
          }
          description={
            filterType === 'irrigation'
              ? 'The system will show an irrigation recommendation when sufficient soil or weather data is available.'
              : 'The system will generate recommendations when crop, soil or weather data is available.'
          }
        />

      ) : (

        <div className="flex flex-col gap-4">

          {visibleAdvisories.map((advisory) => (
            <AdvisoryCard
              key={advisory.id}
              advisory={advisory}
              onResolve={handleResolve}
              onDismiss={handleDismiss}
            />
          ))}

        </div>
      )}

      {/* Crop information */}
      {crops.length > 0 && (
        <div className="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm">

          <div className="mb-4 flex items-center gap-2">
            <Leaf className="h-5 w-5 text-primary-600" />

            <h2 className="font-semibold text-gray-900">
              Monitored Crops
            </h2>
          </div>

          <div className="flex flex-wrap gap-2">
            {crops.map((crop) => (
              <span
                key={crop.id}
                className="rounded-full bg-gray-100 px-3 py-1.5 text-sm text-gray-700"
              >
                {crop.name}
              </span>
            ))}
          </div>

        </div>
      )}
    </div>
  );
}

/* =========================================================
   ADVISORY CARD
   ========================================================= */

function AdvisoryCard({
  advisory,
  onResolve,
  onDismiss,
}: {
  advisory: CropAdvisoryResponse;
  onResolve: (id: number) => void;
  onDismiss: (id: number) => void;
}) {
  const icon =
    advisory.advisory_type === 'irrigation'
      ? Droplets
      : advisory.advisory_type === 'weather'
        ? CloudRain
        : advisory.advisory_type === 'fertilizer'
          ? FlaskConical
          : advisory.advisory_type === 'crop_stage'
            ? Leaf
            : advisory.advisory_type === 'soil'
              ? FlaskConical
              : advisory.advisory_type === 'disease'
                ? AlertTriangle
                : Thermometer;

  const Icon = icon;

  return (
    <div className="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm">

      <div className="flex items-start justify-between gap-4">

        <div className="flex min-w-0 gap-4">

          {/* Icon */}
          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-primary-50">
            <Icon className="h-5 w-5 text-primary-600" />
          </div>

          {/* Content */}
          <div className="min-w-0">

            <div className="flex flex-wrap items-center gap-2">

              <h3 className="font-semibold text-gray-900">
                {advisory.title}
              </h3>

              <StatusBadge
                value={advisory.priority}
              />

              <StatusBadge
                value={advisory.status}
              />

            </div>

            <p className="mt-1 text-xs capitalize text-gray-400">
              {advisory.advisory_type.replace(
                '_',
                ' '
              )}
            </p>

          </div>
        </div>

        {/* Actions */}
        {advisory.status === 'active' && (
          <div className="flex shrink-0 gap-1">

            <button
              type="button"
              onClick={() =>
                onResolve(advisory.id)
              }
              title="Resolve advisory"
              className="rounded-lg p-2 text-gray-400 hover:bg-primary-50 hover:text-primary-600"
            >
              <CheckCircle2 className="h-4 w-4" />
            </button>

            <button
              type="button"
              onClick={() =>
                onDismiss(advisory.id)
              }
              title="Dismiss advisory"
              className="rounded-lg p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-700"
            >
              <X className="h-4 w-4" />
            </button>

          </div>
        )}

      </div>

      {/* Message */}
      <p className="mt-4 text-sm leading-6 text-gray-600">
        {advisory.message}
      </p>

      {/* Valid until */}
      {advisory.valid_until && (
        <p className="mt-3 text-xs text-gray-400">
          Valid until{' '}
          {new Date(
            advisory.valid_until
          ).toLocaleString()}
        </p>
      )}

    </div>
  );
}
