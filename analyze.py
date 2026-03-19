import json
import os
from typing import Any, Dict
# from dotenv import load_dotenv
from litellm import completion

# Load environment variables from .env file
# load_dotenv()

# Get API key from environment
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is not set. Please add it to your .env file.")

# # Set the API key for litellm
# os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# MODEL = "gemini/gemini-2.0-flash"
MODEL = "gemini/gemini-3-flash-preview"


def get_itinerary(destination: str) -> Dict[str, Any]:
    """
    Returns a JSON-like dict with keys:
      - destination
      - price_range
      - ideal_visit_times
      - top_attractions
    """
    
    response_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "recipe_name": {
                    "type": "string",
                },
            },
            "required": ["recipe_name"],
        },
    }
    
    prompt = f"""Generate a travel itinerary for {destination}. 
    Return ONLY valid JSON (no markdown, no extra text) with exactly these keys:
    {{
        "destination": "{destination}",
        "price_range": "budget/moderate/luxury",
        "ideal_visit_times": ["month1", "month2"],
        "top_attractions": ["attraction1", "attraction2", "attraction3"]
    }}"""
    
    try:
        # model = genai.GenerativeModel(MODEL)
        # response = model.generate_content(prompt)
        response = completion(
          model = MODEL,
          messages = [{"role": "user", "content": prompt}]
          # response_format={"type": "json_object", "response_schema": response_schema}
        )
        
        response_text = response.choices[0].message.content
        
        # Parse JSON response
        data = json.loads(response_text)
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response from model: {str(e)}")
    except Exception as e:
        raise Exception(f"Gemini API error: {str(e)}")
