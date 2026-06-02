import json
import re

from services.llm_service import call_llm


def run_stage2(
    change,
    stage1_output,
    requirements
):

    prompt = f"""
You are performing requirement impact analysis.

ONLY use these requirement IDs:
- R-SEP-01
- R-SEP-02
- R-ALT-07

Guideline Change:
{change}

Stage 1 Output:
{json.dumps(stage1_output, indent=2)}

Requirements:
{json.dumps(requirements, indent=2)}

IMPORTANT:

- Identify BOTH direct and indirect impacts.
- Direct impacts modify explicit requirement semantics.
- Indirect impacts affect operational behavior,
  governance dependencies,
  reassessment logic,
  escalation flow,
  or alert behavior.

- If no meaningful governance impact exists,
  return an empty list.

- Do NOT invent unrelated propagation.
- Do NOT create artificial dependencies.

Return STRICT JSON ONLY.

Example format:

{{
  "affected_requirements": [
    {{
      "id": "R-SEP-01",
      "impact_type": "direct/indirect",
      "reasoning": "Explanation"
    }}
  ]
}}
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

        result = json.loads(json_text)

        valid_ids = [
            "R-SEP-01",
            "R-SEP-02",
            "R-ALT-07"
        ]

        hallucinated = []

        valid_requirements = []

        for req in result.get(
            "affected_requirements",
            []
        ):

            if req["id"] in valid_ids:

                valid_requirements.append(req)

            else:

                hallucinated.append(req["id"])

        result["affected_requirements"] = valid_requirements

        result["hallucinated_ids"] = hallucinated

        result["hallucination_count"] = len(hallucinated)

        return result

    except Exception:

        return {

            "error": "Invalid JSON response",

            "raw_response": response
        }