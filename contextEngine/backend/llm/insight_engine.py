import json
from llm.client import generate_response

def generate_wording(base_output: dict) -> dict:
    """
    Takes base engine output and returns structured LLM insight.
    Uses llm.client.generate_response instead of direct Ollama calls.
    """

    # --- Extract signal-level data only ---
    signals = {
        "performance_status": base_output["performance_status"],
        "engagement_rate": base_output["engagement_profile"]["engagement_rate"],
        "save_rate": base_output["engagement_profile"]["save_rate"],
        "share_rate": base_output["engagement_profile"]["share_rate"],
        "dominant_engagement": base_output["engagement_profile"]["dominant_engagement"],
        "content_value_type": base_output["content_value_type"],
        "hook_strength": base_output["hook_analysis"]["hook_strength"],
        "fatigue_level": base_output["topic_health"]["fatigue_level"],
        "intent_match": base_output["audience_alignment"]["intent_match"],
        "timing_quality": base_output["distribution_health"]["timing_quality"],
        "decay_pattern": base_output["distribution_health"]["decay_pattern"]
    }

    # Optional: include reasoning if you have it in base_output
    reasoning = base_output.get("reasoning", "")

    # Build prompt
    prompt = f"""
    Analyze these content signals:
    {json.dumps(signals, indent=2)}

    Reasoning:
    {reasoning}

    Return JSON:
    {{
      "success_driver": "",
      "failure_reason": "",
      "recommendations": [],
      "confidence_score": 0.0
    }}
    """

    try:
        response = generate_response(prompt)

        # --- Safe JSON parsing ---
        try:
            parsed = json.loads(response)
        except json.JSONDecodeError:
            parsed = {
                "failure_reason": None,
                "success_driver": None,
                "recommendations": [],
                "confidence_score": 0.0,
                "raw_llm_output": response
            }

        return {
            "content_id": base_output["content_id"],
            "llm_insight": parsed
        }

    except Exception as e:
        return {
            "content_id": base_output["content_id"],
            "error": str(e)
        }
