def retrieve_governance_patterns(
    evolution_history
):

    patterns = []

    for cycle in evolution_history:

        synthesis = cycle.get(
            "synthesis",
            []
        )

        for result in synthesis:

            if result["final_state"] in [
                "FAIL",
                "REVIEW"
            ]:

                patterns.append({

                    "requirement_id":
                    result["id"],

                    "governance_state":
                    result["final_state"],

                    "reasoning":
                    result.get(
                        "synthesis_reasoning",
                        ""
                    )
                })

    return patterns[-5:]