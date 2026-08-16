import apiClient from './client';
import type { UserCreate, UserLogin, UserResponse, LoginResponseUnknown } from '../types';

export async function register(payload: UserCreate): Promise<UserResponse> {
  const { data } = await apiClient.post<UserResponse>('/api/v1/auth/register', payload);
  return data;
}

// The backend declares no response schema for /login (schema: {} in the
// OpenAPI spec), so we don't know the exact token field name in advance.
// We accept whatever comes back and try the common shapes a FastAPI+JWT
// backend would use, in order of likelihood. If none match, we surface the
// raw payload in the console so it can be inspected and this function
// updated with the real field name.
export async function login(payload: UserLogin): Promise<{ token: string; raw: LoginResponseUnknown }> {
  const { data } = await apiClient.post<LoginResponseUnknown>('/api/v1/auth/login', payload);

  const candidateKeys = ['access_token', 'token', 'accessToken', 'jwt', 'auth_token'];
  for (const key of candidateKeys) {
    const value = (data as Record<string, unknown>)[key];
    if (typeof value === 'string' && value.length > 0) {
      return { token: value, raw: data };
    }
  }

  // eslint-disable-next-line no-console
  console.warn(
    '[auth] Could not find a recognizable token field in the /api/v1/auth/login response. ' +
      'Raw response logged below — update src/api/auth.ts candidateKeys with the real field name.',
    data
  );
  throw new Error(
    "Login succeeded on the server but the response format wasn't recognized. Check the browser console for the raw response and update the frontend's token parsing."
  );
}

export async function getMe(): Promise<UserResponse> {
  const { data } = await apiClient.get<UserResponse>('/api/v1/users/me');
  return data;
}

export async function adminTest(): Promise<unknown> {
  const { data } = await apiClient.get('/api/v1/users/admin-test');
  return data;
}
