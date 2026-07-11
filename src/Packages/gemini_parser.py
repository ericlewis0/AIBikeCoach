from google import genai
import os
from dotenv import load_dotenv
import json
from .models import AthleteProfile, TrainingPlan
from .prompts import build_prompt


load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

def generate_plan(profile: AthleteProfile) -> TrainingPlan:
    prompt = build_prompt(profile)
    
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=TrainingPlan,
            system_instruction= (
                "You are an expert cycling coach."
                "Return only valid JSON."
                "No markdown, no explanation, no preamble."
            ),
            temperature=0.2,
            max_output_tokens=5000
        )
    )
    plan_dict = json.loads(response.text)
    with open('plan_test.json','w', encoding='utf-8') as file:
        json.dump(plan_dict, file, indent=4)
    return TrainingPlan(**plan_dict)
  
