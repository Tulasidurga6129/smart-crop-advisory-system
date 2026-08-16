import { useEffect, useState } from 'react';
import { ShieldCheck } from 'lucide-react';
import { adminTest } from '../../api/auth';
import { LoadingSpinner } from '../../components/ui/LoadingSpinner';
import { ErrorMessage } from '../../components/ui/ErrorMessage';
import { normalizeError } from '../../api/client';

// The backend only exposes GET /api/v1/users/admin-test for role-based
// access — there are no admin list/management endpoints in the OpenAPI spec
// (no user list, farm list, etc). This page reflects that: it verifies
// access and shows the raw response rather than inventing admin CRUD screens
// the backend doesn't support.
export function Admin() {
  const [result, setResult] = useState<unknown>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    adminTest()
      .then(setResult)
      .catch((err) => setError(normalizeError(err).message))
      .finally(() => setIsLoading(false));
  }, []);

  return (
    <div className="mx-auto flex max-w-2xl flex-col gap-6">
      <div className="flex items-center gap-3">
        <div className="rounded-xl bg-earth-50 p-3">
          <ShieldCheck className="h-6 w-6 text-earth-600" />
        </div>
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">Admin</h1>
          <p className="text-sm text-gray-500">Role-gated access check</p>
        </div>
      </div>

      <div className="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm">
        {isLoading ? (
          <LoadingSpinner />
        ) : error ? (
          <ErrorMessage message={error} />
        ) : (
          <pre className="overflow-x-auto rounded-lg bg-gray-50 p-4 text-xs text-gray-700">
            {JSON.stringify(result, null, 2)}
          </pre>
        )}
      </div>

      <p className="text-xs text-gray-400">
        The backend doesn't currently expose broader admin management endpoints (user lists, farm oversight, etc.) — this
        page will grow as those are added.
      </p>
    </div>
  );
}
