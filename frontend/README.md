# Smart Crop Advisory System — Frontend

A React + TypeScript + Tailwind CSS frontend for the Smart Crop Advisory System FastAPI backend, built directly against the backend's real `openapi.json` (37 endpoints).

## Tech stack

- React 19 + Vite 8 + TypeScript
- Tailwind CSS v4 (`@tailwindcss/vite`)
- React Router v6 for routing
- Axios for API communication
- lucide-react for icons, recharts available for charts

## Setup

```bash
cd smart-crop-frontend
npm install
cp .env.example .env   # then edit VITE_API_BASE_URL if your backend isn't on 127.0.0.1:8000
npm run dev
```

The app runs at `http://localhost:5173` by default. Make sure the FastAPI backend (with CORS allowing this origin) is running at the URL set in `.env`.

### Build

```bash
npm run build     # type-checks (tsc -b) then builds to dist/
npm run preview   # serve the production build locally
```

## Environment variables

| Variable | Description | Default |
|---|---|---|
| `VITE_API_BASE_URL` | Base URL of the FastAPI backend. Never hardcoded elsewhere in the app — every API call goes through `src/api/client.ts`. | `http://127.0.0.1:8000` |

## Authentication

- `POST /api/v1/auth/register`, `POST /api/v1/auth/login` — no auth required
- All other endpoints (except yield prediction — see below) require a `Bearer` token, attached automatically by an Axios request interceptor once logged in
- The token is stored in `localStorage` under `sca_auth_token`
- A response interceptor detects `401` responses and logs the user out automatically
- **Important caveat:** the backend's `/api/v1/auth/login` response has no declared schema in the OpenAPI spec (`schema: {}`), so the exact JSON field holding the token wasn't knowable from the spec alone. `src/api/auth.ts` tries the common field names (`access_token`, `token`, `accessToken`, `jwt`, `auth_token`) in order and throws a clear error (with the raw response logged to the console) if none match. **If your backend uses a different field name, update the `candidateKeys` array in `src/api/auth.ts`.**

## Pages

| Route | Page |
|---|---|
| `/` | Landing page |
| `/login`, `/register` | Auth |
| `/dashboard` | Farm dashboard (`GET /dashboard/farm/{id}`) |
| `/farms`, `/farms/new`, `/farms/:id`, `/farms/:id/edit` | Farm CRUD |
| `/farms/:id/conditions/new` | Log soil conditions |
| `/farms/:id/weather/new` | Log a weather reading |
| `/crops`, `/crops/new`, `/crops/:id` | Crop CRUD |
| `/weather` | Weather log for the selected farm |
| `/recommendations` | Generate a crop recommendation (see note below) |
| `/disease-detection` | Disease record list + manual entry form (see note below) |
| `/irrigation` | Irrigation-type advisories (filtered view — see note below) |
| `/crop-monitoring` | Growth-stage monitoring timeline |
| `/yield-prediction` | Public yield prediction form |
| `/advisories` | Full advisory CRUD (create, resolve, dismiss, delete) |
| `/notifications` | Notification center |
| `/profile` | Farmer profile |
| `/admin` | Role-gated access check (admin role only) |

## Known deviations from a "typical" crop-advisory app — and why

These aren't oversights; they reflect what the actual backend (per its OpenAPI spec) supports today:

1. **Disease Detection is a manual record-entry form, not an image upload.** `DiseaseDetectionCreate` takes `disease_name`, `farm_id`, `crop_id` as required JSON fields — there's no file/image parameter in the spec. The UI matches: enter symptoms/diagnosis directly rather than uploading a photo.
2. **There's one generic recommendation endpoint, not separate crop + fertilizer endpoints.** `POST /recommendations/{crop_id}` takes only a crop ID (no body) and its response schema isn't declared. The single "Recommendations" page covers what the brief called both "Crop Recommendation" and "Fertilizer Recommendation," and renders whatever JSON key/value pairs the backend returns.
3. **There's no dedicated irrigation-recommendation endpoint.** The `/irrigation` page is a filtered view of `crop-advisories` (`advisory_type=irrigation`) — the backend's real irrigation-related data model.
4. **Yield Prediction requires no authentication** in the spec, so it's reachable without logging in, at `/yield-prediction`.
5. **Admin functionality is minimal by design.** The spec only exposes `GET /api/v1/users/admin-test` — no user/farm management endpoints exist yet, so the Admin page only verifies role-gated access rather than offering CRUD screens for data the backend doesn't expose.
6. **A few response schemas are untyped in the spec** (`login`, `/`, `/health`, `/api/v1/users/admin-test`, `/recommendations/{crop_id}`). Where this matters for parsing (login), the code is defensive and logs the raw payload for debugging. The Recommendation page renders arbitrary JSON generically for the same reason.

## API layer

One module per resource under `src/api/`, each calling the exact backend path/method from the spec — no invented endpoints:

```
src/api/
  client.ts            axios instance, auth header injection, error normalization
  auth.ts               register, login, getMe, adminTest
  farms.ts               farm CRUD
  crops.ts                crop CRUD
  conditions.ts            soil condition CRUD
  weather.ts                weather log CRUD
  advisories.ts               advisory CRUD + resolve/dismiss
  disease.ts                    disease detection CRUD
  recommendations.ts              POST /recommendations/{crop_id}
  dashboard.ts                     GET /dashboard/farm/{id}
  monitoring.ts                     crop monitoring CRUD
  notifications.ts                   notification CRUD + read/read-all
  yieldPrediction.ts                  POST /yield-prediction/predict
  profile.ts                           farmer profile CRUD
```

## Error & loading handling

- Every API-backed page has loading, success, empty, and error states
- `normalizeError()` in `src/api/client.ts` turns 400/401/403/404/422/500/network errors into user-friendly messages without leaking backend stack traces
- 422 validation errors are mapped to per-field messages and shown next to the relevant form input where applicable

## Notes for further development

- If you confirm the real shape of the untyped responses (login, recommendations, `/`, `/health`, admin-test) against a live backend, update the corresponding types in `src/types/index.ts` and the parsing logic in `src/api/auth.ts` / `RecommendationCard.tsx`.
- If admin management endpoints are added to the backend later, extend `src/pages/admin/Admin.tsx` and add the corresponding API module.

## Re-verification log

Re-audited against `openapi.json` a second time: all 37 endpoint calls in `src/api/*.ts` (paths, methods, path params, request bodies) match the spec exactly, and every schema field in `src/types/index.ts` was diffed against a fresh schema dump with no differences found. One outdated code comment (in `src/pages/recommendations/Recommendations.tsx`) referring to the crop-recommendation ML model as "not yet merged" was removed, since that module is now complete on the backend — the page still correctly reflects that crop and fertilizer guidance share a single `POST /recommendations/{crop_id}` endpoint, which is the real backend structure, not something invented by the frontend. No mock, sample, or hardcoded agricultural data was found anywhere in API-driven pages.
