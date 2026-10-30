import React, { useState, useEffect } from 'react';
import { History, User, Trash2, Calendar, FileText, Activity, BrainCircuit, HeartHandshake, Eye, ChevronRight } from 'lucide-react';
import { GlassCard } from '../ui/GlassCard';
import { Button } from '../ui/Button';
import { ProgressBar } from '../ui/ProgressBar';
import { API_BASE, FACES_URL } from '../../config/api';

export function ScanHistoryView() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedRecord, setSelectedRecord] = useState(null);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/history/?limit=50&offset=0`);
      if (res.ok) {
        const data = await res.json();
        setHistory(data);
      }
    } catch (e) {
      console.error("Failed to load history:", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    if (!window.confirm("Delete this scan record from history?")) return;
    try {
      const res = await fetch(`${API_BASE}/history/${id}`, { method: 'DELETE' });
      if (res.ok) {
        setHistory(prev => prev.filter(item => item.id !== id));
        if (selectedRecord?.id === id) {
          setSelectedRecord(null);
        }
      }
    } catch (err) {
      console.error("Delete failed:", err);
    }
  };

  const formatDate = (dateStr) => {
    try {
      const d = new Date(dateStr);
      return d.toLocaleDateString(undefined, { 
        month: 'short', 
        day: 'numeric', 
        year: 'numeric', 
        hour: '2-digit', 
        minute: '2-digit' 
      });
    } catch {
      return dateStr;
    }
  };

  return (
    <div className="dashboard-grid" style={{ gridTemplateColumns: selectedRecord ? '1.1fr 1.4fr' : '1fr' }}>
      {/* HISTORY LIST */}
      <GlassCard>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <div>
            <h2><History size={22} style={{ display: 'inline', marginRight: '8px', color: 'var(--accent-primary)' }} /> Scan History</h2>
            <p style={{ color: 'var(--text-muted)' }}>Chronological record of analyzed individuals and their vibe metrics.</p>
          </div>
          <Button variant="secondary" onClick={fetchHistory} disabled={loading} style={{ padding: '8px 16px', fontSize: '0.85rem' }}>
            Refresh
          </Button>
        </div>

        {loading && (
          <div className="loader">
            <div className="spinner"></div>
            <p>Loading scan records...</p>
          </div>
        )}

        {!loading && history.length === 0 && (
          <div style={{ textAlign: 'center', padding: '3rem 1rem', color: 'var(--text-muted)' }}>
            <User size={48} style={{ opacity: 0.2, marginBottom: '1rem' }} />
            <p>No scan history recorded yet. Scan a face in the Analyze tab and click "Save to History"!</p>
          </div>
        )}

        {!loading && history.length > 0 && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {history.map((record) => {
              const isSelected = selectedRecord?.id === record.id;
              const avatarUrl = `${FACES_URL}/${record.avatar_crop_filename}`;
              return (
                <div 
                  key={record.id}
                  onClick={() => setSelectedRecord(record)}
                  className={`history-card-item ${isSelected ? 'selected' : ''}`}
                >
                  <img 
                    src={avatarUrl} 
                    alt={record.person_name} 
                    className="history-avatar"
                  />
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <h4 style={{ margin: 0, fontWeight: 600, fontSize: '1.05rem', color: 'var(--text-main)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {record.person_name}
                      </h4>
                      <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                        <Calendar size={12} /> {formatDate(record.created_at)}
                      </span>
                    </div>

                    <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.4rem', flexWrap: 'wrap' }}>
                      {record.vibe_data?.perceptual_appeal && (
                        <span className="badge-pill appeal-badge">
                          Score ③: {record.vibe_data.perceptual_appeal}
                        </span>
                      )}
                      {record.affinity_data?.affinity?.score !== undefined && (
                        <span className="badge-pill affinity-badge">
                          Affinity: {Math.round(record.affinity_data.affinity.score * 100)}%
                        </span>
                      )}
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <button 
                      onClick={(e) => handleDelete(record.id, e)} 
                      className="delete-icon-btn"
                      title="Delete record"
                    >
                      <Trash2 size={16} />
                    </button>
                    <ChevronRight size={18} style={{ color: 'var(--text-muted)' }} />
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </GlassCard>

      {/* SELECTED RECORD DETAIL DRAWER */}
      {selectedRecord && (
        <GlassCard>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1.5rem' }}>
            <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
              <img 
                src={`${FACES_URL}/${selectedRecord.avatar_crop_filename}`} 
                alt={selectedRecord.person_name} 
                style={{ width: '80px', height: '80px', borderRadius: '12px', border: '2px solid var(--accent-primary)', objectFit: 'cover' }}
              />
              <div>
                <h3 style={{ margin: 0, fontSize: '1.4rem' }}>{selectedRecord.person_name}</h3>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginTop: '4px' }}>
                  Recorded on {formatDate(selectedRecord.created_at)}
                </p>
                {selectedRecord.notes && (
                  <p style={{ fontSize: '0.9rem', color: 'var(--accent-secondary)', marginTop: '4px' }}>
                    Note: "{selectedRecord.notes}"
                  </p>
                )}
              </div>
            </div>
            <Button variant="secondary" onClick={() => setSelectedRecord(null)} style={{ padding: '6px 12px' }}>
              Close
            </Button>
          </div>

          {/* Explanation Quote */}
          {selectedRecord.vibe_data?.explanation && (
            <div style={{ marginBottom: '1.5rem', padding: '1rem', background: 'rgba(138, 43, 226, 0.1)', borderRadius: '10px', border: '1px solid rgba(138, 43, 226, 0.25)' }}>
              <h4 style={{ color: 'var(--accent-primary)', margin: '0 0 0.5rem 0' }}><BrainCircuit size={16} style={{ display: 'inline', marginRight: '6px' }} /> Explanation Engine</h4>
              <p style={{ margin: 0, fontSize: '0.9rem', fontStyle: 'italic', lineHeight: '1.4' }}>
                "{selectedRecord.vibe_data.explanation}"
              </p>
            </div>
          )}

          {/* Regional Drivers */}
          {selectedRecord.vibe_data?.regional_contributions && (
            <div style={{ marginBottom: '1.5rem' }}>
              <h4 style={{ color: 'var(--text-muted)', fontSize: '0.8rem', textTransform: 'uppercase', marginBottom: '0.5rem' }}>Regional Drivers</h4>
              <div className="regional-drivers-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
                {Object.entries(selectedRecord.vibe_data.regional_contributions).map(([region, val]) => (
                  <div key={region} style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', background: 'rgba(255,255,255,0.05)', padding: '5px 10px', borderRadius: '6px' }}>
                    <span style={{ textTransform: 'capitalize' }}>{region.replace('_', ' ')}</span>
                    <span style={{ fontWeight: 'bold', color: 'var(--accent-secondary)' }}>{val}%</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Affinity Match */}
          {selectedRecord.affinity_data && (
            <div style={{ marginBottom: '1.5rem', padding: '1rem', background: 'rgba(255, 0, 127, 0.08)', borderRadius: '10px' }}>
              <h4 style={{ color: 'var(--accent-secondary)', margin: '0 0 0.5rem 0' }}><HeartHandshake size={16} style={{ display: 'inline', marginRight: '6px' }} /> Affinity Match</h4>
              <ProgressBar label={`Match against ${selectedRecord.affinity_data.baseline?.name || 'Baseline'}`} score={Math.round(selectedRecord.affinity_data.affinity.score * 100)} />
            </div>
          )}

          {/* Archetypes */}
          {selectedRecord.vibe_data?.archetypes && (
            <div style={{ marginBottom: '1.5rem' }}>
              <h4 style={{ color: 'var(--accent-primary)', marginBottom: '0.75rem' }}><User size={16} style={{ display: 'inline', marginRight: '6px' }} /> Archetypes</h4>
              {Object.entries(selectedRecord.vibe_data.archetypes).map(([name, score]) => (
                <ProgressBar key={name} label={name} score={score} />
              ))}
            </div>
          )}

          {/* Aesthetics */}
          {selectedRecord.vibe_data?.aesthetics && (
            <div>
              <h4 style={{ color: 'var(--accent-secondary)', marginBottom: '0.75rem' }}><Activity size={16} style={{ display: 'inline', marginRight: '6px' }} /> Aesthetics</h4>
              {Object.entries(selectedRecord.vibe_data.aesthetics).map(([name, score]) => (
                <ProgressBar key={name} label={name} score={score} />
              ))}
            </div>
          )}
        </GlassCard>
      )}
    </div>
  );
}
