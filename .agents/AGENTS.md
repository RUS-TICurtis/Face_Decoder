# Project-Scoped Agent Rules & Guidelines

## 1. Stack & Architecture Awareness
- **Backend**: Python 3.10+ with FastAPI, InsightFace / OpenCV, SQLite (SQLAlchemy / aiosqlite), and Vector Stores (Faiss / Qdrant).
- **Frontend**: React 18 / 19 with Vite, Lucide React, and Tailwind / Modern CSS glassmorphic aesthetic.
- **Storage**: Adhere strictly to the storage contract defined in `docs/FILING_AND_STORAGE_SYSTEM.md`.

## 2. Living Documentation Requirement (Mandatory)
- **Primary Documentation**:
  - Architecture: [`docs/ARCHITECTURE.md`](../docs/ARCHITECTURE.md)
  - Storage & Media: [`docs/FILING_AND_STORAGE_SYSTEM.md`](../docs/FILING_AND_STORAGE_SYSTEM.md)
  - References & Tech: [`docs/REFERENCE_PROJECTS_AND_TECHNOLOGIES.md`](../docs/REFERENCE_PROJECTS_AND_TECHNOLOGIES.md)
  - Changelog: [`docs/CHANGELOG.md`](../docs/CHANGELOG.md)
- **Rule**: Whenever any endpoint, model, service, schema, vector adapter, or frontend component is added, modified, refactored, or deleted:
  1. Update or create the relevant markdown documentation in `docs/` in the same turn.
  2. Append all structural or functional changes into [`docs/CHANGELOG.md`](../docs/CHANGELOG.md) with date and context.
  3. Prevent documentation drift.

## 3. Code Quality & Standards
- Python backend code must be clean, asynchronous where I/O bound (`async/await`), strictly typed with Pydantic v2 schemas, and free of unused dependencies or dead code.
- Frontend React components must adhere to clean hook modularity, proper error boundaries, and accessible interactive states.

## 4. Design & Aesthetic Integrity
- Preserve the dark-mode cybernetic/biometric glassmorphism aesthetic.
- Interactive actions must provide immediate visual/animated feedback.
