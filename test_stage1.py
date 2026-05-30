from services.provenance_service import run_feedback_loop
from services.governance_service import run_gate1
from services.stage1_service import run_stage1
from services.stage2_service import run_stage2
from services.stage3_service import run_stage3

import json

change = """
qSOFA should replace SIRS as the primary
sepsis screening mechanism.
"""

with open("data/requirements.json", "r") as file:
    requirements = json.load(file)

# =====================================================
# STAGE 1
# =====================================================

stage1_result = run_stage1(change)

print("\n=== STAGE 1 OUTPUT ===\n")
print(stage1_result)

# =====================================================
# STAGE 2
# =====================================================

stage2_result = run_stage2(stage1_result, requirements)

print("\n=== STAGE 2 OUTPUT ===\n")
print(stage2_result)

# =====================================================
# STAGE 3
# =====================================================

stage3_result = run_stage3(
    stage1_result,
    stage2_result,
    requirements
)

print("\n=== STAGE 3 OUTPUT ===\n")
print(stage3_result)

# =====================================================
# GATE 1 — SAFETY VALIDATION
# =====================================================

print("\n=== GATE 1 OUTPUT ===\n")

for action in stage3_result["requirement_actions"]:

    gate_result = run_gate1(action)

    print(gate_result)

# =====================================================
# FEEDBACK LOOP
# =====================================================

print("\n=== FEEDBACK LOOP OUTPUT ===\n")

for action in stage3_result["requirement_actions"]:

    gate_result = run_gate1(action)

    if gate_result["gate_result"] == "FAIL":

        revised_candidate = run_feedback_loop(
            action,
            gate_result
        )

        print(revised_candidate)