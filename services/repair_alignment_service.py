import json

from services.llm_service import call_llm


def assess_repair_alignment(

    guideline_update,

    repair_candidate

):

    prompt = f"""
You are a Governance Alignment Reviewer.

Original Guideline:

{guideline_update}

Repair Candidate:

{repair_candidate}

Task:

Determine whether the repair candidate still preserves
the operational intent of the guideline.

Possible outcomes:

PASS
- intent preserved

REVIEW
- intent partially preserved

ESCALATE
- repair significantly changes or reverses intent

Return STRICT JSON:

{{
  "alignment_state":"PASS|REVIEW|ESCALATE",
  "alignment_reasoning":"..."
}}
"""

    response = call_llm(prompt)

    try:

        cleaned = response.strip()

        if cleaned.startswith("```json"):
            cleaned = cleaned.replace(
                "```json",
                ""
            ).replace(
                "```",
                ""
            )

        return json.loads(cleaned)

    except:

        return {

            "alignment_state":
            "REVIEW",

            "alignment_reasoning":
            "Alignment assessment failed."
        }