// All types below are transcribed directly from the backend's OpenAPI schema
// (components.schemas). Do not add fields that aren't in the spec.

// ---------- Auth / Users ----------
export interface UserCreate {
  name: string;
  email: string;
  password: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface UserResponse {
  id: number;
  name: string;
  email: string;
  role: string;
  is_active: boolean;
}

// The backend's /api/v1/auth/login response has no declared schema (schema: {}
// in the OpenAPI spec). We don't know the exact field names until we see a
// live response, so we type it loosely and parse defensively in api/auth.ts.
export interface LoginResponseUnknown {
  [key: string]: unknown;
}

// ---------- Farmer Profile ----------
export interface FarmerProfileCreate {
  phone?: string | null;
  address?: string | null;
  village?: string | null;
  district?: string | null;
  state?: string | null;
  land_area?: number | null;
  land_unit?: string | null;
  primary_crop?: string | null;
}

export type FarmerProfileUpdate = Partial<FarmerProfileCreate>;

export interface FarmerProfileResponse {
  id: number;
  user_id: number;
  phone: string | null;
  address: string | null;
  village: string | null;
  district: string | null;
  state: string | null;
  land_area: number | null;
  land_unit: string | null;
  primary_crop: string | null;
  created_at: string;
  updated_at: string;
}

// ---------- Farms ----------
export interface FarmCreate {
  farm_name: string;
  location?: string | null;
  village?: string | null;
  district?: string | null;
  state?: string | null;
  land_area: number;
  land_unit?: string; // default "acres"
  soil_type?: string | null;
  irrigation_type?: string | null;
  current_crop?: string | null;
}

export type FarmUpdate = Partial<FarmCreate>;

export interface FarmResponse {
  id: number;
  farmer_profile_id: number;
  farm_name: string;
  location: string | null;
  village: string | null;
  district: string | null;
  state: string | null;
  land_area: number;
  land_unit: string;
  soil_type: string | null;
  irrigation_type: string | null;
  current_crop: string | null;
}

// ---------- Crops ----------
export interface CropCreate {
  farm_id: number;
  name: string;
  variety?: string | null;
  season: string;
  sowing_date?: string | null; // date
  expected_harvest_date?: string | null; // date
  area?: number | null;
  status?: string; // default "planned"
}

export type CropUpdate = Partial<Omit<CropCreate, 'farm_id'>>;

export interface CropResponse {
  id: number;
  farm_id: number;
  name: string;
  variety: string | null;
  season: string;
  sowing_date: string | null;
  expected_harvest_date: string | null;
  area: number | null;
  status: string;
  // Optional — present on GET /crops/farm/{farm_id} responses, computed
  // server-side from sowing/harvest dates. Not present on every crop
  // endpoint, so treat as optional.
  crop_age_days?: number;
  growth_stage?: string;
  days_to_harvest?: number;
}

// ---------- Farm Conditions (soil) ----------
export interface FarmConditionCreate {
  soil_ph?: number | null;
  nitrogen?: number | null;
  phosphorus?: number | null;
  potassium?: number | null;
  organic_matter?: number | null;
  soil_moisture?: number | null;
  temperature?: number | null;
  humidity?: number | null;
  rainfall?: number | null;
  sunlight?: number | null;
}

export type FarmConditionUpdate = FarmConditionCreate;

export interface FarmConditionResponse extends FarmConditionCreate {
  id: number;
  farm_id: number;
  recorded_at: string;
  created_at: string;
}

// ---------- Weather ----------
export interface WeatherCreate {
  temperature?: number | null;
  humidity?: number | null;
  rainfall?: number | null;
  wind_speed?: number | null;
  weather_condition?: string | null;
  observed_at?: string | null; // date-time
}

export type WeatherUpdate = WeatherCreate;

export interface WeatherResponse extends WeatherCreate {
  id: number;
  farm_id: number;
  created_at: string;
}

// ---------- Crop Advisories ----------
export interface CropAdvisoryCreate {
  advisory_type: string;
  title: string;
  message: string;
  priority?: string; // default "medium"
  status?: string; // default "active"
  valid_until?: string | null; // date-time
  farm_id: number;
  crop_id: number;
}

export type CropAdvisoryUpdate = Partial<Omit<CropAdvisoryCreate, 'farm_id' | 'crop_id'>>;

export interface CropAdvisoryResponse {
  id: number;
  advisory_type: string;
  title: string;
  message: string;
  priority: string;
  status: string;
  valid_until: string | null;
  farm_id: number;
  crop_id: number;
  created_at: string;
  updated_at: string;
}

// ---------- Disease Detection ----------
// NOTE: the backend does NOT accept an image upload for this. It's a JSON
// record-entry endpoint — the caller supplies the diagnosis fields directly.
export interface DiseaseDetectionCreate {
  disease_name: string;
  confidence?: number | null; // 0-1
  severity?: string; // default "medium"
  symptoms?: string | null;
  recommended_treatment?: string | null;
  preventive_measures?: string | null;
  detection_source?: string; // default "manual"
  status?: string; // default "active"
  farm_id: number;
  crop_id: number;
}

export type DiseaseDetectionUpdate = Partial<Omit<DiseaseDetectionCreate, 'farm_id' | 'crop_id'>>;

export interface DiseaseDetectionResponse {
  id: number;
  disease_name: string;
  confidence: number | null;
  severity: string;
  symptoms: string | null;
  recommended_treatment: string | null;
  preventive_measures: string | null;
  detection_source: string;
  status: string;
  farm_id: number;
  crop_id: number;
  created_at: string;
  updated_at: string;
}

// ---------- Crop Monitoring ----------
export interface CropMonitoringCreate {
  crop_id: number;
  monitoring_date: string;
  growth_stage: string;
  plant_height?: number | null;
  crop_health?: string | null;
  pest_observed?: boolean; // default false
  disease_observed?: boolean; // default false
  observation_notes?: string | null;
}

export type CropMonitoringUpdate = Partial<Omit<CropMonitoringCreate, 'crop_id'>>;

export interface CropMonitoringResponse {
  id: number;
  crop_id: number;
  monitoring_date: string;
  growth_stage: string;
  plant_height: number | null;
  crop_health: string | null;
  pest_observed: boolean;
  disease_observed: boolean;
  observation_notes: string | null;
  created_at: string;
  updated_at: string;
}

// ---------- Notifications ----------
export interface NotificationCreate {
  notification_type: string;
  title: string;
  message: string;
  priority?: string; // default "medium"
  farm_id?: number | null;
  crop_id?: number | null;
}

export interface NotificationUpdate {
  notification_type?: string | null;
  title?: string | null;
  message?: string | null;
  priority?: string | null;
}

export interface NotificationResponse {
  id: number;
  notification_type: string;
  title: string;
  message: string;
  priority: string;
  user_id: number;
  farm_id: number | null;
  crop_id: number | null;
  is_read: boolean;
  created_at: string;
  read_at: string | null;
}

// ---------- Dashboard ----------
export interface DashboardFarmResponse {
  id: number;
  farm_name: string;
  location: string | null;
  village: string | null;
  district: string | null;
  state: string | null;
  land_area: number;
  land_unit: string;
  soil_type: string | null;
  irrigation_type: string | null;
  current_crop: string | null;
}

export interface DashboardCropResponse {
  id: number;
  name: string;
  variety: string | null;
  season: string;
  sowing_date: string | null;
  expected_harvest_date: string | null;
  area: number | null;
  status: string;
}

export interface DashboardConditionResponse {
  id: number;
  soil_ph: number | null;
  nitrogen: number | null;
  phosphorus: number | null;
  potassium: number | null;
  organic_matter: number | null;
  soil_moisture: number | null;
  temperature: number | null;
  humidity: number | null;
  rainfall: number | null;
  sunlight: number | null;
  recorded_at: string;
}

export interface DashboardWeatherResponse {
  id: number;
  temperature: number | null;
  humidity: number | null;
  rainfall: number | null;
  wind_speed: number | null;
  weather_condition: string | null;
  observed_at: string;
}

export interface DashboardAdvisoryResponse {
  id: number;
  crop_id: number;
  advisory_type: string;
  title: string;
  message: string;
  priority: string;
  status: string;
  valid_until: string | null;
  created_at: string;
}

export interface DashboardSummaryResponse {
  high: number;
  medium: number;
  low: number;
  total: number;
  top_priority: string | null;
}

export interface FarmDashboardResponse {
  farm: DashboardFarmResponse;
  crops: DashboardCropResponse[];
  latest_condition: DashboardConditionResponse | null;
  latest_weather: DashboardWeatherResponse | null;
  active_advisories: DashboardAdvisoryResponse[];
  summary: DashboardSummaryResponse;
}

// ---------- Yield Prediction ----------
// GET /yield-predictions/crop/{crop_id} — authenticated. The backend looks
// up the crop, farm, and weather/climate data itself; the frontend only
// supplies the crop_id. All climate fields below are backend-derived and
// must never be collected from the farmer.
export interface YieldPredictionResponse {
  crop_id: number;
  farm_id: number;
  crop: string;
  crop_year: number;
  weather_year: number;
  season: string;
  state: string;
  area: number;
  annual_rainfall: number;
  avg_temperature: number;
  max_temperature: number;
  min_temperature: number;
  predicted_yield: number;
}

// ---------- Recommendations ----------
// POST /recommendations/{crop_id} has no declared response schema. Backend
// is expected to return some JSON payload; shape is unknown until observed.
export interface RecommendationAdvisory {
  id: number;
  farm_id: number;
  crop_id: number;
  advisory_type: string;
  title: string;
  message: string;
  priority: string;
  status: string;
  valid_until?: string | null;
  created_at?: string | null;
}

export type RecommendationResponseUnknown = RecommendationAdvisory[];

// ---------- Errors ----------
export interface ValidationError {
  loc: (string | number)[];
  msg: string;
  type: string;
}

export interface HTTPValidationError {
  detail: ValidationError[];
}
