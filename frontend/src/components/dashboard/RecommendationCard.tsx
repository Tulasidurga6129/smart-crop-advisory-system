import { Sparkles } from 'lucide-react';
import type { RecommendationResponseUnknown } from '../../types';

function humanizeKey(key: string) {
  return key.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
}

function renderValue(value: unknown): string {
  if (value == null) return '—';
  if (typeof value === 'object') return JSON.stringify(value);
  return String(value);
}

export function RecommendationCard({
  data,
}: {
  data: RecommendationResponseUnknown;
}) {
  if (!data || data.length === 0) {
    return (
      <div className="rounded-2xl border border-gray-100 bg-white p-6 text-center text-sm text-gray-400 shadow-sm">
        No recommendations available for this crop yet.
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {data.map((recommendation, index) => {
        const entries = Object.entries(recommendation);

        return (
          <div
            key={recommendation.id ?? index}
            className="rounded-2xl border border-primary-100 bg-primary-50/40 p-6 shadow-sm"
          >
            <div className="mb-4 flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-primary-600" />

              <h3 className="font-semibold text-primary-800">
                {recommendation.title}
              </h3>
            </div>

            <p className="mb-4 text-sm leading-6 text-gray-700">
              {recommendation.message}
            </p>

            <dl className="grid gap-3 sm:grid-cols-2">
              {entries
                .filter(([key]) => key !== 'title' && key !== 'message')
                .map(([key, value]) => (
                  <div
                    key={key}
                    className="rounded-xl bg-white p-3 shadow-sm"
                  >
                    <dt className="text-xs font-medium uppercase tracking-wide text-gray-400">
                      {humanizeKey(key)}
                    </dt>

                    <dd className="mt-1 break-words text-sm font-medium text-gray-800">
                      {renderValue(value)}
                    </dd>
                  </div>
                ))}
            </dl>
          </div>
        );
      })}
    </div>
  );
}