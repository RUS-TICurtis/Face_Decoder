import React, { useRef, useState, useEffect } from 'react';
import { Upload, Camera, RefreshCw, X, Sparkles } from 'lucide-react';
import { Button } from '../ui/Button';

export function FaceUploader({ preview, onFileChange, onCapture, onAnalyze }) {
  const fileInputRef = useRef(null);
  const videoRef = useRef(null);
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [cameraStream, setCameraStream] = useState(null);
  const [cameraFacing, setCameraFacing] = useState('user'); // 'user' (front) or 'environment' (back)
  const [cameraError, setCameraError] = useState(null);
  const [isDragging, setIsDragging] = useState(false);

  // Drag and drop handlers
  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (!isDragging) setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    // Only deactivate if leaving the target boundary
    if (e.currentTarget.contains(e.relatedTarget)) return;
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile.type.startsWith('image/')) {
        if (onCapture) {
          onCapture(droppedFile);
        } else if (onFileChange) {
          onFileChange({ target: { files: [droppedFile] } });
        }
      }
    }
  };

  // Stop camera tracks cleanly
  const stopCamera = () => {
    if (cameraStream) {
      cameraStream.getTracks().forEach(track => track.stop());
      setCameraStream(null);
    }
    setIsCameraActive(false);
  };

  // Start video stream
  const startCamera = async (facing = cameraFacing) => {
    stopCamera();
    setCameraError(null);
    try {
      const constraints = {
        video: {
          facingMode: facing,
          width: { ideal: 1280 },
          height: { ideal: 720 }
        },
        audio: false
      };
      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      setCameraStream(stream);
      setIsCameraActive(true);
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (err) {
      console.error("Camera access error:", err);
      setCameraError(
        err.name === 'NotAllowedError' 
          ? 'Camera permission was denied. Please allow camera access in your browser settings.'
          : 'Unable to connect to camera device.'
      );
      setIsCameraActive(false);
    }
  };

  // Switch between front and back camera (especially on mobile)
  const toggleFacing = () => {
    const nextFacing = cameraFacing === 'user' ? 'environment' : 'user';
    setCameraFacing(nextFacing);
    startCamera(nextFacing);
  };

  // Attach stream when video element becomes available
  useEffect(() => {
    if (isCameraActive && cameraStream && videoRef.current) {
      videoRef.current.srcObject = cameraStream;
    }
  }, [isCameraActive, cameraStream]);

  // Clean up on component unmount
  useEffect(() => {
    return () => {
      if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
      }
    };
  }, [cameraStream]);

  // Take Snapshot from video canvas
  const handleSnap = () => {
    if (!videoRef.current) return;
    const video = videoRef.current;
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    const ctx = canvas.getContext('2d');
    
    // If front camera, mirror image for natural selfie feel
    if (cameraFacing === 'user') {
      ctx.translate(canvas.width, 0);
      ctx.scale(-1, 1);
    }
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob((blob) => {
      if (blob) {
        const file = new File([blob], `camera_${Date.now()}.jpg`, { type: 'image/jpeg' });
        stopCamera();
        if (onCapture) {
          onCapture(file);
        }
      }
    }, 'image/jpeg', 0.95);
  };

  return (
    <div className="upload-container">
      {/* CAMERA VIEWFINDER MODAL / VIEW */}
      {isCameraActive ? (
        <div className="camera-viewfinder">
          <video 
            ref={videoRef} 
            autoPlay 
            playsInline 
            muted 
            className={`camera-video ${cameraFacing === 'user' ? 'mirrored' : ''}`}
          />
          <div className="camera-controls">
            <button 
              type="button" 
              className="camera-ctrl-btn" 
              onClick={toggleFacing}
              title="Flip Camera"
              aria-label="Flip Camera"
            >
              <RefreshCw size={20} />
            </button>

            <button 
              type="button" 
              className="camera-shutter-btn" 
              onClick={handleSnap}
              title="Capture Photo"
              aria-label="Capture Photo"
            >
              <div className="shutter-inner" />
            </button>

            <button 
              type="button" 
              className="camera-ctrl-btn" 
              onClick={stopCamera}
              title="Close Camera"
              aria-label="Close Camera"
            >
              <X size={20} />
            </button>
          </div>
        </div>
      ) : (
        /* STANDARD UPLOAD & LIVE CAMERA PROMPTS */
        <div>
          <div className="uploader-selection-grid">
            {/* File Upload Trigger */}
            <div 
              className={`uploader-area ${isDragging ? 'dragging' : ''}`}
              onClick={() => fileInputRef.current?.click()}
              onDragEnter={handleDragEnter}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
            >
              <Upload className="icon" />
              <h2>{isDragging ? 'Drop Image Here' : 'Upload Image'}</h2>
              <p>{isDragging ? 'Release to upload face' : 'Drag & drop or browse device'}</p>
              <input 
                type="file" 
                ref={fileInputRef} 
                onChange={onFileChange} 
                accept="image/*" 
                style={{ display: 'none' }}
              />
            </div>

            {/* Live Camera Snapshot Trigger */}
            <div 
              className="uploader-area camera-trigger" 
              onClick={() => startCamera('user')}
            >
              <Camera className="icon" />
              <h2>Take Live Photo</h2>
              <p>Snap with selfie or mobile camera</p>
            </div>
          </div>

          {cameraError && (
            <div className="camera-error-banner">
              {cameraError}
            </div>
          )}
        </div>
      )}

      {/* PHOTO PREVIEW */}
      {preview && !isCameraActive && (
        <div style={{ textAlign: 'center', marginTop: '2rem' }}>
          <img 
            src={preview} 
            alt="Preview" 
            style={{ 
              maxWidth: '220px', 
              maxHeight: '220px',
              objectFit: 'cover',
              borderRadius: '12px', 
              border: '2px solid var(--accent-primary)',
              boxShadow: '0 8px 24px rgba(0,0,0,0.5)'
            }} 
          />
          <div style={{ marginTop: '1rem', display: 'flex', gap: '0.75rem', justifyContent: 'center', flexWrap: 'wrap' }}>
            <Button onClick={onAnalyze}>
              Analyze Vibes <Sparkles size={18} style={{ display: 'inline', marginLeft: '8px' }} />
            </Button>
            <Button variant="secondary" onClick={() => startCamera('user')}>
              <Camera size={16} style={{ display: 'inline', marginRight: '6px' }} /> Retake Photo
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
