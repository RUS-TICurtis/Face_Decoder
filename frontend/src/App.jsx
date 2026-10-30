import React, { useState, useEffect } from 'react';
import { AlertCircle } from 'lucide-react';
import './index.css';

// Components
import { GlassCard } from './components/ui/GlassCard';
import { Button } from './components/ui/Button';
import { FaceUploader } from './components/features/FaceUploader';
import { VibeDashboard } from './components/features/VibeDashboard';
import { BaselineCreator } from './components/features/BaselineCreator';
import { FaceLibrary } from './components/features/FaceLibrary';
import { ScanHistoryView } from './components/features/ScanHistoryView';

// API Configuration
import { API_BASE, FACES_URL } from './config/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('ANALYZE'); // ANALYZE, BASELINE, LIBRARY, HISTORY

  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState('UPLOAD'); // UPLOAD, ANALYZING, RESULTS, ERROR
  const [error, setError] = useState(null);
  
  // Baselines
  const [baselines, setBaselines] = useState([]);
  const [selectedBaselineId, setSelectedBaselineId] = useState('');
  
  // Data from backend
  const [detectionData, setDetectionData] = useState(null);
  const [vibeData, setVibeData] = useState(null);
  const [affinityData, setAffinityData] = useState(null);

  const fetchBaselines = async () => {
    try {
      const res = await fetch(`${API_BASE}/baselines/`);
      if (res.ok) {
        const data = await res.json();
        setBaselines(data);
      }
    } catch (e) {
      console.error("Failed to load baselines:", e);
    }
  };

  useEffect(() => {
    fetchBaselines();
  }, [activeTab]); // Refresh when swapping tabs

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected) {
      setFile(selected);
      setPreview(URL.createObjectURL(selected));
      setStep('UPLOAD');
    }
  };

  const handleCapture = (capturedFile) => {
    if (capturedFile) {
      setFile(capturedFile);
      setPreview(URL.createObjectURL(capturedFile));
      setStep('UPLOAD');
    }
  };

  const handleUploadAndAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    setStep('ANALYZING');
    setAffinityData(null);
    
    try {
      // 1. Upload & Detect Crop
      const formData = new FormData();
      formData.append('file', file);
      
      const detectRes = await fetch(`${API_BASE}/faces/detect-and-crop`, {
        method: 'POST',
        body: formData,
      });
      
      if (!detectRes.ok) throw new Error('Failed to process image for face detection');
      const detectResult = await detectRes.json();
      setDetectionData(detectResult);
      
      if (!detectResult.faces || detectResult.faces.length === 0) {
        throw new Error('No face detected in the uploaded image.');
      }
      
      // 2. Run Vibe Analysis on the first face crop
      const cropId = detectResult.faces[0].crop_filename;
      const vibeRes = await fetch(`${API_BASE}/semblance/analyze/${cropId}`, {
        method: 'POST',
      });
      
      if (!vibeRes.ok) {
        if (vibeRes.status === 501) throw new Error('Gemini API Key is not configured on the backend.');
        throw new Error('Vibe analysis failed.');
      }
      
      const vibeResult = await vibeRes.json();
      setVibeData(vibeResult);

      // 3. If Baseline selected, compute affinity
      if (selectedBaselineId) {
        const affinityFormData = new FormData();
        affinityFormData.append('file', file);
        const affinityRes = await fetch(`${API_BASE}/baselines/${selectedBaselineId}/analyze`, {
          method: 'POST',
          body: affinityFormData,
        });
        if (affinityRes.ok) {
          const affinityResult = await affinityRes.json();
          setAffinityData(affinityResult);
        }
      }

      setStep('RESULTS');
      
    } catch (err) {
      setError(err.message || 'An unknown error occurred');
      setStep('ERROR');
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setFile(null);
    setPreview(null);
    setDetectionData(null);
    setVibeData(null);
    setAffinityData(null);
    setStep('UPLOAD');
  };

  return (
    <div className="app-container">
      <header>
        <h1>Facial Intelligence</h1>
        <p>Aesthetic & Archetype Analysis Engine</p>
        
        <div className="nav-tab-group" style={{ marginTop: '2rem' }}>
          <Button 
            variant={activeTab === 'ANALYZE' ? 'primary' : 'secondary'} 
            onClick={() => setActiveTab('ANALYZE')}
          >
            Analyze Photo
          </Button>
          <Button 
            variant={activeTab === 'BASELINE' ? 'primary' : 'secondary'} 
            onClick={() => setActiveTab('BASELINE')}
          >
            Define Baselines
          </Button>
          <Button 
            variant={activeTab === 'LIBRARY' ? 'primary' : 'secondary'} 
            onClick={() => setActiveTab('LIBRARY')}
          >
            Face Library
          </Button>
          <Button 
            variant={activeTab === 'HISTORY' ? 'primary' : 'secondary'} 
            onClick={() => setActiveTab('HISTORY')}
          >
            Scan History
          </Button>
        </div>
      </header>
      
      {activeTab === 'ANALYZE' && (
        <GlassCard>
          {step === 'UPLOAD' && (
            <>
              {baselines.length > 0 && (
                <div className="input-group" style={{ marginBottom: '1.5rem', textAlign: 'center' }}>
                  <label>Compare Against Baseline (Score 4)</label>
                  <select 
                    className="text-input" 
                    value={selectedBaselineId} 
                    onChange={(e) => setSelectedBaselineId(e.target.value)}
                    style={{ maxWidth: '300px', margin: '0.5rem auto' }}
                  >
                    <option value="">-- None (Skip Affinity) --</option>
                    {baselines.map(b => (
                      <option key={b.id} value={b.id}>{b.name}</option>
                    ))}
                  </select>
                </div>
              )}
              <FaceUploader 
                preview={preview}
                onFileChange={handleFileChange}
                onCapture={handleCapture}
                onAnalyze={handleUploadAndAnalyze}
              />
            </>
          )}

          {step === 'ANALYZING' && (
            <div className="loader">
              <div className="spinner"></div>
              <h2>Running AI Analysis...</h2>
              <p>Extracting face coordinates and computing aesthetic resonance.</p>
            </div>
          )}

          {step === 'ERROR' && (
            <div style={{ textAlign: 'center', padding: '2rem' }}>
              <AlertCircle size={48} color="#ff007f" style={{ marginBottom: '1rem' }} />
              <h2 style={{ color: '#ff007f' }}>Analysis Failed</h2>
              <p style={{ marginTop: '1rem' }}>{error}</p>
              <Button onClick={reset} style={{ marginTop: '2rem' }}>Try Again</Button>
            </div>
          )}

          {step === 'RESULTS' && (
            <VibeDashboard 
              detectionData={detectionData}
              vibeData={vibeData}
              affinityData={affinityData}
              facesUrl={FACES_URL}
              onReset={reset}
            />
          )}
        </GlassCard>
      )}
      
      {activeTab === 'BASELINE' && (
        <BaselineCreator />
      )}

      {activeTab === 'LIBRARY' && (
        <FaceLibrary />
      )}

      {activeTab === 'HISTORY' && (
        <ScanHistoryView onNavigateToAnalyze={() => setActiveTab('ANALYZE')} />
      )}
    </div>
  );
}
