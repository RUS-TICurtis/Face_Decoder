# Technology & Research Reference Map

**Face Decoder — Technical Intelligence Document**

> This document is a curated reference library for the coding agents and developers working on this project. It maps existing GitHub repositories, models, datasets, APIs, and SDKs to their specific roles in our architecture, indicating what to borrow, what to avoid, and what we build ourselves.

---

## 1. Architecture Overview (Revised)

Our system has **five distinct engines**, each with its own ML stack:

```
┌─────────────────────┐
│   Flutter Mobile    │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│    Web App (React)  │
└──────────┬──────────┘
           │ REST / WebSocket
┌──────────▼──────────┐
│      FastAPI        │
│    API Gateway      │
└──────────┬──────────┘
           │
  ┌────────┼────────────┐
  ↓        ↓            ↓
Face    Embedding    Video
Detection  Engine    Engine
RetinaFace/ InsightFace/ Frame sampling
SCRFD    ArcFace
  │        │
  └────────┤
           ↓
  ┌───────────────┐
  │  Vector Store  │
  │ FAISS → Qdrant │
  └──────┬────────┘
         │
  ┌──────┼──────────────┐
  ↓      ↓              ↓
Identity Resemblance  Archetype
Engine   Engine       Engine
         │
         ↓
  Personal Affinity
         │
  ┌──────┴──────────────┐
  ↓                     ↓
Appeal/Perception    Explanation
Analysis Engine       Engine
```

## 2. The Four-Score Model

Our core innovation is a **four-score output** per face analysis. These are NOT the same thing, and must be kept separate:

| Score | Question | Basis |
|---|---|---|
| **① Identity Similarity** | Could these be the same person? | ArcFace embedding cosine distance |
| **② Resemblance** | How much does Face A visually resemble Face B? | Embedding distance + geometric features |
| **③ Perceptual Appeal** | How aesthetically appealing is this face, objectively? | Trained on SCUT-FBP5500 dataset |
| **④ Personal Affinity** | How closely does this face match *my* personal archetype? | User-defined baseline embedding |

> **Important Note**: Attractiveness ≠ Likeability ≠ Approachability ≠ Personal Preference. These are different psychological constructs and must NOT be conflated into a single score.

---

## 3. Reference Projects

### 3a. Face Detection & Embedding Pipelines

| Repo | Link | What to borrow |
|---|---|---|
| **face_recognition (Shi1f2)** | [GitHub](https://github.com/Shi1f2/face_recognition) | Image → RetinaFace → ArcFace → FAISS ranked matches. Study pipeline architecture. |
| **face-recognition-search (bassalemi)** | [GitHub](https://github.com/bassalemi/face-recognition-search) | InsightFace + FAISS + perceptual hashing + duplicate detection + web UI. Ideas for Face Library/Database Explorer. |
| **face-search (albertkao227)** | [GitHub](https://github.com/albertkao227/face-search) | ✅ **Best architectural reference.** Mirrors our folder structure. Borrow the `detector.py` / `embedder.py` / `indexer.py` / `search.py` decomposition pattern. |

**Key folder structure to emulate (from face-search):**
```
data/
  raw_photos/
  face_crops/
  faiss_index.bin
  metadata.json
src/
  config.py
  detector.py
  embedder.py
  indexer.py
  search.py
  app.py
```

### 3b. Lookalike / Casting Resemblance

| Repo | Link | What to borrow |
|---|---|---|
| **lookalike (haydenjeune)** | [GitHub](https://github.com/haydenjeune/lookalike) | ✅ **Most relevant to our casting engine.** 40,000+ celebrity faces, <200ms response. Study the embedding + FAISS retrieval flow. |

> **Our differentiation vs lookalike:** Their question: *"Who does this person look like?"* Our question: *"Who does this person resemble, what characteristics create that resemblance, how close are they to a personal aesthetic archetype, and which candidates fit a specific casting requirement?"*

### 3c. Million-Scale Retrieval

| Repo | Link | What to borrow |
|---|---|---|
| **SENTINEL face-retrieval (gallardorafael)** | [GitHub](https://github.com/gallardorafael/sentinel-face-retrieval) | EdgeFace lightweight embeddings, CPU-friendly at 1M+ points. **Do not implement now.** Design interfaces to allow swapping vector-search implementation later. |

### 3d. Perceptual Appeal & Explainability

| Repo | Link | What to borrow |
|---|---|---|
| **FaceHeauty (uladzislau-varabei)** | [GitHub](https://github.com/uladzislau-varabei/faceheauty) | ✅ **Key inspiration.** Beauty score + **regional heatmaps** + FaceNet/InsightFace backbones + web app. The heatmap/explanation concept is critical for us. |
| **BeautyPredict (TheL1Samurai)** | [GitHub](https://github.com/TheL1Samurai/BeautyPredict) | Implementation on SCUT-FBP5500 dataset. Study multiple ML approaches to beauty prediction. |

### 3e. Production API Architecture

| Repo | Link | What to borrow |
|---|---|---|
| **deepface-rest-api (DmytroGural)** | [GitHub](https://github.com/DmytroGural/deepface-rest-api) | Face verification, analysis, embeddings, extraction, Docker deployment, structured API responses. Study API contract design. |

---

## 4. Models & Embedding Engines

| Model | Task | Status |
|---|---|---|
| **RetinaFace** | Face detection + 5-point landmarks | ✅ Use for detection |
| **SCRFD** | Faster lightweight detection alternative | ⚠️ Consider for mobile inference |
| **ArcFace (InsightFace)** | 512-D identity embedding | ✅ Core of identity + resemblance engine |
| **EdgeFace** | Lightweight embedder for scale | ⏳ Future: million-scale only |

> **Do NOT use**: OpenCV Haar Cascades (too imprecise), raw DeepFace (black box with no control), any model that predicts ethnicity/race from appearance.

---

## 5. Datasets

| Dataset | Description | Use Case |
|---|---|---|
| **SCUT-FBP5500** | 5,500 frontal faces, beauty ratings, landmarks, demographic diversity | Training/fine-tuning the Perceptual Appeal engine |

---

## 6. Vector Databases

| Technology | Phase | Rationale |
|---|---|---|
| **FAISS (Facebook)** | ✅ MVP → Thousands | In-memory, no infrastructure, fast to iterate |
| **Qdrant** | ⏳ Phase 2 → Tens of thousands | Filtering + metadata + REST API + Docker |
| **Milvus** | ⏳ Phase 3 → Millions | Distributed, cloud-native, enterprise-scale |

> **Architectural principle**: Design vector-search interfaces as swappable adapters. The business logic never talks directly to FAISS. It calls `vector_store.search(embedding, k=20)`. Swapping FAISS for Qdrant requires changing one file only.

---

## 7. APIs & Commercial Products

| Product | Link | Role |
|---|---|---|
| **Microsoft Azure Face — Find Similar** | [Docs](https://learn.microsoft.com/en-us/rest/api/face/face-recognition-operations/find-similar-from-face-list) | ✅ **Validates our concept.** Microsoft ships a commercial "Find Similar Faces" API. Study their API contract. |
| **InsightFace Server** | [Site](https://www.insightface.ai/solutions/insightface-server) | Self-hosted recognition pipeline. Study: detect → align → embed → normalize → search → ranked results. |

---

## 8. What We Build Ourselves (Our Differentiating Layer)

**We do NOT innovate on:** ArcFace, FAISS, RetinaFace, or REST API scaffolding. These are infrastructure.

**We innovate on:**

```
Reference Faces
      ↓
Personal Archetype (user-defined baseline)
      ↓
Feature / Embedding Analysis
      ↓
Resemblance + Appeal + Personal Affinity
      ↓
Explanation Layer
```

**Target output (our product's unique value):**
```
PERSONAL AFFINITY: 87/100

Primary contributors
────────────────────
Eye region        █████████  91
Facial symmetry   ████████   86
Face proportions  ████████   84
Smile/warmth      ███████    78
Jaw structure     ██████     69

Why? Your selected reference faces tend to share
these structural characteristics.
```

---

## 9. What NOT to Build

| Item | Reason |
|---|---|
| Custom face detector from scratch | RetinaFace/SCRFD exist and are state of the art |
| Custom ArcFace training from scratch | Pre-trained weights are better than we can fine-tune |
| Ethnicity/race prediction from appearance | Unreliable, ethically problematic, not part of our product |
| Calling a single "Likeability" score | Scientifically incorrect — split into the 4 scores |

---

## 10. Recommended Next Steps (Pre-Week 3)

1. ✅ Update the PRD to reflect the **4-score model**
2. ✅ Commit this reference map to `docs/`
3. ⏳ Integrate **InsightFace + ArcFace** embedding pipeline (replacing current YuNet → Gemini flow)
4. ⏳ Build a **FAISS vector store adapter** with a swappable interface
5. ⏳ Design the **Baseline / Personal Archetype** data model in Postgres
6. ⏳ Prototype the **Explanation Engine** using FaceHeauty's regional heatmap concept

---

*Last updated: 2026-09-12*
*Maintained by: Technical Co-Founder / Lead Engineer*
