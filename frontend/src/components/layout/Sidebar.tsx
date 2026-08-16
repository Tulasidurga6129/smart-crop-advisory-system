import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Tractor,
  Sprout,
  CloudSun,
  Sparkles,
  Bug,
  Droplets,
  LineChart,
  Wheat,
  ClipboardList,
  Bell,
  UserCircle,
  ShieldCheck,
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/farms', label: 'My Farms', icon: Tractor },
  { to: '/crops', label: 'Crops', icon: Sprout },
  { to: '/weather', label: 'Weather', icon: CloudSun },
  { to: '/recommendations', label: 'Recommendations', icon: Sparkles },
  { to: '/disease-detection', label: 'Disease Detection', icon: Bug },
  { to: '/irrigation', label: 'Irrigation', icon: Droplets },
  { to: '/crop-monitoring', label: 'Crop Monitoring', icon: LineChart },
  { to: '/yield-prediction', label: 'Yield Prediction', icon: Wheat },
  { to: '/advisories', label: 'Advisories', icon: ClipboardList },
  { to: '/notifications', label: 'Notifications', icon: Bell },
  { to: '/profile', label: 'Profile', icon: UserCircle },
];

export function Sidebar({ open, onClose }: { open: boolean; onClose: () => void }) {
  const { user } = useAuth();

  return (
    <>
      {open && <div className="fixed inset-0 z-30 bg-black/30 lg:hidden" onClick={onClose} />}
      <aside
        className={`fixed inset-y-0 left-0 z-40 w-64 transform border-r border-gray-100 bg-white transition-transform lg:static lg:translate-x-0 ${
          open ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex h-16 items-center gap-2 border-b border-gray-100 px-5">
          <div className="rounded-lg bg-primary-600 p-1.5">
            <Sprout className="h-5 w-5 text-white" />
          </div>
          <span className="font-semibold text-gray-900">Smart Crop Advisory</span>
        </div>
        <nav className="flex flex-col gap-0.5 overflow-y-auto p-3">
          {navItems.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              onClick={onClose}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition ${
                  isActive ? 'bg-primary-50 text-primary-700' : 'text-gray-600 hover:bg-gray-50'
                }`
              }
            >
              <Icon className="h-4.5 w-4.5" />
              {label}
            </NavLink>
          ))}
          {user?.role === 'admin' && (
            <NavLink
              to="/admin"
              onClick={onClose}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition ${
                  isActive ? 'bg-earth-50 text-earth-700' : 'text-gray-600 hover:bg-gray-50'
                }`
              }
            >
              <ShieldCheck className="h-4.5 w-4.5" />
              Admin
            </NavLink>
          )}
        </nav>
      </aside>
    </>
  );
}
