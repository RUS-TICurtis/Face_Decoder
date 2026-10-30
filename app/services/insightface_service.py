import os
from pathlib import Path
from typing import List, Optional
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis

from app.core.config import settings
from app.schemas.face import (
    FaceBoundingBox,
    LandmarkPoint,
    FacialLandmarks,
    DetectedFace,
    FaceAnalysisResponse,
    ImageDimensions,
)

class InsightFaceService:
    """
    Production-grade Face Detection, Alignment, and Embedding Extraction Service
    powered by InsightFace (buffalo_l model pack).
    Extracts bounding boxes, 5 key landmarks (eyes, nose, mouth corners), 
    crops faces, and generates 512-D ArcFace identity embeddings.
    """

    def __init__(self):
        # We specify providers=['CPUExecutionProvider'] to ensure it runs on CPU for this MVP
        self.app = FaceAnalysis(name="buffalo_l", providers=['CPUExecutionProvider'])
        # det_size=(640, 640) is standard for RetinaFace
        self.app.prepare(ctx_id=0, det_size=(640, 640))

    def detect_and_embed(
        self,
        image_path: Path,
        file_id: str,
        padding_ratio: float = 0.15
    ) -> FaceAnalysisResponse:
        """
        Detect faces in the given image, extract 5 landmarks and embeddings,
        and save cropped face chips into storage/processed_faces/.
        """
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found at path: {image_path}")

        # Read image
        img = cv2.imread(str(image_path))
        if img is None:
            raise ValueError(f"Failed to read image binary at: {image_path}")

        h, w = img.shape[:2]
        
        # Detect faces (retinaface + arcface)
        faces = self.app.get(img)

        detected_faces: List[DetectedFace] = []

        if faces is not None:
            settings.PROCESSED_FACES_DIR.mkdir(parents=True, exist_ok=True)

            for idx, raw_face in enumerate(faces):
                # Bounding box coordinates
                bx1, by1, bx2, by2 = raw_face.bbox
                bw = bx2 - bx1
                bh = by2 - by1
                conf = float(raw_face.det_score)

                # Landmarks: 5 points (left_eye, right_eye, nose, mouth_left, mouth_right)
                # Note: Insightface returns a 5x2 array
                kps = raw_face.kps
                landmarks = FacialLandmarks(
                    left_eye=LandmarkPoint(x=float(kps[0][0]), y=float(kps[0][1])),
                    right_eye=LandmarkPoint(x=float(kps[1][0]), y=float(kps[1][1])),
                    nose_tip=LandmarkPoint(x=float(kps[2][0]), y=float(kps[2][1])),
                    mouth_left=LandmarkPoint(x=float(kps[3][0]), y=float(kps[3][1])),
                    mouth_right=LandmarkPoint(x=float(kps[4][0]), y=float(kps[4][1])),
                )

                bbox = FaceBoundingBox(
                    x=int(max(0, bx1)),
                    y=int(max(0, by1)),
                    width=int(bw),
                    height=int(bh),
                    confidence=round(conf, 4),
                )

                # ArcFace 512-D embedding
                embedding = raw_face.embedding.tolist() if raw_face.embedding is not None else None

                # Compute padded crop boundary
                pad_w = int(bw * padding_ratio)
                pad_h = int(bh * padding_ratio)

                crop_x1 = max(0, int(bx1 - pad_w))
                crop_y1 = max(0, int(by1 - pad_h))
                crop_x2 = min(w, int(bx1 + bw + pad_w))
                crop_y2 = min(h, int(by1 + bh + pad_h))

                face_chip = img[crop_y1:crop_y2, crop_x1:crop_x2]

                crop_filename = f"{file_id}_face_{idx}.jpg"
                crop_path = settings.PROCESSED_FACES_DIR / crop_filename

                # Save cropped face chip
                cv2.imwrite(str(crop_path), face_chip)

                face_obj = DetectedFace(
                    face_id=f"{file_id}_face_{idx}",
                    index=idx,
                    bbox=bbox,
                    landmarks=landmarks,
                    confidence=round(conf, 4),
                    crop_filename=crop_filename,
                    crop_path=str(crop_path),
                    embedding=embedding
                )
                detected_faces.append(face_obj)

        return FaceAnalysisResponse(
            file_id=file_id,
            image_dimensions=ImageDimensions(width=w, height=h),
            total_faces=len(detected_faces),
            faces=detected_faces,
        )

# Global singleton
insightface_service = InsightFaceService()
