import json

from services.llm_service import call_llm


def run_feedback_repair(
    failed_requirements
):

    repair_outputs = []

    for item in failed_requirements:

        prompt = f"""
You are a Governance Repair Engineer.

Requirement ID:
{item.get('id')}

Requirement Text:
{item.get('requirement_text', '')}

Violated Constraints:
{json.dumps(item.get('violated_constraints', []), indent=2)}

Governance Reasoning:
{item.get('synthesis_reasoning', '')}

Task:

Generate a revised requirement that:

- resolves all violated constraints
- preserves safety intent
- preserves traceability
- remains operationally feasible
- is auditable and computable

Return STRICT JSON ONLY.

{{
  "repair_candidate": "...",
  "repair_reasoning": "..."
}}
"""

        response = call_llm(prompt)

        try:

            cleaned = response.strip()

            if cleaned.startswith("```json"):
                cleaned = cleaned.replace("```json", "")
                cleaned = cleaned.replace("```", "")

            parsed = json.loads(cleaned)

            repair_outputs.append({

                "id":
                item["id"],

                "repair_candidate":
                parsed["repair_candidate"],

                "repair_reasoning":
                parsed["repair_reasoning"]
            })

        except Exception:

            repair_outputs.append({

                "id":
                item["id"],

                "repair_candidate":
                "Repair generation failed.",

                "repair_reasoning":
                "LLM parsing failure."
            })

    return repair_outputs