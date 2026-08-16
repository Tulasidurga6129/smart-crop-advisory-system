const TONE_MAP: Record<string, string> = {
  active: 'bg-primary-100 text-primary-700',
  planned: 'bg-sky-100 text-sky-700',
  harvested: 'bg-earth-100 text-earth-700',
  resolved: 'bg-gray-100 text-gray-600',
  dismissed: 'bg-gray-100 text-gray-500',
  high: 'bg-red-100 text-red-700',
  medium: 'bg-amber-100 text-amber-700',
  low: 'bg-primary-100 text-primary-700',
  critical: 'bg-red-100 text-red-700',
};

export function StatusBadge({ value }: { value: string }) {
  const tone = TONE_MAP[value?.toLowerCase()] || 'bg-gray-100 text-gray-600';
  return (
    <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium capitalize ${tone}`}>
      {value}
    </span>
  );
}
