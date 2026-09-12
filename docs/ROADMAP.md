# Development Roadmap: Facial Recognition & Semblance Engine

## Phase 1: Core Foundation & Modular Filing System (Completed)
- [x] Establish comprehensive `.gitignore` across Python environments, IDEs, and binary storage directories.
- [x] Implement structured file storage taxonomy with `.gitkeep` directory preservation.
- [x] Modularize `app/` into `core/`, `api/`, `schemas/`, `services/`, and `utils/`.
- [x] Create Pydantic v2 schemas for face coordinates, emotional affect profiles, and semblance metrics.
- [x] Build upload pipeline with UUID tracking, header validation, and metadata extraction.
- [x] Author comprehensive documentation (`README.md`, `ARCHITECTURE.md`, `FILING_AND_STORAGE_SYSTEM.md`).

## Phase 2: Computer Vision & Landmark Extraction (Completed / Week 3 Milestone)
- [x] Integrate high-precision face detection backend (OpenCV YuNet ONNX with automated model caching).
- [x] Extract 5 key facial landmarks: right eye, left eye, nose tip, mouth right, mouth left.
- [x] Implement boundary-safe aspect-ratio padding and automatic face chip cropping.
- [x] Store cropped face chips into `storage/processed_faces/` and expose via `/static/faces/`.
- [x] Provide endpoints: `POST /api/v1/faces/detect/{file_id}` and `POST /api/v1/faces/detect-and-crop`.

## Phase 3: Face Embeddings & Similarity (Weeks 5–8)
- [ ] Implement ArcFace / SFace 512-dimensional facial embedding generation.
- [ ] Integrate FAISS vector index for nearest-neighbor similarity search.
- [ ] Pairwise structural likeness computation (cosine similarity & Euclidean distance).

## Phase 4: Archetype Modeling & Semblance Analysis (Weeks 9–10)
- [ ] User archetype base-face model: centroid vector synthesis $\frac{1}{N}\sum \vec{v}_i$.
- [ ] Likeability & human feeling decomposition: Symmetry, Averageness, Warmth (smile), and Structural Softness.
- [ ] Natural language Explanation Engine converting metrics to human-readable summaries.
- [ ] Multi-subject comparison matrix and report generation into `storage/reports/`.
