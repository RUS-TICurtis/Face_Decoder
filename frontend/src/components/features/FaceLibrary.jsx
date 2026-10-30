import React, { useState, useEffect } from 'react';
import { Search, Loader2, Image as ImageIcon } from 'lucide-react';
import { Button } from '../ui/Button';
import { GlassCard } from '../ui/GlassCard';
import { API_BASE, FACES_URL } from '../../config/api';

export function FaceLibrary() {
  const [faces, setFaces] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchMode, setSearchMode] = useState(false);
  
  // Search results
  const [searchResults, setSearchResults] = useState([]);
  const [searchPreview, setSearchPreview] = useState(null);

  const fetchFaces = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/library/?limit=50&offset=0`);
      if (res.ok) {
        const data = await res.json();
        setFaces(data);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFaces();
  }, []);

  const handleSearchUpload = async (e) => {
    const selected = e.target.files[0];
    if (!selected) return;
    
    setSearchPreview(URL.createObjectURL(selected));
    setSearchMode(true);
    setLoading(true);
    
    try {
      const formData = new FormData();
      formData.append('file', selected);
      
      const res = await fetch(`${API_BASE}/library/search?top_k=12`, {
        method: 'POST',
        body: formData
      });
      
      if (!res.ok) throw new Error('Search failed');
      const data = await res.json();
      setSearchResults(data);
    } catch (err) {
      alert(err.message);
      setSearchMode(false);
    } finally {
      setLoading(false);
    }
  };

  const clearSearch = () => {
    setSearchMode(false);
    setSearchPreview(null);
    setSearchResults([]);
    fetchFaces(); // Refresh regular grid
  };

  return (
    <div className="dashboard-grid" style={{ gridTemplateColumns: '1fr' }}>
      <GlassCard>
        <div className="library-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
          <div>
            <h2>Face Library & Casting Search</h2>
            <p style={{ color: 'var(--text-muted)' }}>Explore processed faces or find lookalikes via vector search.</p>
          </div>
          
          <div className="library-actions" style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
            {searchMode && (
              <Button variant="secondary" onClick={clearSearch}>Clear Search</Button>
            )}
            <div className="add-photo-box" style={{ width: '150px', height: '40px', display: 'flex', flexDirection: 'row', padding: '0 1rem' }} onClick={() => document.getElementById('search-upload').click()}>
              <Search size={16} />
              <span style={{ marginLeft: '8px' }}>Find Lookalike</span>
            </div>
            <input 
              id="search-upload"
              type="file" 
              accept="image/*" 
              onChange={handleSearchUpload} 
              style={{ display: 'none' }}
            />
          </div>
        </div>

        {loading && (
          <div style={{ textAlign: 'center', padding: '2rem' }}>
            <Loader2 className="spinner" size={32} style={{ color: 'var(--accent-primary)', marginBottom: '1rem' }} />
            <p>Searching vector space...</p>
          </div>
        )}

        {searchMode && !loading && (
          <div style={{ marginBottom: '2rem', padding: '1rem', background: 'rgba(255,255,255,0.02)', borderRadius: '12px' }}>
            <h3 style={{ marginBottom: '1rem' }}>Query Image</h3>
            <img src={searchPreview} alt="Search Query" style={{ height: '100px', borderRadius: '8px', border: '2px solid var(--accent-secondary)' }} />
          </div>
        )}

        {!loading && (
          <div>
            <h3 style={{ marginBottom: '1rem' }}>
              {searchMode ? 'Top Lookalikes' : 'Recently Indexed Faces'}
            </h3>
            
            {((searchMode && searchResults.length === 0) || (!searchMode && faces.length === 0)) ? (
              <p style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '3rem' }}>
                <ImageIcon size={48} style={{ opacity: 0.2, marginBottom: '1rem' }} />
                <br/>
                No faces found in the library. Go to the Analyze tab to upload and index some!
              </p>
            ) : (
              <div style={{ 
                display: 'grid', 
                gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))', 
                gap: '1rem' 
              }}>
                {searchMode ? (
                  searchResults.map((item, idx) => (
                    <div key={idx} style={{ background: 'rgba(255,255,255,0.05)', borderRadius: '8px', padding: '0.5rem', textAlign: 'center' }}>
                      <img 
                        src={`${FACES_URL}/${item.record.filename}`} 
                        alt="Match" 
                        style={{ width: '100%', aspectRatio: '1/1', objectFit: 'cover', borderRadius: '4px' }}
                      />
                      <div style={{ marginTop: '0.5rem' }}>
                        <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Match</span>
                        <div style={{ color: 'var(--accent-primary)', fontWeight: 'bold' }}>{item.similarity}%</div>
                      </div>
                    </div>
                  ))
                ) : (
                  faces.map((face) => (
                    <div key={face.id} style={{ background: 'rgba(255,255,255,0.05)', borderRadius: '8px', padding: '0.5rem', textAlign: 'center' }}>
                      <img 
                        src={`${FACES_URL}/${face.filename}`} 
                        alt="Indexed Face" 
                        style={{ width: '100%', aspectRatio: '1/1', objectFit: 'cover', borderRadius: '4px' }}
                      />
                      <div style={{ marginTop: '0.5rem', fontSize: '0.75rem', color: 'var(--text-muted)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {face.source_image}
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}
          </div>
        )}
      </GlassCard>
    </div>
  );
}
