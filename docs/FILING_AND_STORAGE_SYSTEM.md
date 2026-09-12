# Filing and Storage System Specification

## 1. Directory Structure

The application separates transient, raw, normalized, and computed artifacts into designated directories under `storage/`:

```text
storage/
├── raw_images/          # Ingested, unedited uploads
│   └── <uuid>_<clean_filename>.<ext>
├── processed_faces/     # Extracted and normalized face crops
│   └── <uuid>_face_<index>.jpg
├── embeddings/          # Computed vector representations (JSON or .npy)
│   └── <uuid>_features.json
├── reports/             # Persisted semblance comparison artifacts
│   └── <comparison_id>.json
└── cache/               # Temporary scratchpad for transformations
```

## 2. Retention & Git Policy

All media, models, and embeddings stored in `storage/` are excluded from version control via `.gitignore` rules:
```gitignore
storage/raw_images/*
!storage/raw_images/.gitkeep

storage/processed_faces/*
!storage/processed_faces/.gitkeep

storage/embeddings/*
!storage/embeddings/.gitkeep

storage/reports/*
!storage/reports/.gitkeep

storage/cache/*
!storage/cache/.gitkeep
```
This guarantees that:
1. The project can be freshly cloned without missing directories.
2. Large binary assets, test photos, and user uploads never bloat the repository.

## 3. Ingestion & File Naming Conventions

When an image is submitted via `POST /api/v1/upload`:
1. **Sanitization**: Original filename is stripped of path traversal characters (`..`, `/`, `\`) and spaces are replaced with underscores.
2. **UUID Prefixing**: A unique UUIDv4 is assigned (e.g. `e1c4a03b-d519-487d-815d-0072eb0f3f2d`).
3. **Storage Format**:
   ```
   storage/raw_images/{UUID}_{sanitized_original_filename}
   ```
4. **Validation**: Header verification is executed via PIL; if non-conforming or larger than `MAX_FILE_SIZE_BYTES` (15 MB), the file is cleaned up immediately and rejected.
