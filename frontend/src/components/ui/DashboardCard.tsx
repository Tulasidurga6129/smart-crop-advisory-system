import type { LucideIcon } from 'lucide-react';
import type { ReactNode } from 'react';

export function DashboardCard({
  icon: Icon,
  label,
  value,
  sub,
  tone = 'primary',
}: {
  icon: LucideIcon;
  label: string;
  value: ReactNode;
  sub?: string;
  tone?: 'primary' | 'earth' | 'sky' | 'red' | 'amber';
}) {
  const tones: Record<string, string> = {
    primary: 'bg-primary-50 text-primary-600',
    earth: 'bg-earth-50 text-earth-600',
    sky: 'bg-sky-100 text-sky-600',
    red: 'bg-red-50 text-red-600',
    amber: 'bg-amber-50 text-amber-600',
  };
  return (
    <div className="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm">
      <div className="flex items-center gap-3">
        <div className={`rounded-xl p-2.5 ${tones[tone]}`}>
          <Icon className="h-5 w-5" />
        </div>
        <div>
          <p className="text-xs font-medium uppercase tracking-wide text-gray-400">{label}</p>
          <p className="text-xl font-semibold text-gray-900">{value}</p>
        </div>
      </div>
      {sub && <p className="mt-2 text-xs text-gray-400">{sub}</p>}
    </div>
  );
}
