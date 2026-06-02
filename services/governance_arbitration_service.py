import json

from services.llm_service import call_llm


def run_governance_arbitration(

    conflict_results

):

    prompt = f"""
You are performing GOVERNANCE ARBITRATION
for adaptive requirement evolution
in a safety-critical ICU Cyber-Physical-Social System.

Your task:
- prioritize conflicting governance objectives,
- determine dominant governance priorities,
- resolve adaptive tradeoffs,
- recommend governance-aligned decisions.

IMPORTANT:

Generate only one arbitration decision
for each requirement_id.

The arbitration result must resolve
the highest-priority governance conflict.

Do not generate multiple arbitration outcomes
for the same requirement.

Conflict Results:
{json.dumps(conflict_results, indent=2)}

IMPORTANT:

The conflicting objectives contained within
Conflict Results are the authoritative governance
conflicts identified by the Conflict Detection Layer.

You are NOT identifying new objectives.

You are NOT reformulating objectives.

You are NOT introducing additional governance goals.

For each requirement:

- use the conflicting objectives exactly as provided,
- select the dominant objective,
- select the suppressed objective,
- justify the prioritization using the governance hierarchy.

The dominant_objective field MUST exactly match
one of the objectives supplied by Conflict Detection.

The suppressed_objective field MUST exactly match
one of the objectives supplied by Conflict Detection.

Priority hierarchy:
1. Patient safety
2. Escalation responsiveness
3. Operational stability
4. Traceability integrity
5. Workflow efficiency
6. Alert fatigue reduction

Rules:
- Higher-priority governance objectives dominate lower-priority objectives.
- Safety-critical objectives override operational optimization.
- Explainability and traceability should be preserved where possible.
- Governance stability should be maintained across evolution cycles.

Return STRICT JSON ONLY.

Required JSON format:

{{
  "arbitration_results": [
    {{
      "requirement_id": "R-SEP-01",
      "dominant_objective": "Preserve escalation responsiveness during protocol transition",
      "suppressed_objective": "Reduce alert noise through higher-specificity screening",
      "governance_decision": "Prioritize patient safety over workflow optimization.",
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

        return parsed["arbitration_results"]

    except Exception:

        return [
            {
                "requirement_id": "UNKNOWN",
                "dominant_objective":
                "Unknown",

                "suppressed_objective":
                "Unknown",

                "governance_decision":
                "Arbitration parsing failure.",

                "reasoning":
                "Unable to resolve governance priorities."
            }
        ]