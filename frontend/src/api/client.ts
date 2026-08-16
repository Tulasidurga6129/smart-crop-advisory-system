import axios, { AxiosError } from 'axios';

// Base URL is configurable via env var so it's never hardcoded across the app.
const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export const TOKEN_STORAGE_KEY = 'sca_auth_token';

export const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Attach the bearer token to every request if we have one.
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_STORAGE_KEY);
  if (token) {
    config.headers = config.headers || {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Normalize error responses (400/401/403/404/422/500/network) into a
// consistent shape the UI can render without leaking raw stack traces.
export interface ApiError {
  status: number | null;
  message: string;
  fieldErrors?: { field: string; message: string }[];
}

export function normalizeError(error: unknown): ApiError {
  if (axios.isAxiosError(error)) {
    const err = error as AxiosError<any>;
    const status = err.response?.status ?? null;
    const data = err.response?.data;

    if (!err.response) {
      return { status: null, message: 'Network error — could not reach the server. Check your connection or that the backend is running.' };
    }

    if (status === 422 && data?.detail && Array.isArray(data.detail)) {
      return {
        status,
        message: 'Please check the highlighted fields.',
        fieldErrors: data.detail.map((d: any) => ({
          field: Array.isArray(d.loc) ? String(d.loc[d.loc.length - 1]) : 'field',
          message: d.msg || 'Invalid value',
        })),
      };
    }

    if (status === 401) {
      return { status, message: 'Your session has expired. Please log in again.' };
    }
    if (status === 403) {
      return { status, message: "You don't have permission to do that." };
    }
    if (status === 404) {
      return { status, message: 'The requested item could not be found.' };
    }
    if (status === 500) {
      return { status, message: 'Something went wrong on the server. Please try again shortly.' };
    }

    // Fallback: try to surface a readable message from common shapes.
    const msg =
      (typeof data?.detail === 'string' && data.detail) ||
      (typeof data?.message === 'string' && data.message) ||
      'Something went wrong. Please try again.';
    return { status, message: msg };
  }

  return { status: null, message: 'An unexpected error occurred.' };
}

let onUnauthorized: (() => void) | null = null;
export function registerUnauthorizedHandler(fn: () => void) {
  onUnauthorized = fn;
}

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (axios.isAxiosError(error) && error.response?.status === 401) {
      onUnauthorized?.();
    }
    return Promise.reject(error);
  }
);

export default apiClient;
