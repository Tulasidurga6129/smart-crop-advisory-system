import { useEffect, useState } from 'react';
import { CheckCheck, Bell } from 'lucide-react';
import { getNotifications, markNotificationRead, markAllNotificationsRead, deleteNotification } from '../../api/notifications';
import type { NotificationResponse } from '../../types';
import { NotificationItem } from '../../components/notifications/NotificationItem';
import { LoadingSpinner } from '../../components/ui/LoadingSpinner';
import { ErrorMessage } from '../../components/ui/ErrorMessage';
import { EmptyState } from '../../components/ui/EmptyState';
import { normalizeError } from '../../api/client';

export function Notifications() {
  const [notifications, setNotifications] = useState<NotificationResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    setIsLoading(true);
    setError(null);
    try {
      const data = await getNotifications();
      setNotifications(data.slice().sort((a, b) => b.created_at.localeCompare(a.created_at)));
    } catch (err) {
      setError(normalizeError(err).message);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function handleMarkRead(id: number) {
    try {
      const updated = await markNotificationRead(id);
      setNotifications((list) => list.map((n) => (n.id === id ? updated : n)));
    } catch (err) {
      setError(normalizeError(err).message);
    }
  }

  async function handleDelete(id: number) {
    try {
      await deleteNotification(id);
      setNotifications((list) => list.filter((n) => n.id !== id));
    } catch (err) {
      setError(normalizeError(err).message);
    }
  }

  async function handleMarkAll() {
    try {
      await markAllNotificationsRead();
      await load();
    } catch (err) {
      setError(normalizeError(err).message);
    }
  }

  const unreadCount = notifications.filter((n) => !n.is_read).length;

  return (
    <div className="mx-auto flex max-w-2xl flex-col gap-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-900">Notifications</h1>
        {unreadCount > 0 && (
          <button
            onClick={handleMarkAll}
            className="inline-flex items-center gap-1.5 rounded-lg border border-gray-200 bg-white px-3 py-1.5 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            <CheckCheck className="h-4 w-4" /> Mark all as read
          </button>
        )}
      </div>

      {isLoading ? (
        <LoadingSpinner size="lg" />
      ) : error ? (
        <ErrorMessage message={error} onRetry={load} />
      ) : notifications.length === 0 ? (
        <EmptyState icon={Bell} title="You're all caught up" description="No notifications right now." />
      ) : (
        <div className="flex flex-col gap-3">
          {notifications.map((n) => (
            <NotificationItem key={n.id} notification={n} onMarkRead={handleMarkRead} onDelete={handleDelete} />
          ))}
        </div>
      )}
    </div>
  );
}
