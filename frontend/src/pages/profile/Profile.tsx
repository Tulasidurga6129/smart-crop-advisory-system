import { useEffect, useState, type FormEvent } from 'react';
import { UserCircle } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { getMyProfile, createMyProfile, updateMyProfile } from '../../api/profile';
import type { FarmerProfileResponse, FarmerProfileCreate } from '../../types';
import { FormInput } from '../../components/ui/FormInput';
import { LoadingSpinner } from '../../components/ui/LoadingSpinner';
import { normalizeError, type ApiError } from '../../api/client';

export function Profile() {
  const { user } = useAuth();
  const [profile, setProfile] = useState<FarmerProfileResponse | null>(null);
  const [exists, setExists] = useState(true);
  const [isLoading, setIsLoading] = useState(true);
  const [form, setForm] = useState<FarmerProfileCreate>({});
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    getMyProfile()
      .then((data) => {
        setProfile(data);
        setForm({
          phone: data.phone ?? '',
          address: data.address ?? '',
          village: data.village ?? '',
          district: data.district ?? '',
          state: data.state ?? '',
          land_area: data.land_area ?? undefined,
          land_unit: data.land_unit ?? '',
          primary_crop: data.primary_crop ?? '',
        });
      })
      .catch((err) => {
        // A 404 here plausibly means no profile has been created yet.
        if (normalizeError(err).status === 404) {
          setExists(false);
        } else {
          setError(normalizeError(err));
        }
      })
      .finally(() => setIsLoading(false));
  }, []);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setSuccess(false);
    setSaving(true);
    try {
      const result = exists ? await updateMyProfile(form) : await createMyProfile(form);
      setProfile(result);
      setExists(true);
      setSuccess(true);
    } catch (err) {
      setError(normalizeError(err));
    } finally {
      setSaving(false);
    }
  }

  if (isLoading) return <LoadingSpinner size="lg" />;

  return (
    <div className="mx-auto flex max-w-2xl flex-col gap-6">
      <div className="flex items-center gap-3">
        <div className="rounded-xl bg-primary-50 p-3">
          <UserCircle className="h-6 w-6 text-primary-600" />
        </div>
        <div>
          <h1 className="text-2xl font-semibold text-gray-900">{user?.name}</h1>
          <p className="text-sm text-gray-500">{user?.email}</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4 rounded-2xl border border-gray-100 bg-white p-6 shadow-sm">
        <h2 className="font-semibold text-gray-900">Farmer Profile</h2>
        <div className="grid gap-4 sm:grid-cols-2">
          <FormInput label="Phone" value={form.phone ?? ''} onChange={(e) => setForm((f) => ({ ...f, phone: e.target.value }))} />
          <FormInput
            label="Primary crop"
            value={form.primary_crop ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, primary_crop: e.target.value }))}
          />
        </div>
        <FormInput label="Address" value={form.address ?? ''} onChange={(e) => setForm((f) => ({ ...f, address: e.target.value }))} />
        <div className="grid gap-4 sm:grid-cols-3">
          <FormInput label="Village" value={form.village ?? ''} onChange={(e) => setForm((f) => ({ ...f, village: e.target.value }))} />
          <FormInput label="District" value={form.district ?? ''} onChange={(e) => setForm((f) => ({ ...f, district: e.target.value }))} />
          <FormInput label="State" value={form.state ?? ''} onChange={(e) => setForm((f) => ({ ...f, state: e.target.value }))} />
        </div>
        <div className="grid gap-4 sm:grid-cols-2">
          <FormInput
            label="Land area"
            type="number"
            step="any"
            value={form.land_area ?? ''}
            onChange={(e) => setForm((f) => ({ ...f, land_area: e.target.value === '' ? undefined : Number(e.target.value) }))}
          />
          <FormInput label="Land unit" value={form.land_unit ?? ''} onChange={(e) => setForm((f) => ({ ...f, land_unit: e.target.value }))} />
        </div>
        {error && <p className="text-sm text-red-600">{error.message}</p>}
        {success && <p className="text-sm text-primary-600">Profile saved.</p>}
        <button
          type="submit"
          disabled={saving}
          className="rounded-lg bg-primary-600 py-2.5 text-sm font-medium text-white hover:bg-primary-700 disabled:opacity-60"
        >
          {saving ? 'Saving…' : exists ? 'Save Changes' : 'Create Profile'}
        </button>
      </form>

      {profile && (
        <p className="text-xs text-gray-400">
          Profile last updated {new Date(profile.updated_at).toLocaleString()}
        </p>
      )}
    </div>
  );
}
