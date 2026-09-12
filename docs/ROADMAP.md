# Development Roadmap: Facial Recognition & Semblance Engine

## Phase 1: Core Foundation & Modular Filing System (Completed)
- [x] Establish comprehensive `.gitignore` across Python environments, IDEs, and binary storage directories.
- [x] Implement structured file storage taxonomy with `.gitkeep` directory preservation.
- [x] Modularize `app/` into `core/`, `api/`, `schemas/`, `services/`, and `utils/`.
- [x] Create Pydantic v2 schemas for face coordinates, emotional affect profiles, and semblance metrics.
- [x] Build upload pipeline with UUID tracking, header validation, and metadata extraction.
- [x] Author comprehensive documentation (`README.md`, `ARCHITECTURE.md`, `FILING_AND_STORAGE_SYSTEM.md`).

## Phase 2: Computer Vision & Landmark Extraction
- [ ] Integrate lightweight face detection backend (MediaPipe Face Mesh or OpenCV YuNet).
- [ ] Implement face alignment and normalization (eye-level rotation, standard bounding crop).
- [ ] Store cropped face chips into `storage/processed_faces/`.

## Phase 3: Deep Affect & Human Feeling Analysis
- [ ] Train or integrate deep affective models (e.g. FER2013 fine-tuned, EmoNet, or HSEmotion).
- [ ] Compute continuous Valence-Arousal dimensional metrics alongside discrete emotion classes.
- [ ] Implement micro-expression detection across localized regions (eyes, brow, mouth curvature).

## Phase 4: Semblance Engine & Comparison Matrix
- [ ] Implement high-dimensional facial embeddings (ArcFace or FaceNet).
- [ ] Develop cosine similarity and Riemannian metric comparisons for geometric semblance.
- [ ] Build multi-subject comparison matrix and PDF/JSON report generation into `storage/reports/`.
- [ ] Interactive Web UI for side-by-side image comparison with visual semblance heatmaps.
