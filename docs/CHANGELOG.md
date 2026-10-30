# Changelog

All codebase adjustments and additions are documented chronologically here.

## [Unreleased] - 2026-10-30

### Added / Configured
- **Git Ignore Rules for Local Testing & Persistent Stores** ([.gitignore](file:///c:/Users/Curtis/Documents/_Github/Facial_Recognisiton_And_Semblance/.gitignore)):
  - Added patterns to exclude local test images and test media (`test_*.jpg`, `test_*.png`, `test_*.mp4`, `sample_*`, `*.test.*`).
  - Added patterns to exclude temporary testing artifacts, folders, and logs (`tests_output/`, `test_output/`, `temp_*/`, `scratch/`, `*.log`).
  - Excluded local databases and vector collections (`storage/database.sqlite3`, `storage/qdrant/`, `*.sqlite3`, `*.db`) to prevent repository bloat while preserving directories via `.gitkeep`.

- **Agent Framework & Codebase Remediation**:
  - Removed corrupted/non-standard `.agents/skills/app-store-compliance` (missing required `SKILL.md`).
  - Rewrote [.agents/AGENTS.md](file:///c:/Users/Curtis/Documents/_Github/Facial_Recognisiton_And_Semblance/.agents/AGENTS.md) to accurately match the Python FastAPI + React Vite stack instead of Flutter.
  - Added `scipy>=1.11.0` to [requirements.txt](file:///c:/Users/Curtis/Documents/_Github/Facial_Recognisiton_And_Semblance/requirements.txt) required by `resemblance_service.py`.
  - Added `FaceRecord` export to [app/models/__init__.py](file:///c:/Users/Curtis/Documents/_Github/Facial_Recognisiton_And_Semblance/app/models/__init__.py).
  - Resolved frontend unused imports, parameters, and states in `FaceUploader.jsx`, `FaceLibrary.jsx`, and `App.jsx`.
  - Added [tests/test_api_smoke.py](file:///c:/Users/Curtis/Documents/_Github/Facial_Recognisiton_And_Semblance/tests/test_api_smoke.py) for baseline endpoint verification.

- **Frontend Port Alignment & Mobile Responsiveness**:
  - Fixed `ERR_CONNECTION_REFUSED` by creating centralized [frontend/src/config/api.js](file:///c:/Users/Curtis/Documents/_Github/Facial_Recognisiton_And_Semblance/frontend/src/config/api.js) with dynamic origin resolution and Vite dev proxy routing `/api` and `/static` to active uvicorn ports (`8000`/`8001`).
  - Updated [App.jsx](file:///c:/Users/Curtis/Documents/_Github/Facial_Recognisiton_And_Semblance/frontend/src/App.jsx), [FaceLibrary.jsx](file:///c:/Users/Curtis/Documents/_Github/Facial_Recognisiton_And_Semblance/frontend/src/components/features/FaceLibrary.jsx), and [BaselineCreator.jsx](file:///c:/Users/Curtis/Documents/_Github/Facial_Recognisiton_And_Semblance/frontend/src/components/features/BaselineCreator.jsx) to consume `API_BASE` and `FACES_URL`.
  - Added mobile breakpoints (`max-width: 840px` and `max-width: 480px`) in [index.css](file:///c:/Users/Curtis/Documents/_Github/Facial_Recognisiton_And_Semblance/frontend/src/index.css) ensuring responsive tab button wrapping, adaptive glass cards, vertical breakdown for side-by-side grids, and touch-friendly controls.
  - Added iOS `safe-area-inset` support for notches and rounded display corners.
  - Increased mobile touch target sizes for sliders (`24px` thumbs) and upload action boxes.

- **Real-Time Live Camera Integration & Drag-and-Drop Fix**:
  - Upgraded [FaceUploader.jsx](file:///c:/Users/Curtis/Documents/_Github/Facial_Recognisiton_And_Semblance/frontend/src/components/features/FaceUploader.jsx) with WebRTC `navigator.mediaDevices.getUserMedia` live video streaming.
  - Added biometric viewfinder with cybernetic glassmorphism frame, front/rear camera flip (`facingMode: 'user'` vs `'environment'`), natural selfie mirroring, and circular shutter capture.
  - Integrated direct canvas rasterization exporting high-quality JPEG `File` objects directly into the analysis pipeline.
  - Connected `onCapture` prop in [App.jsx](file:///c:/Users/Curtis/Documents/_Github/Facial_Recognisiton_And_Semblance/frontend/src/App.jsx) enabling instantaneous transition from live snapshot to InsightFace and Vibe analysis.
  - Resolved unresponsive Drag-and-Drop by adding HTML5 drag listeners (`onDragEnter`, `onDragOver`, `onDragLeave`, `onDrop`) with active drop states (`isDragging`), dynamic text cues ("Drop Image Here"), and child event suppression (`pointer-events: none`) preventing premature drag cancelation.

- **Scan History Engine & Record Preservation**:
  - Implemented persistent SQLModel [app/models/scan_history.py](file:///c:/Users/Curtis/Documents/_Github/Facial_Recognisiton_And_Semblance/app/models/scan_history.py) storing scanned individual records: `id`, `person_name`, `avatar_crop_filename`, `source_filename`, `vibe_data_json`, `affinity_data_json`, `notes`, and `created_at` timestamp.
  - Exported `ScanHistory` in [app/models/__init__.py](file:///c:/Users/Curtis/Documents/_Github/Facial_Recognisiton_And_Semblance/app/models/__init__.py).
  - Created RESTful API router [app/api/routes_history.py](file:///c:/Users/Curtis/Documents/_Github/Facial_Recognisiton_And_Semblance/app/api/routes_history.py) mounted under `/api/v1/history/` and `/history/`:
    - `POST /`: Validates and saves complete analysis results, person name, notes, and avatar crop filename.
    - `GET /`: Lists scans in chronological descending order (`created_at desc`) with pagination (`limit`, `offset`).
    - `DELETE /{record_id}`: Removes individual scan history entries.
  - Registered history routes in [app/main.py](file:///c:/Users/Curtis/Documents/_Github/Facial_Recognisiton_And_Semblance/app/main.py).
  - Enhanced [frontend/src/components/features/VibeDashboard.jsx](file:///c:/Users/Curtis/Documents/_Github/Facial_Recognisiton_And_Semblance/frontend/src/components/features/VibeDashboard.jsx) with a "Save Scan Record" card featuring an editable Subject Name input, contextual notes textarea, and an interactive "Save to History" action with animated feedback.
  - Built [frontend/src/components/features/ScanHistoryView.jsx](file:///c:/Users/Curtis/Documents/_Github/Facial_Recognisiton_And_Semblance/frontend/src/components/features/ScanHistoryView.jsx):
    - Chronological list displaying avatar crops, subject names, formatted timestamps, Score ③ Appeal badges, and Affinity % pills.
    - Interactive inspection drawer displaying full Archetype profiles, Aesthetic bars, Regional Driver percentages, Gemini Explanation Engine quotes, and custom notes.
    - One-click deletion with instantaneous state updating.
  - Integrated Scan History tab into main navigation in [frontend/src/App.jsx](file:///c:/Users/Curtis/Documents/_Github/Facial_Recognisiton_And_Semblance/frontend/src/App.jsx) and styled in [frontend/src/index.css](file:///c:/Users/Curtis/Documents/_Github/Facial_Recognisiton_And_Semblance/frontend/src/index.css).
