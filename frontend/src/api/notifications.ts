import apiClient from './client';
import type { NotificationCreate, NotificationUpdate, NotificationResponse } from '../types';

export async function getNotifications(): Promise<NotificationResponse[]> {
  const { data } = await apiClient.get<NotificationResponse[]>('/notifications');
  return data;
}

export async function createNotification(payload: NotificationCreate): Promise<NotificationResponse> {
  const { data } = await apiClient.post<NotificationResponse>('/notifications', payload);
  return data;
}

export async function getNotification(notificationId: number): Promise<NotificationResponse> {
  const { data } = await apiClient.get<NotificationResponse>(`/notifications/${notificationId}`);
  return data;
}

export async function updateNotification(notificationId: number, payload: NotificationUpdate): Promise<NotificationResponse> {
  const { data } = await apiClient.put<NotificationResponse>(`/notifications/${notificationId}`, payload);
  return data;
}

export async function deleteNotification(notificationId: number): Promise<void> {
  await apiClient.delete(`/notifications/${notificationId}`);
}

export async function markNotificationRead(notificationId: number): Promise<NotificationResponse> {
  const { data } = await apiClient.patch<NotificationResponse>(`/notifications/${notificationId}/read`);
  return data;
}

export async function markAllNotificationsRead(): Promise<unknown> {
  const { data } = await apiClient.patch('/notifications/read-all');
  return data;
}
