import json
import subprocess

MODEL_NAME = "mistral"


def generate_insight(base_output):
    prompt = f"""
You are an expert content performance analyst.

You will receive a structured JSON object that represents the interpreted performance
of a single piece of digital content.

RULES:
- Do NOT invent metrics
- Do NOT contradict the input
- Base all reasoning ONLY on the input
- Respond ONLY in valid JSON
- Follow the exact output schema below
- No markdown, no explanations outside JSON

OUTPUT SCHEMA:
{{
  "content_id": "string",
  "overall_verdict": "success | average | failure",
  "performance_explanation": {{
    "summary": "string",
    "key_reasons": ["string"]
  }},
  "primary_drivers": {{
    "positive_drivers": ["string"],
    "negative_drivers": ["string"]
  }},
  "content_diagnosis": {{
    "hook_quality": "strong | medium | weak",
    "content_value_alignment": "string",
    "audience_response": "string"
  }},
  "distribution_diagnosis": {{
    "timing_effectiveness": "good | average | poor",
    "longevity_assessment": "string"
  }},
  "recommended_actions": {{
    "content_changes": ["string"],
    "distribution_changes": ["string"],
    "experiments_to_try": ["string"]
  }},
  "confidence_score": 0.0
}}

INPUT:
{json.dumps(base_output, indent=2)}
"""

    result = subprocess.run(
        ["ollama", "run", MODEL_NAME],
        input=prompt,
        capture_output=True,
        text=True
    )

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        raise ValueError("LLM returned invalid JSON")
