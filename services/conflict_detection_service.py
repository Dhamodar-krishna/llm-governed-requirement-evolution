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

IMPORTANT:

Use concise governance objectives.

Each objective should be a short phrase
containing no more than 12 words.

Avoid lengthy explanations inside
conflicting_objectives.

Place detailed reasoning only in the reasoning field.

IMPORTANT:

Identify only the single most significant governance conflict
for each requirement evolution.

If multiple conflicts exist,
select the conflict with the highest governance impact.

Do not return multiple conflicts
for the same requirement_id.

Requirement Evolutions:
{json.dumps(actions, indent=2)}

Gate 1 Results:
{json.dumps(gate1_results, indent=2)}

Gate 2 Results:
{json.dumps(gate2_results, indent=2)}

Gate 3 Results:
{json.dumps(gate3_results, indent=2)}

Identify conflicts from the actual
guideline interpretation,
requirement evolution,
and governance gate outputs.

Do NOT reuse example conflicts.

Do NOT assume:
- qSOFA transitions
- SIRS replacement
- alert fatigue scenarios
- protocol migration scenarios

unless explicitly present in the current evolution.

Conflicts must be derived solely from:
- Requirement Evolutions
- Gate 1 Results
- Gate 2 Results
- Gate 3 Results

IMPORTANT:

The conflict reasoning must remain
fully traceable to the current
requirement evolution.

If a concept is not present in:
- requirement evolution,
- governance gate outputs,

then it must not appear in the conflict analysis.

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