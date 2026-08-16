import { Menu, Bell, LogOut, ChevronDown } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useFarms } from '../../context/FarmContext';
import { useEffect, useState } from 'react';
import { getNotifications } from '../../api/notifications';

export function Navbar({ onMenuClick }: { onMenuClick: () => void }) {
  const { user, logout } = useAuth();
  const { farms, selectedFarmId, setSelectedFarmId } = useFarms();
  const navigate = useNavigate();
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    let mounted = true;
    getNotifications()
      .then((list) => {
        if (mounted) setUnreadCount(list.filter((n) => !n.is_read).length);
      })
      .catch(() => {});
    return () => {
      mounted = false;
    };
  }, []);

  return (
    <header className="sticky top-0 z-20 flex h-16 items-center justify-between gap-4 border-b border-gray-100 bg-white/90 px-4 backdrop-blur">
      <div className="flex items-center gap-3">
        <button onClick={onMenuClick} className="rounded-lg p-2 text-gray-500 hover:bg-gray-100 lg:hidden">
          <Menu className="h-5 w-5" />
        </button>
        {farms.length > 0 && (
          <div className="relative">
            <select
              value={selectedFarmId ?? ''}
              onChange={(e) => setSelectedFarmId(Number(e.target.value))}
              className="appearance-none rounded-lg border border-gray-200 bg-white py-1.5 pl-3 pr-8 text-sm font-medium text-gray-700 outline-none focus:border-primary-400"
            >
              {farms.map((f) => (
                <option key={f.id} value={f.id}>
                  {f.farm_name}
                </option>
              ))}
            </select>
            <ChevronDown className="pointer-events-none absolute right-2 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-gray-400" />
          </div>
        )}
      </div>

      <div className="flex items-center gap-3">
        <button
          onClick={() => navigate('/notifications')}
          className="relative rounded-lg p-2 text-gray-500 hover:bg-gray-100"
        >
          <Bell className="h-5 w-5" />
          {unreadCount > 0 && (
            <span className="absolute -right-0.5 -top-0.5 flex h-4 w-4 items-center justify-center rounded-full bg-red-500 text-[10px] font-bold text-white">
              {unreadCount > 9 ? '9+' : unreadCount}
            </span>
          )}
        </button>
        <div className="hidden text-right sm:block">
          <p className="text-sm font-medium text-gray-800">{user?.name}</p>
          <p className="text-xs text-gray-400">{user?.role}</p>
        </div>
        <button onClick={logout} className="rounded-lg p-2 text-gray-500 hover:bg-red-50 hover:text-red-600" title="Logout">
          <LogOut className="h-5 w-5" />
        </button>
      </div>
    </header>
  );
}
