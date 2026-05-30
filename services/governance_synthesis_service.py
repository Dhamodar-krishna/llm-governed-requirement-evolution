import json
import re

from services.llm_service import call_llm


def run_governance_synthesis(

    actions,
    gate1_results,
    gate2_results,
    gate3_results

):

    prompt = f"""
You are performing SYSTEM-LEVEL GOVERNANCE SYNTHESIS
for adaptive requirement evolution
in a healthcare ICU Cyber-Physical-Social System.

Requirement Evolutions:
{json.dumps(actions, indent=2)}

Gate 1 Results:
{json.dumps(gate1_results, indent=2)}

Gate 2 Results:
{json.dumps(gate2_results, indent=2)}

Gate 3 Results:
{json.dumps(gate3_results, indent=2)}

Possible final states:
- PASS
- REVIEW
- ESCALATE
- FAIL

Governance Rules:

- PASS if all governance gates pass.

- REVIEW only when at least one governance gate returns REVIEW.

Governance observations,
documentation gaps,
future validation activities,
deployment readiness concerns,
or implementation recommendations
must NOT independently downgrade
a requirement from PASS to REVIEW
if all governance gates returned PASS.

FAIL only when governance evidence indicates
unacceptable safety degradation,
escalation suppression,
or two or more governance gate failures.

Traceability concerns,
validation uncertainty,
workflow ambiguity,
or operational trade-offs
should normally result in REVIEW or ESCALATE,
not FAIL.

- ESCALATE only when governance cannot confidently determine
  whether the requirement should PASS, REVIEW, or FAIL.

IMPORTANT:

- Known unsafe requirements MUST be FAIL.
- Multiple gate failures MUST be FAIL.
- ESCALATE is for unresolved governance ambiguity,
  not known unsafe evolution.

Decision Matrix:

IMPORTANT:

If Gate1 = PASS
and Gate2 = PASS
and Gate3 = PASS

the requirement MUST be PASS.

The synthesis stage may add governance notes,
but may not downgrade the requirement
without governance gate evidence.

A requirement must not be classified as FAIL
based solely on inferred risks,
recommended future validation,
documentation concerns,
deployment readiness concerns,
or missing operational evidence.

FAIL requires explicit governance gate evidence
or explicit safety violations.

Gate1 PASS
Gate2 PASS
Gate3 PASS
    → PASS

One gate REVIEW
    → REVIEW

Two or more REVIEW outcomes
    → REVIEW

Mixed PASS/FAIL outcomes
    → ESCALATE

One FAIL + remaining PASS
    → ESCALATE

Two or more FAIL outcomes
    → FAIL

Three FAIL outcomes
    → FAIL

Return STRICT JSON ONLY.

Required JSON format:

{{
  "results": [
    {{
      "id": "R-SEP-01",
      "final_state": "PASS",
      "requirement_text": "..."
      "violated_constraints": [],
      "synthesis_reasoning": "Explanation"
    }}
  ]
}}
"""

    response = call_llm(prompt)

    try:

        cleaned = response.strip()

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

        return parsed["results"]

    except Exception:

        return [
            {
                "id": "UNKNOWN",
                "final_state": "ESCALATE",
                "violated_constraints": [
                    "Synthesis parsing failure"
                ],
                "synthesis_reasoning":
                "Governance synthesis failed."
            }
        ]