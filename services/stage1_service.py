import json
import re

from services.llm_service import call_llm


def run_stage1(change_text):

    prompt = f"""
You are assisting with requirement evolution
in a healthcare ICU Cyber-Physical-Social System.

Analyze the following guideline update.

Return ONLY valid JSON.

Required JSON format:

{{
    "change_type": "...",
    "operational_implications": [
        "...",
        "..."
    ],
    "affected_system_areas": [
        "...",
        "..."
    ]
}}

Guideline Update:
{change_text}
"""

    response = call_llm(prompt)

    try:

        cleaned = response.strip()

        # =============================================
        # ROBUST JSON EXTRACTION
        # =============================================

        match = re.search(

            r"\{.*\}",

            cleaned,

            re.DOTALL
        )

        if not match:

            raise ValueError(
                "No JSON object found."
            )

        json_text = match.group(0)

        parsed = json.loads(json_text)

        return parsed

    except Exception:

        return {

            "error": "Invalid JSON response",

            "raw_response": response
        }