import { Link } from 'react-router-dom';
import { Sprout, CloudSun, Bug, LineChart, Wheat, ArrowRight } from 'lucide-react';

const features = [
  { icon: Sprout, title: 'Crop Recommendations', desc: 'Get crop guidance tailored to each field you manage.' },
  { icon: CloudSun, title: 'Weather Tracking', desc: 'Log and review weather conditions across your farms.' },
  { icon: Bug, title: 'Disease Detection', desc: 'Record and track disease diagnoses per crop.' },
  { icon: LineChart, title: 'Crop Monitoring', desc: 'Follow growth stages and health over time.' },
  { icon: Wheat, title: 'Yield Prediction', desc: 'Estimate yield using season, soil and weather inputs.' },
];

export function Landing() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 via-white to-white">
      <header className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
        <div className="flex items-center gap-2">
          <div className="rounded-lg bg-primary-600 p-1.5">
            <Sprout className="h-5 w-5 text-white" />
          </div>
          <span className="font-semibold text-gray-900">Smart Crop Advisory</span>
        </div>
        <div className="flex items-center gap-3">
          <Link to="/login" className="text-sm font-medium text-gray-600 hover:text-gray-900">
            Log in
          </Link>
          <Link
            to="/register"
            className="rounded-lg bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-700"
          >
            Get started
          </Link>
        </div>
      </header>

      <section className="mx-auto max-w-4xl px-6 py-20 text-center">
        <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">
          Smarter farming decisions, <span className="text-primary-600">one dashboard away</span>
        </h1>
        <p className="mx-auto mt-5 max-w-2xl text-lg text-gray-500">
          Manage your farms and crops, track conditions, and get recommendations, disease detection, and yield
          predictions — all in one place, built for farmers.
        </p>
        <div className="mt-8 flex justify-center gap-3">
          <Link
            to="/register"
            className="inline-flex items-center gap-2 rounded-lg bg-primary-600 px-6 py-3 text-sm font-medium text-white hover:bg-primary-700"
          >
            Create your account <ArrowRight className="h-4 w-4" />
          </Link>
          <Link
            to="/login"
            className="inline-flex items-center rounded-lg border border-gray-200 bg-white px-6 py-3 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            I already have an account
          </Link>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-6 pb-24">
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {features.map(({ icon: Icon, title, desc }) => (
            <div key={title} className="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm">
              <div className="mb-3 w-fit rounded-xl bg-primary-50 p-2.5">
                <Icon className="h-5 w-5 text-primary-600" />
              </div>
              <h3 className="font-semibold text-gray-900">{title}</h3>
              <p className="mt-1 text-sm text-gray-500">{desc}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
