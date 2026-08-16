import type { ApiError } from '../api/client';

export function fieldError(apiError: ApiError | null, field: string): string | undefined {
  return apiError?.fieldErrors?.find((f) => f.field === field)?.message;
}
