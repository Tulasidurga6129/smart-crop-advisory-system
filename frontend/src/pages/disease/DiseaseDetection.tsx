import { useEffect, useState, type ChangeEvent } from 'react';
import { Bug, Upload, Trash2, CheckCircle2, AlertTriangle, Leaf } from 'lucide-react';
import { useFarms } from '../../context/FarmContext';
import { getFarmCrops } from '../../api/crops';
import { getFarmDetections, deleteDetection, predictDisease, type DiseasePredictionResponse } from '../../api/disease';
import type { CropResponse, DiseaseDetectionResponse } from '../../types';
import { LoadingSpinner } from '../../components/ui/LoadingSpinner';
import { ErrorMessage } from '../../components/ui/ErrorMessage';
import { EmptyState } from '../../components/ui/EmptyState';
import { StatusBadge } from '../../components/ui/StatusBadge';
import { normalizeError } from '../../api/client';

export function DiseaseDetection() {
  const { selectedFarmId, farms } = useFarms();
  const [crops, setCrops] = useState<CropResponse[]>([]);
  const [records, setRecords] = useState<DiseaseDetectionResponse[]>([]);
  const [selectedCropId, setSelectedCropId] = useState<number | null>(null);
  const [image, setImage] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<DiseasePredictionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    if (!selectedFarmId) return;
    setError(null);
    try {
      const [cropData, detectionData] = await Promise.all([getFarmCrops(selectedFarmId), getFarmDetections(selectedFarmId)]);
      setCrops(cropData);
      setRecords(detectionData);
      setSelectedCropId((current) => current && cropData.some(c => c.id === current) ? current : cropData[0]?.id ?? null);
    } catch (err) { setError(normalizeError(err).message); }
  }

  useEffect(() => { load(); }, [selectedFarmId]);

  function handleImage(e: ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0] ?? null;
    setImage(file); setResult(null); setError(null);
    if (preview) URL.revokeObjectURL(preview);
    setPreview(file ? URL.createObjectURL(file) : null);
  }

  async function handlePredict() {
    if (!selectedFarmId || !selectedCropId || !image) { setError('Select a crop and upload a leaf image first.'); return; }
    setLoading(true); setError(null); setResult(null);
    try {
      const response = await predictDisease(selectedFarmId, selectedCropId, image);
      setResult(response);
      setRecords(r => [response.detection, ...r.filter(x => x.id !== response.detection.id)]);
    } catch (err) { setError(normalizeError(err).message); }
    finally { setLoading(false); }
  }

  async function handleDelete(id: number) {
    try { await deleteDetection(id); setRecords(r => r.filter(x => x.id !== id)); }
    catch (err) { setError(normalizeError(err).message); }
  }

  if (farms.length === 0) return <EmptyState icon={Bug} title="Add a farm first" description="Disease detection is tied to a farm and crop." />;

  return (
    <div className="mx-auto flex max-w-5xl flex-col gap-6">
      <div><h1 className="text-2xl font-semibold text-gray-900">Disease Detection</h1><p className="text-sm text-gray-500">Upload a crop leaf image and let the ML model identify the disease and provide treatment guidance.</p></div>

      <div className="rounded-2xl border border-gray-100 bg-white p-6 shadow-sm">
        <div className="grid gap-5 md:grid-cols-2">
          <div>
            <label className="mb-2 block text-sm font-medium text-gray-700">Crop</label>
            <select value={selectedCropId ?? ''} onChange={e => { setSelectedCropId(Number(e.target.value)); setResult(null); }} className="w-full rounded-lg border border-gray-200 px-3 py-2.5 text-sm">
              {crops.map(c => <option key={c.id} value={c.id}>{c.name}{c.variety ? ` · ${c.variety}` : ''}</option>)}
            </select>
          </div>
          <div>
            <label className="mb-2 block text-sm font-medium text-gray-700">Leaf image</label>
            <label className="flex cursor-pointer items-center gap-3 rounded-lg border border-dashed border-primary-300 bg-primary-50/30 px-4 py-3 text-sm hover:bg-primary-50">
              <Upload className="h-5 w-5 text-primary-600" />
              <span>{image ? image.name : 'Choose JPEG, PNG or WEBP image'}</span>
              <input type="file" accept="image/jpeg,image/png,image/webp" onChange={handleImage} className="hidden" />
            </label>
          </div>
        </div>

        {preview && <div className="mt-5 overflow-hidden rounded-xl border bg-gray-50"><img src={preview} alt="Selected leaf" className="mx-auto max-h-72 object-contain" /></div>}
        {error && <div className="mt-4"><ErrorMessage message={error} /></div>}
        <button onClick={handlePredict} disabled={loading || !image || !selectedCropId} className="mt-5 inline-flex items-center gap-2 rounded-lg bg-primary-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-primary-700 disabled:opacity-50">
          <Bug className="h-4 w-4" /> {loading ? 'Analyzing…' : 'Analyze Disease'}
        </button>
      </div>

      {loading && <LoadingSpinner size="lg" label="Running the disease detection model…" />}

      {result && !loading && <PredictionResult result={result} />}

      <div>
        <h2 className="mb-3 text-lg font-semibold text-gray-900">Detection History</h2>
        {records.length === 0 ? <EmptyState icon={Bug} title="No disease detections yet" /> : <div className="grid gap-4 sm:grid-cols-2">
          {records.map(rec => <div key={rec.id} className="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm">
            <div className="flex items-center justify-between"><p className="font-semibold text-gray-900">{rec.disease_name}</p><StatusBadge value={rec.severity} /></div>
            {rec.confidence != null && <p className="mt-1 text-xs text-gray-400">Confidence: {(rec.confidence * 100).toFixed(1)}%</p>}
            {rec.symptoms && <p className="mt-2 text-sm text-gray-600">{rec.symptoms}</p>}
            <div className="mt-3 flex items-center justify-between"><StatusBadge value={rec.detection_source} /><button onClick={() => handleDelete(rec.id)} className="inline-flex items-center gap-1 text-xs font-medium text-red-500 hover:underline"><Trash2 className="h-3.5 w-3.5" /> Delete</button></div>
          </div>)}
        </div>}
      </div>
    </div>
  );
}

function PredictionResult({ result }: { result: DiseasePredictionResponse }) {
  const p = result.prediction;
  const confidence = p.confidence * 100;
  return <div className="rounded-2xl border border-primary-100 bg-white p-6 shadow-sm">
    <div className="flex flex-wrap items-start justify-between gap-3">
      <div><div className="flex items-center gap-2 text-sm font-medium text-primary-700"><CheckCircle2 className="h-5 w-5" /> ML Detection Result</div><h2 className="mt-1 text-2xl font-bold text-gray-900">{p.disease}</h2><p className="text-sm text-gray-500">{p.plant} · {p.class_name}</p></div>
      <div className="rounded-xl bg-primary-50 px-4 py-3 text-center"><p className="text-2xl font-bold text-primary-700">{confidence.toFixed(1)}%</p><p className="text-xs text-gray-500">Confidence</p></div>
    </div>
    {confidence < 70 && <div className="mt-4 flex gap-2 rounded-lg bg-amber-50 p-3 text-sm text-amber-800"><AlertTriangle className="h-5 w-5 shrink-0" /> Moderate confidence. Upload a clear, well-lit leaf image for a more reliable result.</div>}
    <p className="mt-5 text-sm leading-6 text-gray-600">{p.description}</p>
    <div className="mt-5 grid gap-4 md:grid-cols-2">
      <Info title="Treatment" items={p.treatment} />
      <Info title="Prevention" items={p.prevention} />
    </div>
    <div className="mt-4 rounded-xl bg-emerald-50 p-4"><div className="mb-1 flex items-center gap-2 font-medium text-emerald-800"><Leaf className="h-4 w-4" /> Fertilizer Guidance</div><p className="text-sm text-emerald-900/80">{p.fertilizer}</p></div>
  </div>;
}

function Info({ title, items }: { title: string; items: string[] }) { return <div className="rounded-xl border border-gray-100 p-4"><h3 className="mb-2 font-medium text-gray-900">{title}</h3><ul className="space-y-2 text-sm text-gray-600">{items.map((x,i) => <li key={i}>• {x}</li>)}</ul></div>; }
