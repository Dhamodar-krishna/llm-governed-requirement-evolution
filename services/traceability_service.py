import json

from services.llm_service import call_llm


def run_gate3(requirement_actions):

    prompt = f"""
You are performing TRACEABILITY INTEGRITY validation
for adaptive requirement evolution
in a healthcare ICU Cyber-Physical-Social System.

Evaluate ALL evolved requirements together.

Requirement Evolutions:
{json.dumps(requirement_actions, indent=2)}

Traceability concerns include:
- preserving semantic continuity,
- preserving explainability,
- preserving provenance integrity,
- preserving governance lineage,
- preserving auditability.

Possible governance states:
- PASS
- REVIEW
- FAIL

Rules:
- FAIL if traceability integrity breaks.
- REVIEW if explainability high risks exist.
- PASS if traceability remains preserved, even with moderate concerns. 

Return STRICT JSON ONLY.

Required JSON format:

{{
  "results": [
    {{
      "id": "R-SEP-01",
      "gate_result": "PASS/REVIEW/FAIL",
      "reason": "Explanation",
      "traceability_risk": "Risk Description"
    }}
  ]
}}
"""

    response = call_llm(prompt)

    try:

        cleaned = response.strip()

        if cleaned.startswith("```json"):

            cleaned = cleaned.replace(
                "```json",
                ""
            )

            cleaned = cleaned.replace(
                "```",
                ""
            )

        parsed = json.loads(cleaned)

        return parsed["results"]

    except Exception:

        return [
            {
                "id": "UNKNOWN",
                "gate_result": "REVIEW",
                "reason":
                "Gate 3 parsing failure.",
                "traceability_risk":
                "Unknown"
            }
        ]