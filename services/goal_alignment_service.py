import json

from services.llm_service import call_llm


def run_gate2(requirement_actions):

    prompt = f"""
You are performing GOAL ALIGNMENT validation
for adaptive requirement evolution
in a healthcare ICU Cyber-Physical-Social System.

Evaluate ALL evolved requirements together.

Requirement Evolutions:
{json.dumps(requirement_actions, indent=2)}

Operational goals include:
- maintaining ICU workflow efficiency,
- reducing clinician alert fatigue,
- preserving escalation responsiveness,
- supporting operational safety,
- minimizing workflow disruption.

Possible governance states:
- PASS
- REVIEW
- FAIL

Rules:
- FAIL if operational goals are violated.
- REVIEW if heavy operational tradeoffs and uncertainties exist.
- PASS if goals remain aligned, even with moderate concerns.

Return STRICT JSON ONLY.

Required JSON format:

{{
  "results": [
    {{
      "id": "R-SEP-01",
      "gate_result": "PASS",
      "reason": "Explanation",
      "affected_goal": "Goal Name"
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
                "Gate 2 parsing failure.",
                "affected_goal":
                "Unknown"
            }
        ]