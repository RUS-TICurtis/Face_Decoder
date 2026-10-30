import json
from pathlib import Path
from typing import Dict, Any, Union
from google import genai
from PIL import Image

from app.core.config import settings

class VibeAnalysisService:
    def __init__(self):
        # Initialize the Gemini client
        self.api_key = settings.GEMINI_API_KEY
        if not self.api_key:
            print("WARNING: GEMINI_API_KEY is not set in the configuration.")
            self.client = None
        else:
            self.client = genai.Client(api_key=self.api_key)

    def analyze_face(self, image_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Analyzes a face image and scores it on configured archetypes and aesthetics.
        """
        if not self.client:
            raise ValueError("Gemini API key is not configured. Cannot perform vibe analysis.")

        # Load the image
        img = Image.open(image_path)

        # Prepare the prompt
        archetypes_str = ", ".join(settings.ARCHETYPES)
        aesthetics_str = ", ".join(settings.AESTHETICS)
        
        prompt = f"""
        Analyze this face image and act as an expert computer vision and aesthetic explanation engine.
        
        1. Rate it on the following subjective archetypes (0 to 100):
        {archetypes_str}
        
        2. Rate it on these subjective aesthetics (0 to 100):
        {aesthetics_str}
        
        3. Provide a 'perceptual_appeal' score (0 to 100) acting as a proxy for structural and perceptual beauty.
        
        4. Break down the 'regional_contributions' (how much each region drives the overall aesthetic or structural resemblance, each 0 to 100).
        
        5. Provide a 1-2 sentence 'explanation' summarizing the key structural drivers (e.g. "The strong jawline symmetry and eye proportions are the primary drivers of this look.")
        
        Respond with ONLY a valid JSON object in the exact following format, without markdown blocks or any other text:
        {{
            "archetypes": {{
                "Approachable": 85,
                "Regal": 40
            }},
            "aesthetics": {{
                "cute": 90,
                "10/10": 80
            }},
            "perceptual_appeal": 85,
            "regional_contributions": {{
                "eyes": 91,
                "nose": 75,
                "mouth": 82,
                "jawline_symmetry": 88,
                "proportions": 84
            }},
            "explanation": "Eye region and facial symmetry are the primary aesthetic drivers."
        }}
        """

        # Call Gemini 3.6 Flash
        response = self.client.models.generate_content(
            model='gemini-3.6-flash',
            contents=[img, prompt]
        )

        # Parse the JSON response
        try:
            # Clean up the response in case it returns markdown formatting (e.g. ```json ... ```)
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
                
            result = json.loads(text.strip())
            return result
        except Exception as e:
            raise RuntimeError(f"Failed to parse Gemini response: {e}\nRaw Response: {response.text}")

vibe_service = VibeAnalysisService()
