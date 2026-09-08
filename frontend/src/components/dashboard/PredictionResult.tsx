import { Wheat } from 'lucide-react';

export function PredictionResult({
  predictedYield,
  unit = 'tonnes / hectare',
}: {
  predictedYield: number;
  unit?: string;
}) {
  return (
    <div className="flex flex-col items-center gap-3 rounded-2xl border border-earth-200 bg-gradient-to-br from-earth-50 to-white p-8 text-center shadow-sm">
      <div className="rounded-full bg-earth-100 p-3">
        <Wheat className="h-8 w-8 text-earth-600" />
      </div>
      <p className="text-sm font-medium uppercase tracking-wide text-gray-400">Predicted Yield</p>
      <p className="text-4xl font-bold text-earth-700">
        {predictedYield.toLocaleString(undefined, { maximumFractionDigits: 2 })}
        {unit && <span className="ml-2 text-base font-medium text-gray-400">{unit}</span>}
      </p>
      <p className="text-xs text-gray-400">As returned by the yield prediction model</p>
    </div>
  );
}
