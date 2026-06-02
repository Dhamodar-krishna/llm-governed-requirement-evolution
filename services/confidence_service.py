def calculate_confidence(

    synthesis_results,

    evolution_history

):

    confidence_outputs = []

    for item in synthesis_results:

        score = 1.0

        final_state = item.get(
            "final_state",
            "REVIEW"
        )

        violated_constraints = item.get(
            "violated_constraints",
            []
        )

        reasoning = item.get(
            "synthesis_reasoning",
            ""
        )

        # =============================================
        # FINAL STATE IMPACT
        # =============================================

        if final_state == "PASS":

            score -= 0.05

        elif final_state == "REVIEW":

            score -= 0.15

        elif final_state == "FAIL":

            score -= 0.60

        elif final_state == "ESCALATE":

            score -= 0.35

        # =============================================
        # CONSTRAINT IMPACT
        # =============================================

        score -= (
            len(violated_constraints)
            * 0.05
        )

        # =============================================
        # SCORE NORMALIZATION
        # =============================================

        if score < 0:

            score = 0.0

        if score > 1:

            score = 1.0

        # =============================================
        # CONFIDENCE LEVELS
        # =============================================

        if score >= 0.85:

            confidence_level = "HIGH"

            escalation = (
                "Autonomous Governance "
                "Progression Allowed"
            )

        elif score >= 0.65:

            confidence_level = "MODERATE"

            escalation = (
                "Human Governance Review "
                "Recommended"
            )

        elif score >= 0.40:

            confidence_level = "LOW"

            escalation = (
                "Mandatory Human Review "
                "Required"
            )

        else:

            confidence_level = "CRITICAL"

            escalation = (
                "Adaptive Evolution Blocked "
                "Pending Governance Escalation"
            )

        # =============================================
        # OUTPUT
        # =============================================

        confidence_outputs.append({

            "id": item["id"],

            "confidence_score":
            round(score, 2),

            "confidence_level":
            confidence_level,

            "escalation_recommendation":
            escalation,

            "confidence_reasoning":
            reasoning,

            "confidence_breakdown": {

                "final_state_impact":
                final_state,

                "violated_constraints":
                len(violated_constraints),

                "governance_history_available":
                len(evolution_history) > 0
            }
        })

    return confidence_outputs