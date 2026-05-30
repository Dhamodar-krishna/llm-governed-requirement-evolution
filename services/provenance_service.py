import json
import os
from datetime import datetime


PROVENANCE_PATH = (
    "data/evolution_history.json"
)


def record_governance_cycle(

    guideline_update,

    stage1_output,

    stage2_output,

    stage3_output,

    gate1_results,

    gate2_results,

    gate3_results,

    conflict_results,

    arbitration_results,

    synthesis_results,

    confidence_outputs,

    repair_outputs,

    human_approval="PENDING"

):

    # =============================================
    # LOAD EXISTING HISTORY
    # =============================================

    if os.path.exists(
        PROVENANCE_PATH
    ):

        with open(
            PROVENANCE_PATH,
            "r"
        ) as f:

            try:

                history = json.load(f)

            except Exception:

                history = []

    else:

        history = []

    # =============================================
    # CREATE GOVERNANCE RECORD
    # =============================================

    cycle_record = {

        "timestamp":
        str(datetime.utcnow()),

        "guideline_update":
        guideline_update,

        "stage1":
        stage1_output,

        "stage2":
        stage2_output,

        "stage3":
        stage3_output,

        "gate1":
        gate1_results,

        "gate2":
        gate2_results,

        "gate3":
        gate3_results,

        "conflicts":
        conflict_results,

        "arbitration":
        arbitration_results,

        "synthesis":
        synthesis_results,

        "confidence":
        confidence_outputs,

        "repair_outputs":
        repair_outputs,

        "human_governance_decisions":
        human_approval
    }

    # =============================================
    # APPEND HISTORY
    # =============================================

    history.append(
        cycle_record
    )

    # =============================================
    # SAVE
    # =============================================

    with open(
        PROVENANCE_PATH,
        "w"
    ) as f:

        json.dump(
            history,
            f,
            indent=2
        )

    return cycle_record