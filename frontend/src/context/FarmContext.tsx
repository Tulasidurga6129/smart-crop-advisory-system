import { createContext, useContext, useState, useEffect, useCallback, type ReactNode } from 'react';
import { getMyFarms } from '../api/farms';
import type { FarmResponse } from '../types';
import { useAuth } from './AuthContext';

interface FarmContextValue {
  farms: FarmResponse[];
  selectedFarmId: number | null;
  setSelectedFarmId: (id: number) => void;
  isLoading: boolean;
  error: string | null;
  refresh: () => Promise<void>;
}

const FarmContext = createContext<FarmContextValue | undefined>(undefined);

const SELECTED_FARM_KEY = 'sca_selected_farm_id';

export function FarmProvider({ children }: { children: ReactNode }) {
  const { isAuthenticated } = useAuth();
  const [farms, setFarms] = useState<FarmResponse[]>([]);
  const [selectedFarmId, setSelectedFarmIdState] = useState<number | null>(() => {
    const stored = localStorage.getItem(SELECTED_FARM_KEY);
    return stored ? Number(stored) : null;
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const setSelectedFarmId = useCallback((id: number) => {
    setSelectedFarmIdState(id);
    localStorage.setItem(SELECTED_FARM_KEY, String(id));
  }, []);

  const refresh = useCallback(async () => {
    if (!isAuthenticated) return;
    setIsLoading(true);
    setError(null);
    try {
      const data = await getMyFarms();
      setFarms(data);
      setSelectedFarmIdState((current) => {
        if (current && data.some((f) => f.id === current)) return current;
        return data[0]?.id ?? null;
      });
    } catch {
      setError('Could not load your farms.');
    } finally {
      setIsLoading(false);
    }
  }, [isAuthenticated]);

  useEffect(() => {
    if (isAuthenticated) refresh();
    else setFarms([]);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isAuthenticated]);

  return (
    <FarmContext.Provider value={{ farms, selectedFarmId, setSelectedFarmId, isLoading, error, refresh }}>
      {children}
    </FarmContext.Provider>
  );
}

export function useFarms() {
  const ctx = useContext(FarmContext);
  if (!ctx) throw new Error('useFarms must be used within FarmProvider');
  return ctx;
}
