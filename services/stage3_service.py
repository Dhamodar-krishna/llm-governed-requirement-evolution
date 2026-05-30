import json
import re

from services.llm_service import call_llm

from services.governance_memory_service import (
    retrieve_governance_patterns
)


def run_stage3(
    stage1_output,
    stage2_output,
    requirements,
    evolution_history
):

    # =================================================
    # GOVERNANCE MEMORY RETRIEVAL
    # =================================================

    governance_patterns = (
        retrieve_governance_patterns(
            evolution_history
        )
    )

    historical_context = ""

    for pattern in governance_patterns:

        historical_context += f"""

Historical Governance Pattern

Requirement:
{pattern['requirement_id']}

Governance State:
{pattern['governance_state']}

Governance Reasoning:
{pattern['reasoning']}
"""

    # =================================================
    # PROMPT
    # =================================================

    prompt = f"""
You are performing requirement evolution analysis.

Your task is to generate the requirement changes implied by the guideline update.

Governance validation, safety assessment, and repair are performed in later layers.

STAGE 1 OUTPUT:
{json.dumps(stage1_output, indent=2)}

STAGE 2 OUTPUT:
{json.dumps(stage2_output, indent=2)}

CURRENT REQUIREMENTS:
{json.dumps(requirements, indent=2)}

RETRIEVED GOVERNANCE MEMORY:
{historical_context}

Use governance memory only for contextual awareness.

IMPORTANT:

- Generate the requirement evolution implied by the guideline.
- Do NOT repair unsafe evolution.
- Do NOT introduce governance corrections.
- Do NOT add safety mitigations unless explicitly stated in the guideline.
- Do NOT preserve safety invariants automatically.
- Do NOT perform governance validation.
- Governance assessment occurs in later layers.

For each affected requirement:
- decide whether to modify,
- review,
- retain,
- or deprecate.

IMPORTANT:
- ONLY evolve requirements present in
  affected_requirements.
- If no requirements are affected,
  return an empty requirement_actions list.
- Do NOT invent propagation.

Return STRICT JSON ONLY.

Required JSON format:

{{
  "requirement_actions": [
    {{
      "id": "R-SEP-01",
      "recommended_action": "modify",
      "modified_text": "Updated requirement",
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

        parsed = json.loads(json_text)

        valid_ids = [
            req["id"]
            for req in requirements
        ]

        validated_actions = []

        hallucinated_ids = []

        for item in parsed.get(
            "requirement_actions",
            []
        ):

            if item["id"] in valid_ids:

                validated_actions.append(
                    item
                )

            else:

                hallucinated_ids.append(
                    item["id"]
                )

        return {

            "requirement_actions":
            validated_actions,

            "hallucinated_ids":
            hallucinated_ids,

            "hallucination_count":
            len(hallucinated_ids)

        }

    except Exception:

        return {

            "error":
            "Invalid JSON response",

            "raw_response":
            response
        }