import { Bell, Check, Trash2 } from 'lucide-react';
import type { NotificationResponse } from '../../types';
import { StatusBadge } from '../ui/StatusBadge';

export function NotificationItem({
  notification,
  onMarkRead,
  onDelete,
}: {
  notification: NotificationResponse;
  onMarkRead: (id: number) => void;
  onDelete: (id: number) => void;
}) {
  return (
    <div
      className={`flex items-start gap-3 rounded-xl border p-4 shadow-sm ${
        notification.is_read ? 'border-gray-100 bg-white' : 'border-primary-200 bg-primary-50/40'
      }`}
    >
      <div className={`mt-0.5 rounded-full p-2 ${notification.is_read ? 'bg-gray-100 text-gray-400' : 'bg-primary-100 text-primary-600'}`}>
        <Bell className="h-4 w-4" />
      </div>
      <div className="min-w-0 flex-1">
        <div className="flex items-center gap-2">
          <p className="truncate font-medium text-gray-900">{notification.title}</p>
          <StatusBadge value={notification.priority} />
        </div>
        <p className="mt-1 text-sm text-gray-600">{notification.message}</p>
        <p className="mt-1 text-xs text-gray-400">
          {notification.notification_type} · {new Date(notification.created_at).toLocaleString()}
        </p>
      </div>
      <div className="flex shrink-0 gap-1">
        {!notification.is_read && (
          <button
            onClick={() => onMarkRead(notification.id)}
            title="Mark as read"
            className="rounded-lg p-2 text-gray-400 hover:bg-primary-50 hover:text-primary-600"
          >
            <Check className="h-4 w-4" />
          </button>
        )}
        <button
          onClick={() => onDelete(notification.id)}
          title="Delete"
          className="rounded-lg p-2 text-gray-400 hover:bg-red-50 hover:text-red-600"
        >
          <Trash2 className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}
