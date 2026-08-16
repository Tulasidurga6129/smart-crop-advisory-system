import { Advisories } from '../advisories/Advisories';

// The backend has no dedicated irrigation-recommendation endpoint — the only
// relevant data is crop-advisories with advisory_type="irrigation". This page
// reuses the Advisories view filtered to that type rather than inventing a
// separate computed-irrigation endpoint that doesn't exist in the backend.
export function IrrigationAdvisory() {
  return <Advisories filterType="irrigation" />;
}
