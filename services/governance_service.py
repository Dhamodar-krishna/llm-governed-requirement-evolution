import json
import re

from services.llm_service import call_llm


def run_gate1(requirement_actions):

    prompt = f"""
You are performing SAFETY INVARIANT validation
for adaptive requirement evolution
in a healthcare ICU Cyber-Physical-Social System.

Evaluate ALL evolved requirements together.

Requirement Evolutions:
{json.dumps(requirement_actions, indent=2)}

Possible governance states:
- PASS
- REVIEW
- FAIL

Governance Principles:

- PASS if safety invariants remain preserved, even with moderate concerns.
- REVIEW if heavy governance uncertainty exists.
- FAIL only for direct safety-critical degradation.

- Operational adaptation is expected.
- Moderate tradeoffs are acceptable.
- Governance should support safe evolution.

Return STRICT JSON ONLY.

Required JSON format:

{{
  "results": [
    {{
      "id": "R-SEP-01",
      "gate_result": "PASS",
      "reason": "Explanation"
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
                "gate_result": "REVIEW",
                "reason":
                "Governance parsing failure."
            }
        ]