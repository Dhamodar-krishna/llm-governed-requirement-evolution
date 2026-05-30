import json

from services.llm_service import call_llm


def detect_governance_conflicts(

    actions,
    gate1_results,
    gate2_results,
    gate3_results

):

    prompt = f"""
You are performing GOVERNANCE CONFLICT DETECTION
for adaptive requirement evolution
in a healthcare ICU Cyber-Physical-Social System.

Your task:
- identify conflicting governance objectives,
- detect competing operational constraints,
- identify governance tradeoffs,
- identify incompatible adaptations.

Requirement Evolutions:
{json.dumps(actions, indent=2)}

Gate 1 Results:
{json.dumps(gate1_results, indent=2)}

Gate 2 Results:
{json.dumps(gate2_results, indent=2)}

Gate 3 Results:
{json.dumps(gate3_results, indent=2)}

Possible governance conflicts include:
- alert fatigue reduction
VS
escalation responsiveness

- operational efficiency
VS
patient safety

- workflow optimization
VS
traceability preservation

- adaptive flexibility
VS
governance stability

Return STRICT JSON ONLY.

Required JSON format:

{{
  "conflicts": [
    {{
      "requirement_id": "R-SEP-01",
      "conflict_type": "Operational Tradeoff",
      "conflicting_objectives": [
        "Reduce alert fatigue",
        "Preserve escalation responsiveness"
      ],
      "severity": "Moderate",
      "reasoning": "Explanation"
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

        return parsed["conflicts"]

    except Exception:

        return [
            {
                "requirement_id": "UNKNOWN",
                "conflict_type":
                "Conflict Detection Failure",
                "conflicting_objectives": [],
                "severity": "Unknown",
                "reasoning":
                "Conflict detection parsing failed."
            }
        ]