import os
from pathlib import Path
from typing import Set, List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Facial Recognition & Semblance API"
    VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # API Keys
    GEMINI_API_KEY: str = ""
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    
    # Base directory for the project
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    
    # Storage configuration
    STORAGE_DIR: Path = BASE_DIR / "storage"
    RAW_IMAGES_DIR: Path = STORAGE_DIR / "raw_images"
    PROCESSED_FACES_DIR: Path = STORAGE_DIR / "processed_faces"
    EMBEDDINGS_DIR: Path = STORAGE_DIR / "embeddings"
    REPORTS_DIR: Path = STORAGE_DIR / "reports"
    CACHE_DIR: Path = STORAGE_DIR / "cache"
    
    # Upload constraints
    ALLOWED_EXTENSIONS: Set[str] = {"jpg", "jpeg", "png", "webp", "bmp"}
    MAX_FILE_SIZE_BYTES: int = 15 * 1024 * 1024  # 15 MB
    
    # Semblance & Feeling Analysis Defaults
    DEFAULT_CONFIDENCE_THRESHOLD: float = 0.60
    DEFAULT_SEMBLANCE_METRIC: str = "cosine"
    
    # Subjective Traits for Vision API
    ARCHETYPES: List[str] = [
        "Approachable", 
        "Regal", 
        "Mysterious", 
        "Trustworthy"
    ]
    AESTHETICS: List[str] = [
        "cute", 
        "10/10", 
        "spec", 
        "beautiful", 
        "handsome"
    ]

settings = Settings()
