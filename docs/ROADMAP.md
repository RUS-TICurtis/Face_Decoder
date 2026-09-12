# Development Roadmap: Face Decoder
*Personalized Facial Resemblance & Perceptual Affinity Engine*

> See `docs/REFERENCE_PROJECTS_AND_TECHNOLOGIES.md` for the full technology reference map.

---

## Phase 1: Core Foundation & Modular Filing System ✅
- [x] Establish `.gitignore`, structured file storage taxonomy, and `.gitkeep` preservation.
- [x] Modularize `app/` into `core/`, `api/`, `schemas/`, `services/`, and `utils/`.
- [x] Build upload pipeline with UUID tracking, header validation, and metadata extraction.
- [x] Author comprehensive documentation (`README.md`, `ARCHITECTURE.md`).

## Phase 2: Computer Vision & Landmark Extraction ✅
- [x] Integrate high-precision face detection (OpenCV YuNet ONNX + automated model caching).
- [x] Extract 5 key facial landmarks: right eye, left eye, nose tip, mouth corners.
- [x] Implement boundary-safe padded face chip cropping → `storage/processed_faces/`.
- [x] Endpoints: `POST /api/v1/faces/detect/{file_id}` and `POST /api/v1/faces/detect-and-crop`.

## Phase 2.5: Vibe Analysis & Frontend MVP ✅
- [x] Integrate Gemini 3.6 Flash Vision API for zero-shot archetype/aesthetic scoring.
- [x] Build modular React + Vite frontend with glassmorphism design system.
- [x] Implement FaceUploader, VibeDashboard, and BaselineCreator components.
- [x] Create tab-based navigation between "Analyze Photo" and "Define Baselines".
- [x] Produce scores for: Approachable, Regal, Mysterious, Trustworthy, cute, 10/10, spec, beautiful, handsome.

## Phase 3: ArcFace Embeddings & Vector Search (Next)
> **Reference**: albertkao227/face-search architecture, haydenjeune/lookalike, InsightFace Server
- [ ] Replace YuNet with InsightFace / RetinaFace for higher-fidelity detection + alignment.
- [ ] Generate ArcFace 512-D identity embeddings per face chip.
- [ ] Build a **swappable vector store adapter** (FAISS now → Qdrant/Milvus later).
- [ ] Implement pairwise cosine similarity and Euclidean distance search.
- [ ] Produce **Score ①: Identity Similarity** and **Score ②: Resemblance** per face pair.

## Phase 4: Personal Archetype & Affinity Engine
> **Reference**: haydenjeune/lookalike, Microsoft Azure Find Similar
- [ ] Persist Baseline subjects to PostgreSQL (name, reference photos, embedding centroid).
- [ ] Compute personal archetype vector: `centroid = (1/N) Σ v_i` across reference faces.
- [ ] Build cosine-similarity comparison of new face against archetype centroid.
- [ ] Produce **Score ④: Personal Affinity** with delta breakdown.
- [ ] Connect frontend "Save Baseline" button to backend database.

## Phase 5: Perceptual Appeal & Explanation Engine
> **Reference**: FaceHeauty (heatmaps), SCUT-FBP5500 dataset, BeautyPredict
- [ ] Fine-tune or integrate a perceptual attractiveness model on SCUT-FBP5500 dataset.
- [ ] Produce **Score ③: Perceptual Appeal** with regional contribution heatmap.
- [ ] Build Explanation Engine: convert embedding delta → natural language summary.
- [ ] Target output: "Eye region (91%), Facial symmetry (86%), Face proportions (84%) are primary similarity drivers."

## Phase 6: Scale, Search & Casting Engine
> **Reference**: SENTINEL (million-scale), bassalemi/face-recognition-search
- [ ] Swap FAISS for Qdrant (tens of thousands of faces).
- [ ] Build Face Library explorer: search, filter, bulk-index celebrity/casting databases.
- [ ] Implement duplicate detection via perceptual hashing.
- [ ] Support video frame sampling as input source.

