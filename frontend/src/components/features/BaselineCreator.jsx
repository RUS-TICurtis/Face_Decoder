import React, { useState } from 'react';
import { Button } from '../ui/Button';
import { GlassCard } from '../ui/GlassCard';
import { User, Image as ImageIcon, Save, Loader2 } from 'lucide-react';
import { API_BASE } from '../../config/api';

export function BaselineCreator() {
  const [name, setName] = useState('');
  const [photoFiles, setPhotoFiles] = useState([]);
  const [photoUrls, setPhotoUrls] = useState([]);
  const [loading, setLoading] = useState(false);
  
  // Default values
  const [archetypes, setArchetypes] = useState({
    Approachable: 50,
    Regal: 50,
    Mysterious: 50,
    Trustworthy: 50
  });
  
  const [aesthetics, setAesthetics] = useState({
    cute: 50,
    '10/10': 50,
    spec: 50,
    beautiful: 50,
    handsome: 50
  });

  const handlePhotoUpload = (e) => {
    const files = Array.from(e.target.files);
    const slotsAvailable = 3 - photoFiles.length;
    if (slotsAvailable <= 0) return;
    
    const newFiles = files.slice(0, slotsAvailable);
    setPhotoFiles([...photoFiles, ...newFiles]);
    
    const newUrls = newFiles.map(p => URL.createObjectURL(p));
    setPhotoUrls([...photoUrls, ...newUrls]);
  };

  const handleSave = async () => {
    if (!name) {
      alert('Please enter a name for the baseline');
      return;
    }
    if (photoFiles.length === 0) {
      alert('Please upload at least one reference photo.');
      return;
    }
    
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('name', name);
      formData.append('archetypes', JSON.stringify(archetypes));
      formData.append('aesthetics', JSON.stringify(aesthetics));
      
      photoFiles.forEach(file => {
        formData.append('files', file);
      });

      const response = await fetch(`${API_BASE}/baselines/`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || 'Failed to save baseline');
      }

      alert(`Baseline established for ${name}!`);
      
      // Reset form
      setName('');
      setPhotoFiles([]);
      setPhotoUrls([]);
    } catch (err) {
      alert('Error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <GlassCard>
      <div style={{ marginBottom: '2rem', textAlign: 'center' }}>
        <h2><User size={24} style={{ display: 'inline', marginRight: '8px' }}/> Define Ground Truth Baseline</h2>
        <p style={{ color: 'var(--text-muted)' }}>Manually set the ideal aesthetic scores for a specific person or persona.</p>
      </div>
      
      <div className="input-group">
        <label>Subject Name (e.g., Ryan Reynolds)</label>
        <input 
          type="text" 
          value={name} 
          onChange={(e) => setName(e.target.value)}
          placeholder="Enter name..."
          className="text-input"
        />
      </div>
      
      <div className="input-group" style={{ marginTop: '1.5rem' }}>
        <label>Reference Photos (Max 3) - These are used to calculate the ArcFace structural centroid</label>
        <div style={{ display: 'flex', gap: '1rem', marginTop: '0.5rem' }}>
          {photoUrls.map((p, i) => (
            <img key={i} src={p} alt={`Upload ${i}`} className="baseline-img" />
          ))}
          {photoUrls.length < 3 && (
            <div className="add-photo-box" onClick={() => document.getElementById('baseline-upload').click()}>
              <ImageIcon />
              <span>Add</span>
            </div>
          )}
        </div>
        <input 
          id="baseline-upload"
          type="file" 
          multiple 
          accept="image/*" 
          onChange={handlePhotoUpload} 
          style={{ display: 'none' }}
        />
      </div>
      
      <div className="dashboard-grid" style={{ marginTop: '2rem' }}>
        <div className="slider-group">
          <h3 style={{ color: 'var(--accent-primary)', marginBottom: '1rem' }}>Archetypes (Ground Truth)</h3>
          {Object.keys(archetypes).map(arch => (
            <div key={arch} className="slider-container">
              <div className="slider-header">
                <span>{arch}</span>
                <span>{archetypes[arch]}%</span>
              </div>
              <input 
                type="range" 
                min="0" max="100" 
                value={archetypes[arch]} 
                onChange={(e) => setArchetypes({...archetypes, [arch]: parseInt(e.target.value)})}
                className="custom-slider"
              />
            </div>
          ))}
        </div>
        
        <div className="slider-group">
          <h3 style={{ color: 'var(--accent-secondary)', marginBottom: '1rem' }}>Aesthetics (Ground Truth)</h3>
          {Object.keys(aesthetics).map(ast => (
            <div key={ast} className="slider-container">
              <div className="slider-header">
                <span>{ast}</span>
                <span>{aesthetics[ast]}%</span>
              </div>
              <input 
                type="range" 
                min="0" max="100" 
                value={aesthetics[ast]} 
                onChange={(e) => setAesthetics({...aesthetics, [ast]: parseInt(e.target.value)})}
                className="custom-slider"
              />
            </div>
          ))}
        </div>
      </div>
      
      <Button onClick={handleSave} disabled={loading} style={{ width: '100%', marginTop: '2rem' }}>
        {loading ? <Loader2 size={18} className="spinner" style={{ display: 'inline', marginRight: '8px' }}/> : <Save size={18} style={{ display: 'inline', marginRight: '8px' }}/>}
        {loading ? 'Saving...' : 'Save Baseline'}
      </Button>
    </GlassCard>
  );
}
