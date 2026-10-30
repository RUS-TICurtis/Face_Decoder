import React, { useState } from 'react';
import { User, Activity, HeartHandshake, BrainCircuit, ScanFace, Bookmark, Check, Loader2 } from 'lucide-react';
import { Button } from '../ui/Button';
import { ProgressBar } from '../ui/ProgressBar';
import { API_BASE } from '../../config/api';

export function VibeDashboard({ detectionData, vibeData, affinityData, facesUrl, onReset, onSaveSuccess }) {
  const [personName, setPersonName] = useState('');
  const [notes, setNotes] = useState('');
  const [isSaving, setIsSaving] = useState(false);
  const [isSaved, setIsSaved] = useState(false);

  if (!vibeData || !detectionData) return null;
  
  const faceCropUrl = `${facesUrl}/${detectionData.faces[0].crop_filename}`;

  const handleSaveToHistory = async () => {
    setIsSaving(true);
    try {
      const payload = {
        person_name: personName.trim() || 'Anonymous Subject',
        avatar_crop_filename: detectionData.faces[0].crop_filename,
        source_filename: detectionData.faces[0].crop_filename,
        vibe_data: vibeData,
        affinity_data: affinityData,
        notes: notes.trim() || null
      };

      const res = await fetch(`${API_BASE}/history/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error('Failed to save to scan history');
      setIsSaved(true);
      if (onSaveSuccess) onSaveSuccess();
    } catch (err) {
      alert(err.message);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="dashboard-grid">
      <div className="face-preview">
        <h3>Detected Face</h3>
        <img 
          src={faceCropUrl} 
          alt="Detected Face Crop" 
          className="face-img" 
        />
        
        {/* SAVE TO HISTORY SECTION */}
        <div className="save-history-box" style={{ width: '100%', marginTop: '1rem', padding: '1rem', background: 'rgba(255,255,255,0.03)', borderRadius: '12px', border: '1px solid var(--border-glass)' }}>
          <label style={{ display: 'block', fontSize: '0.85rem', marginBottom: '0.4rem', color: 'var(--text-muted)' }}>
            Subject Name / Identifier
          </label>
          <input 
            type="text" 
            placeholder="e.g. Alex Rivera" 
            value={personName}
            onChange={(e) => setPersonName(e.target.value)}
            disabled={isSaved}
            className="text-input"
            style={{ fontSize: '0.9rem', padding: '8px 12px', marginBottom: '0.75rem' }}
          />

          <input 
            type="text" 
            placeholder="Optional notes or context..." 
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            disabled={isSaved}
            className="text-input"
            style={{ fontSize: '0.85rem', padding: '6px 12px', marginBottom: '0.75rem' }}
          />

          <Button 
            onClick={handleSaveToHistory} 
            disabled={isSaving || isSaved} 
            style={{ width: '100%', padding: '10px 16px', fontSize: '0.9rem' }}
          >
            {isSaved ? (
              <><Check size={16} style={{ display: 'inline', marginRight: '6px' }} /> Saved to History</>
            ) : isSaving ? (
              <><Loader2 size={16} className="spinner" style={{ display: 'inline', marginRight: '6px' }} /> Saving...</>
            ) : (
              <><Bookmark size={16} style={{ display: 'inline', marginRight: '6px' }} /> Save to History</>
            )}
          </Button>
        </div>

        <Button onClick={onReset} variant="secondary" style={{ width: '100%', marginTop: '0.5rem' }}>
          Analyze Another
        </Button>
      </div>
      
      <div className="stats-container">
        
        {/* EXPLANATION ENGINE (Score 3) */}
        {vibeData.explanation && (
          <div className="stat-group" style={{ marginBottom: '1.5rem', backgroundColor: 'rgba(138, 43, 226, 0.1)', padding: '1.2rem', borderRadius: '12px', border: '1px solid rgba(138, 43, 226, 0.3)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
              <h3 style={{ color: 'var(--accent-primary)', margin: 0 }}><BrainCircuit size={20} color="#8a2be2" style={{ display: 'inline', marginRight: '6px' }}/> Explanation Engine</h3>
              {vibeData.perceptual_appeal && (
                <div style={{ background: 'var(--accent-primary)', color: 'white', padding: '4px 10px', borderRadius: '20px', fontSize: '0.85rem', fontWeight: 'bold' }}>
                  Score ③: {vibeData.perceptual_appeal}
                </div>
              )}
            </div>
            <p style={{ fontSize: '0.95rem', lineHeight: '1.5', margin: '0 0 1rem 0' }}>"{vibeData.explanation}"</p>
            
            {vibeData.regional_contributions && (
              <div>
                <h4 style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '1px', marginBottom: '0.5rem' }}><ScanFace size={14} style={{ display: 'inline', marginRight: '4px'}}/> Regional Drivers</h4>
                <div className="regional-drivers-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
                  {Object.entries(vibeData.regional_contributions).map(([region, val]) => (
                    <div key={region} style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', background: 'rgba(255,255,255,0.05)', padding: '4px 8px', borderRadius: '4px' }}>
                      <span style={{ textTransform: 'capitalize' }}>{region.replace('_', ' ')}</span>
                      <span style={{ fontWeight: 'bold', color: 'var(--accent-secondary)' }}>{val}%</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* SCORE 4: PERSONAL AFFINITY */}
        {affinityData && (
          <div className="stat-group" style={{ marginBottom: '1.5rem', backgroundColor: 'rgba(255, 0, 127, 0.1)', padding: '1rem', borderRadius: '12px' }}>
            <h3 style={{ color: 'var(--accent-secondary)' }}><HeartHandshake size={20} color="#ff007f" /> Personal Affinity (Score 4)</h3>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
              Structural similarity to {affinityData.baseline.name}'s centroid
            </p>
            <ProgressBar label="Affinity Match" score={Math.round(affinityData.affinity.score * 100)} />
          </div>
        )}

        <div className="stat-group">
          <h3><User size={20} color="#8a2be2" /> Archetypes</h3>
          {Object.entries(vibeData.archetypes).map(([name, score]) => (
            <ProgressBar key={name} label={name} score={score} />
          ))}
        </div>
        
        <div className="stat-group" style={{ marginTop: '1.5rem' }}>
          <h3><Activity size={20} color="#ff007f" /> Aesthetics</h3>
          {Object.entries(vibeData.aesthetics).map(([name, score]) => (
            <ProgressBar key={name} label={name} score={score} />
          ))}
        </div>
      </div>
    </div>
  );
}
