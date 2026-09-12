# Facial Recognition & Semblance Engine (Face Decoder)

An intelligent Python and FastAPI platform engineered for **Facial Recognition, Human Emotion & Affect Analysis, and Semblance Likeness Evaluation**.

Unlike conventional facial verification tools that only assess biometrics or 1:1 identity matching, this project focuses deeply on **"Semblance"**—the nuanced visual, emotional, and affective likeness between human expressions. It bridges computer vision with computational affective science to detect faces, measure feeling states (valence, arousal, expression archetypes), and quantify how closely two subjects resonate in mood and appearance.

---

## 🌟 Key Capabilities

- **Facial Ingestion & Storage Filing System**: Secure image intake with UUID isolation, format validation, and automated directory partitioning.
- **Human Feeling & Affect Profiling**: Extraction of emotional vectors representing primary feeling states (e.g. joy, serenity, sorrow, tension, wonder, neutral) along with valence and arousal metrics.
- **Dual-Dimensional Semblance Scoring**:
  - **Structural Semblance**: Visual and geometric feature correspondence between facial contours.
  - **Emotional Semblance**: Mathematical likeness between emotional feeling profiles.
  - **Composite Semblance**: Weighted score synthesizing physical and emotive semblance.
- **RESTful API Architecture**: Fast and modular FastAPI endpoints with OpenAPI / Swagger documentation out of the box.

---

## 🗂️ Project & Filing Structure

```text
Facial_Recognisiton_And_Semblance/
├── app/
│   ├── api/                     # API routers and endpoints
│   │   ├── routes_upload.py     # Image upload and validation routes
│   │   └── routes_semblance.py  # Face detection & semblance analysis routes
│   ├── core/                    # Core configuration and settings
│   │   └── config.py            # Global settings & storage paths
│   ├── models/                  # (Reserved for ORM / database entities)
│   ├── schemas/                 # Pydantic data contracts (DTOs)
│   │   └── face.py              # Face, emotion, and semblance schemas
│   ├── services/                # Business logic
│   │   ├── file_service.py      # Storage, UUID naming, and safe file I/O
│   │   └── semblance_service.py # Affect analysis & semblance scoring
│   ├── utils/                   # Utility helpers
│   │   └── image_utils.py       # Image validation & stream handling
│   └── main.py                  # Application entrypoint & middleware
├── docs/                        # Architectural & design documentation
│   ├── ARCHITECTURE.md          # Detailed system architecture
│   ├── FILING_AND_STORAGE_SYSTEM.md # Storage filing taxonomy & lifecycle
│   └── ROADMAP.md               # Upcoming models, pipelines & research
├── storage/                     # Local file-based storage hierarchy
│   ├── raw_images/              # Ingested original images
│   ├── processed_faces/         # Normalized and cropped face chips
│   ├── embeddings/              # Extracted feature vectors and cache
│   ├── reports/                 # Semblance comparison reports
│   └── cache/                   # Temporary processing cache
├── .gitignore                   # Comprehensive exclusions for Python/media
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.14)
- Git

### 2. Environment Setup
```bash
# Clone the repository
git clone https://github.com/RUS-TICurtis/Face_Decoder.git
cd Face_Decoder

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Launching the Development Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Visit the interactive Swagger API documentation at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔌 API Reference

### System
- `GET /` - Root status, project metadata, and filing system paths.
- `GET /health` - Service health check.

### Ingestion & Storage
- `POST /api/v1/upload` (or `/upload`)
  - **Payload**: `multipart/form-data` with `file: UploadFile`
  - **Returns**: `file_id`, dimensions, size, sanitized storage path.

### Semblance & Affect Analysis
- `GET /api/v1/semblance/detect/{file_id}`
  - Detects faces and extracts affective emotion scores (valence, arousal, primary feeling).
- `POST /api/v1/semblance/compare`
  - **Payload**:
    ```json
    {
      "source_file_id": "3b29c51c-...",
      "target_file_id": "8f1a23e9-..."
    }
    ```
  - **Returns**: Structural semblance, emotional feeling resemblance, composite score, and qualitative evaluation.

---

## 📚 Further Documentation

For deep technical details:
- [System Architecture](file:///docs/ARCHITECTURE.md)
- [Filing and Storage System](file:///docs/FILING_AND_STORAGE_SYSTEM.md)
- [Project Roadmap](file:///docs/ROADMAP.md)

---

## 📄 License
MIT License.
