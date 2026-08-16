import { BrowserRouter, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { FarmProvider } from './context/FarmContext';
import { ProtectedRoute } from './components/layout/ProtectedRoute';
import { AppLayout } from './components/layout/AppLayout';

import { Landing } from './pages/Landing';
import { Login } from './pages/auth/Login';
import { Register } from './pages/auth/Register';
import { Dashboard } from './pages/Dashboard';
import { Profile } from './pages/profile/Profile';

import { FarmsList } from './pages/farms/FarmsList';
import { AddFarm } from './pages/farms/AddFarm';
import { EditFarm } from './pages/farms/EditFarm';
import { FarmDetails } from './pages/farms/FarmDetails';
import { AddFarmCondition } from './pages/farms/AddFarmCondition';

import { CropsList } from './pages/crops/CropsList';
import { AddCrop } from './pages/crops/AddCrop';
import { CropDetails } from './pages/crops/CropDetails';

import { WeatherPage } from './pages/weather/WeatherPage';
import { AddWeather } from './pages/weather/AddWeather';

import { Recommendations } from './pages/recommendations/Recommendations';
import { DiseaseDetection } from './pages/disease/DiseaseDetection';
import { CropMonitoring } from './pages/monitoring/CropMonitoring';
import { YieldPrediction } from './pages/yield/YieldPrediction';
import { Advisories } from './pages/advisories/Advisories';
import { IrrigationAdvisory } from './pages/advisories/IrrigationAdvisory';
import { Notifications } from './pages/notifications/Notifications';
import { Admin } from './pages/admin/Admin';

// Simple shell (no sidebar/farm-selector) for the one page that works
// without authentication, since /yield-prediction/predict has no auth
// requirement on the backend.
function PublicShell() {
  return (
    <div className="min-h-screen bg-gray-50 p-4 sm:p-6">
      <Outlet />
    </div>
  );
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route element={<PublicShell />}>
        <Route path="/yield-prediction" element={<YieldPrediction />} />
      </Route>

      <Route element={<ProtectedRoute />}>
        <Route element={<AppLayout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile" element={<Profile />} />

          <Route path="/farms" element={<FarmsList />} />
          <Route path="/farms/new" element={<AddFarm />} />
          <Route path="/farms/:farmId" element={<FarmDetails />} />
          <Route path="/farms/:farmId/edit" element={<EditFarm />} />
          <Route path="/farms/:farmId/conditions/new" element={<AddFarmCondition />} />
          <Route path="/farms/:farmId/weather/new" element={<AddWeather />} />

          <Route path="/crops" element={<CropsList />} />
          <Route path="/crops/new" element={<AddCrop />} />
          <Route path="/crops/:cropId" element={<CropDetails />} />

          <Route path="/weather" element={<WeatherPage />} />
          <Route path="/recommendations" element={<Recommendations />} />
          <Route path="/disease-detection" element={<DiseaseDetection />} />
          <Route path="/irrigation" element={<IrrigationAdvisory />} />
          <Route path="/crop-monitoring" element={<CropMonitoring />} />
          <Route path="/advisories" element={<Advisories />} />
          <Route path="/notifications" element={<Notifications />} />
        </Route>

        <Route element={<ProtectedRoute adminOnly />}>
          <Route element={<AppLayout />}>
            <Route path="/admin" element={<Admin />} />
          </Route>
        </Route>
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <FarmProvider>
          <AppRoutes />
        </FarmProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}
