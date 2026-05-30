import streamlit as st
import json

from services.governance_synthesis_service import run_governance_synthesis
from services.stage1_service import run_stage1
from services.stage2_service import run_stage2
from services.stage3_service import run_stage3
from services.governance_service import run_gate1
from services.goal_alignment_service import run_gate2
from services.traceability_service import run_gate3
from services.provenance_service import (
    record_governance_cycle
)
from services.conflict_detection_service import (
    detect_governance_conflicts
)
from services.governance_arbitration_service import (
    run_governance_arbitration
)
from services.confidence_service import (
    calculate_confidence
)
from services.feedback_repair_service import (
    run_feedback_repair
)
from services.repair_alignment_service import (
    assess_repair_alignment
)
import networkx as nx
import matplotlib.pyplot as plt

with open("data/requirements.json") as f:
    requirements = json.load(f)

# =================================================
# GOVERNANCE LAYER HEADER
# =================================================

def layer_header(

    title,

    color="#1f4e79"

):

    st.markdown(

        f'''
        <div style="
            background-color:{color};
            padding:5px;
            border-radius:5px;
            margin-top:10px;
            margin-bottom:10px;
        ">

        <h2 style="
            color:#111827;
            text-align:center;
            margin:0;
        ">
        {title}
        </h2>

        </div>
        ''',

        unsafe_allow_html=True
    )

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Governed CPSS Evolvability Platform",
    layout="wide"
)

# =====================================================
# TITLE
# =====================================================

st.title(
    "Governed Adaptive Requirement Evolvability Framework"
)

st.subheader(
    "A Governance-Oriented Architecture for Safety-Critical CPSS"
)

# =================================================
# LOAD EVOLUTION HISTORY
# =================================================

history_file = "data/evolution_history.json"

try:

    with open(history_file, "r") as f:

        persistent_history = json.load(f)

except:

    persistent_history = []

# =================================================
# EVOLUTION MEMORY STORE
# =================================================

if "evolution_history" not in st.session_state:

    st.session_state.evolution_history = persistent_history

st.markdown("""

This prototype demonstrates a governed adaptive framework
for evolving requirements in safety-critical
Cyber-Physical-Social Systems (CPSS).

The framework combines:
- LLM-assisted requirement interpretation,
- adaptive requirement evolution,
- multi-layer governance validation,
- conflict detection and arbitration,
- uncertainty-aware confidence estimation,
- human-centered oversight,
- provenance and evolution continuity.

The architecture is designed to support:
- runtime requirement adaptation,
- governance-constrained evolvability,
- explainable adaptive reasoning,
- policy-aware operational tradeoffs,
- safe and accountable evolution.

---

### Key Governance Objectives

- Patient Safety
- Escalation Responsiveness
- Operational Stability
- Traceability Integrity
- Workflow Efficiency
- Governance Stability

---

### Research Contribution

This prototype demonstrates how institutional governance
principles can constrain and guide adaptive requirement evolution
using LLM-assisted reasoning in safety-critical environments.

""")

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title(
        "CPSS Evolvability Framework"
    )

    st.markdown("""
# Governed Adaptive Requirement Evolvability

A governance-oriented framework for
adaptive requirement evolution
in safety-critical Cyber-Physical-Social Systems (CPSS).

---

# INPUT LAYER
- Clinical Guideline Update
- Operational Change
- Environmental Trigger

---

# INTERPRETATION LAYER
- Stage 1 — Guideline Interpretation
- Stage 2 — Requirement Impact Analysis

---

# ADAPTIVE EVOLUTION LAYER
- Stage 3 — Requirement Evolution
- Historical Governance Memory
- Governance Pattern Retrieval

---

# GOVERNANCE ORCHESTRATION
- Gate 1 — Safety Validation
- Gate 2 — Goal Alignment
- Gate 3 — Traceability Integrity
- Conflict Detection
- Governance Arbitration
- Governance Synthesis
- Confidence Assessment

---

# ADAPTIVE OVERSIGHT
- Feedback Repair Loop
- Human Governance Approval
- Provenance Tracking
- Evolution Memory

---

# Research Focus
Governed adaptive evolution
for safety-critical CPSS environments.
""")

layer_header(

    "LAYER 1 — INPUT LAYER",

    "#d1d5db"
)

# =====================================================
# INPUT
# =====================================================

st.header("Guideline Update Input")

guideline_update = st.text_area(
    "Enter a guideline update",
    height=150,
    value="""
qSOFA should replace SIRS
as the primary sepsis screening mechanism.
"""
)

run_button = st.button("Run Evolvability Pipeline")

# =====================================================
# PIPELINE
# =====================================================

if run_button:

    st.divider()

    layer_header(

        "LAYER 2 — INTERPRETATION LAYER",

        "#bfdbfe"
    )

    # =================================================
    # STAGE 1
    # =================================================

    st.header("Stage 1 — Guideline Interpretation")

    with st.expander("What is Stage 1 doing?"):

        st.markdown("""
### Purpose
Stage 1 interprets evolving operational or clinical guidance.

### Why it matters
Cyber-Physical-Social Systems continuously evolve due to:
- guideline updates,
- regulatory changes,
- operational pressures,
- and stakeholder adaptation.

Traditional requirements engineering assumes static requirements.
This framework instead treats requirements as evolving runtime entities.

### What happens here
The LLM:
- interprets the guideline change,
- extracts operational implications,
- identifies affected system domains,
- and produces structured machine-readable reasoning.

### Research significance
This stage demonstrates runtime requirement interpretation
for adaptive CPSS environments.
""")

    with st.spinner("Running Stage 1..."):

        stage1_output = run_stage1(guideline_update)

    st.success("Stage 1 Complete")

    st.subheader("Change Type")

    st.info(

        stage1_output.get(
            "change_type",
            "Unknown"
        )
    )

    st.subheader(
        "Operational Implications"
    )

    for item in stage1_output.get(
        "operational_implications",
        []
    ):

        st.markdown(
            f"- {item}"
        )

    st.subheader(
        "Affected System Areas"
    )

    for item in stage1_output.get(
        "affected_system_areas",
        []
    ):

        st.markdown(
            f"- {item}"
        )

    # =================================================
    # STAGE 2
    # =================================================

    st.divider()

    st.header("Stage 2 — Requirement Impact Analysis")

    with st.expander("What is Stage 2 doing?"):

        st.markdown("""
### Purpose
Stage 2 identifies which requirements are affected
by the evolving operational context.

### What happens here
The framework:
- compares operational implications,
- maps impacts onto existing requirements,
- distinguishes direct vs indirect impacts,
- validates requirement identity integrity.

### Governance feature
Hallucinated requirement identifiers are rejected
through repository validation.

### Research significance
This stage demonstrates governed requirement impact reasoning
under evolving operational conditions.
""")

    with st.spinner("Running Stage 2..."):

        stage2_output = run_stage2(
            guideline_update,
            stage1_output
        )

    st.success("Stage 2 Complete")

    affected = stage2_output.get(
        "affected_requirements",
        []
    )

    if len(affected) == 0:

        st.warning(
            "No governance-relevant "
            "requirements affected."
        )

    else:

        for req in affected:

            requirement_labels = {

                "R-SEP-01":
                """
                The ICU system shall trigger
                sepsis alerts using SIRS criteria.
                """,

                "R-SEP-02":
                """
                The ICU system shall reassess
                sepsis risk every 15 minutes.
                """,

                "R-ALT-07":
                """
                Duplicate sepsis alerts within
                5 minutes shall be suppressed.
                """
            }

            label = requirement_labels.get(

                req["id"],

                "Unknown Requirement"
            )

            st.subheader(
                req["id"]
            )

            st.markdown(
                f"""
                <div style="
                    background-color:#ffffff;
                    padding:12px;
                    border-radius:10px;
                    border:1px solid #d1d5db;
                    margin-bottom:15px;
                ">
                <b>Current Requirement:</b><br><br>
                {label}
                </div>
                """,

                unsafe_allow_html=True
            )

            impact_type = req[
                "impact_type"
            ].upper()

            if impact_type == "DIRECT":

                st.error(
                    f"DIRECT IMPACT"
                )

            else:

                st.info(
                    f"INDIRECT IMPACT"
                )

            st.write(
                "Reasoning:"
            )

            st.write(
                req["reasoning"]
            )

            st.divider()

    if stage2_output.get(
        "hallucination_count",
        0
    ) > 0:

        st.error(

            f"Hallucinated IDs Detected: "
            f"{stage2_output['hallucinated_ids']}"
        )

    affected_requirements = stage2_output.get(
        "affected_requirements",
        []
    )

    if len(affected_requirements) == 0:

        st.warning(
            "No governance-relevant requirements "
            "were affected by this guideline update."
        )

        st.info(
            "Pipeline propagation terminated."
        )

        st.stop()

    layer_header(

        "LAYER 3 — ADAPTIVE EVOLUTION LAYER",

        "#e9d5ff"
    )

    # =================================================
    # STAGE 3
    # =================================================

    st.divider()

    st.header("Stage 3 — Requirement Evolution")

    with st.expander("What is Stage 3 doing?"):

        st.markdown("""
### Purpose
Stage 3 proposes adaptive requirement evolution.

### What happens here
The LLM:
- determines whether requirements should evolve,
- proposes modified requirement specifications,
- and optimizes operational workflows.

### Important research issue
Operational optimization may unintentionally:
- reduce safety margins,
- delay escalation,
- weaken detection sensitivity.

This creates the need for governance validation.

### Research significance
This stage demonstrates adaptive requirement evolution
under competing operational objectives.
""")

    with st.spinner("Running Stage 3..."):

        stage3_output = run_stage3(

            stage1_output,

            stage2_output,

            requirements,

            st.session_state.evolution_history

        )

    st.success("Stage 3 Complete")

    actions = stage3_output.get(
        "requirement_actions",
        []
    )

    for action in actions:

        st.subheader(action["id"])

        recommended_action = action[
            "recommended_action"
        ].upper()

        # =============================================
        # GOVERNANCE ACTION HIGHLIGHT
        # =============================================

        if recommended_action == "MODIFY":

            st.markdown(
                """
                <div style="
                    background-color:#dcfce7;
                    color:#166534;
                    padding:14px;
                    border-radius:10px;
                    font-weight:bold;
                    margin-bottom:15px;
                    text-align:center;
                    font-size:18px;
                ">
                MODIFY REQUIREMENT
                </div>
                """,

                unsafe_allow_html=True
            )

        elif recommended_action == "REVIEW":

            st.markdown(
                """
                <div style="
                    background-color:#fef3c7;
                    color:#92400e;
                    padding:14px;
                    border-radius:10px;
                    font-weight:bold;
                    margin-bottom:15px;
                    text-align:center;
                    font-size:18px;
                ">
                REQUIRES GOVERNANCE REVIEW
                </div>
                """,

                unsafe_allow_html=True
            )

        elif recommended_action == "RETAIN":

            st.markdown(
                """
                <div style="
                    background-color:#dbeafe;
                    color:#1d4ed8;
                    padding:14px;
                    border-radius:10px;
                    font-weight:bold;
                    margin-bottom:15px;
                    text-align:center;
                    font-size:18px;
                ">
                RETAIN CURRENT REQUIREMENT
                </div>
                """,

                unsafe_allow_html=True
            )

        elif recommended_action == "DEPRECATE":

            st.markdown(
                """
                <div style="
                    background-color:#fee2e2;
                    color:#991b1b;
                    padding:14px;
                    border-radius:10px;
                    font-weight:bold;
                    margin-bottom:15px;
                    text-align:center;
                    font-size:18px;
                ">
                DEPRECATE REQUIREMENT
                </div>
                """,

                unsafe_allow_html=True
            )

        else:

            st.warning(
                recommended_action
            )

        # =========================================
        # MODIFY
        # =========================================

        if action["recommended_action"] == "modify":

            st.success(
                action["modified_text"]
            )

        # =========================================
        # REVIEW
        # =========================================

        elif action["recommended_action"] == "review":

            st.warning(
                "Pending governance review."
            )

        # =========================================
        # RETAIN
        # =========================================

        elif action["recommended_action"] == "retain":

            st.info(
                "Original requirement retained."
            )

        # =========================================
        # REASONING
        # =========================================

        st.write(
            "Reasoning:"
        )

        st.write(
            action["reasoning"]
        )

        st.divider() 

    layer_header(

        "LAYER 4 — GOVERNANCE ORCHESTRATION LAYER",

        "#fde68a"
    )
        
    # =================================================
    # GATE 1
    # =================================================

    st.divider()

    st.header("Gate 1 — Safety Invariant Validation")

    with st.expander("Why is governance required?"):

        st.markdown("""
### Purpose
Governance gates constrain unsafe requirement evolution.

### Gate 1 checks
Whether requirement modifications:
- reduce detection sensitivity,
- delay escalation,
- suppress critical alerts,
- weaken patient safety.

### Key research insight
LLMs may generate operationally efficient solutions
that unintentionally violate safety invariants.

### Research significance
This demonstrates governed AI-assisted requirement evolution
for safety-critical CPSS environments.
""")

    actions = stage3_output.get(
        "requirement_actions",
        []
    )

    with st.spinner(
        "Running Gate 1 — Safety Validation..."
    ):

        gate_results = run_gate1(
            actions
        )

    for result in gate_results:

        if result["gate_result"] == "PASS":

            st.success(
                f"{result['id']} → PASS"
            )

            st.write(result["reason"])

        elif result["gate_result"] == "REVIEW":

            st.warning(
                f"{result['id']} → REVIEW"
            )

            st.write(result["reason"])

        else:

            st.error(
                f"{result['id']} → FAIL"
            )

            st.write(result["reason"])
    # =================================================
    # GATE 2
    # =================================================

    st.divider()

    st.header("Gate 2 — Goal Alignment Validation")

    with st.expander("Why is goal alignment important?"):

        st.markdown("""
    ### Purpose
    Gate 2 validates whether evolved requirements
    remain aligned with operational ICU goals.

    ### What this gate checks
    The framework evaluates whether requirement evolution:
    - preserves rapid escalation,
    - reduces clinician alert fatigue,
    - maintains workflow efficiency,
    - supports safe operational behaviour.

    ### Why this matters
    Operational optimisation alone is insufficient.

    Requirement evolution must also preserve
    high-level system objectives.

    ### Research significance
    This demonstrates goal-aware adaptive evolution
    for safety-critical CPSS environments.
    """)

    with st.spinner(
        "Running Gate 2 — Goal Alignment..."
    ):

        gate2_results = run_gate2(
            actions
        )

    for result in gate2_results:

        if result["gate_result"] == "PASS":

            st.success(
                f"{result['id']} → PASS"
            )

        elif result["gate_result"] == "REVIEW":

            st.warning(
                f"{result['id']} → REVIEW"
            )

        else:

            st.error(
                f"{result['id']} → FAIL"
            )

        st.write(result["reason"])

        st.caption(
            f"Affected Goal: {result['affected_goal']}"
        )
    # =================================================
    # GATE 3
    # =================================================

    st.divider()

    st.header("Gate 3 — Traceability Integrity Validation")

    with st.expander("Why is traceability integrity important?"):

        st.markdown("""
    ### Purpose

    Gate 3 validates whether requirement evolution
    preserves explainability and lifecycle traceability.

    ### What this gate checks

    The framework evaluates whether:
    - requirement rationale remains understandable,
    - semantic meaning is preserved,
    - provenance continuity exists,
    - governance lineage remains explainable.

    ### Why this matters

    Adaptive evolution without traceability
    creates governance opacity.

    Safety-critical CPSS environments require:
    - explainability,
    - auditability,
    - semantic continuity,
    - governance accountability.

    ### Research significance

    This demonstrates governed traceability-aware
    adaptive requirement evolution.
    """)

    with st.spinner(
        "Running Gate 3 — Traceability Integrity..."
    ):

        gate3_results = run_gate3(
            actions
        )

    for result in gate3_results:

        if result["gate_result"] == "PASS":

            st.success(
                f"{result['id']} → PASS"
            )

        elif result["gate_result"] == "REVIEW":

            st.warning(
                f"{result['id']} → REVIEW"
            )

        else:

            st.error(
                f"{result['id']} → FAIL"
            )

        st.write(result["reason"])

        st.caption(
            f"Traceability Risk: {result['traceability_risk']}"
        )
    # =================================================
    # GOVERNANCE CONFLICT DETECTION
    # =================================================

    st.divider()

    st.header(
        "Governance Conflict Detection"
    )

    with st.expander(
        "Why is conflict detection important?"
    ):

        st.markdown("""

    ### Purpose

    Adaptive evolution often creates
    competing governance objectives.

    ### What this layer detects

    The framework identifies:
    - operational tradeoffs,
    - conflicting governance goals,
    - incompatible adaptive decisions,
    - competing safety constraints.

    ### Why this matters

    CPSS environments continuously balance:
    - safety,
    - efficiency,
    - explainability,
    - workflow optimisation,
    - operational continuity.

    These goals may conflict.

    ### Research significance

    This demonstrates:
    - explainable governance negotiation,
    - adaptive tradeoff reasoning,
    - multi-objective governance orchestration.

    """)
        
    with st.spinner(
        "Running Conflict Detection..."
    ):

        conflict_results = detect_governance_conflicts(

            actions,

            gate_results,

            gate2_results,

            gate3_results
        )

    for item in conflict_results:

        st.warning(

            f"{item['requirement_id']} "
            f"→ {item['conflict_type']}"
        )

        st.write(
            "### Conflicting Objectives"
        )

        st.write(
            item["conflicting_objectives"]
        )

        st.write(
            "### Severity"
        )

        st.write(
            item["severity"]
        )

        st.write(
            "### Governance Reasoning"
        )

        st.write(
            item["reasoning"]
        )
        st.divider()
    # =================================================
    # GOVERNANCE ARBITRATION
    # =================================================


    st.header(
        "Governance Arbitration Layer"
    )

    with st.expander(
        "Why is governance arbitration important?"
    ):

        st.markdown("""

    ### Purpose

    Adaptive governance often involves
    competing operational objectives.

    The framework must determine:
    - which governance priorities dominate,
    - which objectives are suppressed,
    - how adaptive tradeoffs are resolved.

    ### Why this matters

    Safety-critical CPSS environments require:
    - explicit governance hierarchy,
    - explainable prioritisation,
    - policy-aware adaptive reasoning.

    ### Research significance

    This demonstrates:
    - governance negotiation,
    - policy-driven adaptation,
    - adaptive objective prioritisation,
    - explainable governance arbitration.

    """)

    with st.spinner(
        "Running Governance Arbitration..."
    ):

        arbitration_results = run_governance_arbitration(

            conflict_results
        )

    for item in arbitration_results:

        st.info(

            f"{item['requirement_id']} "
            f"→ Governance Arbitration"
        )

        st.write(
            "### Dominant Objective"
        )

        st.success(
            item["dominant_objective"]
        )

        st.write(
            "### Suppressed Objective"
        )

        st.warning(
            item["suppressed_objective"]
        )

        st.write(
            "### Governance Decision"
        )

        st.write(
            item["governance_decision"]
        )

        st.write(
            "### Arbitration Reasoning"
        )

        st.write(
            item["reasoning"]
        )
        st.divider()

    # =================================================
    # GOVERNANCE SYNTHESIS
    # =================================================


    st.header("Governance Synthesis Layer")

    with st.expander("What is governance synthesis doing?"):

        st.markdown("""
    ### Purpose

    The governance synthesis layer merges
    multiple governance evaluations into
    a unified adaptive governance decision.

    ### Why this matters

    Real-world CPSS environments involve:
    - conflicting operational goals,
    - safety constraints,
    - workflow tradeoffs,
    - adaptive uncertainty.

    This layer performs:
    - governance conflict resolution,
    - violated constraint extraction,
    - repair requirement determination.

    ### Research significance

    This demonstrates:
    - recursive governance reasoning,
    - adaptive evolvability control,
    - explainable governance synthesis.
    """)

    with st.spinner(
        "Running Governance Synthesis..."
    ):

        synthesis_results = run_governance_synthesis(

            gate_results,

            gate2_results,

            gate3_results,

            arbitration_results
        )

    for result in synthesis_results:

        state = result["final_state"]

        if state == "PASS":

            st.success(f"{result['id']} → PASS")

        elif state == "FAIL":

            st.error(f"{result['id']} → FAIL")

        elif state == "REVIEW":

            st.warning(f"{result['id']} → REVIEW")

        else:

            st.info(f"{result['id']} → ESCALATE")

        st.write("### Violated Constraints")

        st.write(result["violated_constraints"])

        st.write("### Governance Reasoning")

        st.write(result["synthesis_reasoning"])

        st.divider()

    # =================================================
    # GOVERNANCE CONFIDENCE
    # =================================================


    st.header(
        "Governance Confidence Assessment"
    )

    with st.expander(
        "Why is governance confidence important?"
    ):

        st.markdown("""

    ### Purpose

    Governance confidence estimates
    how safely adaptive evolution
    can proceed within the CPSS.

    ### Confidence Signals

    Confidence is derived from:

    - governance agreement,
    - conflict severity,
    - repair requirements,
    - propagation stability,
    - traceability preservation,
    - governance continuity.

    ### Governance Meaning

    Higher confidence indicates:
    - stronger governance stability,
    - lower operational uncertainty,
    - safer adaptive progression.

    Lower confidence requires:
    - stronger human oversight,
    - governance escalation,
    - adaptive constraint review.

    ### Research Significance

    This demonstrates:

    - uncertainty-aware governance,
    - confidence-based escalation,
    - adaptive governance authority modeling,
    - explainable institutional oversight.

    """)

    # =================================================
    # DETERMINISTIC CONFIDENCE
    # =================================================

    confidence_outputs = calculate_confidence(

        synthesis_results,

        [],

        []
    )

    # =================================================
    # DISPLAY RESULTS
    # =================================================

    for item in confidence_outputs:

        confidence_score = item[
            "confidence_score"
        ]

        confidence_level = item[
            "confidence_level"
        ]

        escalation = item[
            "escalation_recommendation"
        ]

        reasoning = item[
            "confidence_reasoning"
        ]

        # =============================================
        # CONFIDENCE STATUS
        # =============================================

        if confidence_level == "HIGH":

            st.success(

                f"{item['id']} "
                f"→ HIGH CONFIDENCE"
            )

        elif confidence_level == "MODERATE":

            st.warning(

                f"{item['id']} "
                f"→ MODERATE CONFIDENCE"
            )

        elif confidence_level == "LOW":

            st.error(

                f"{item['id']} "
                f"→ LOW CONFIDENCE"
            )

        else:

            st.error(

                f"{item['id']} "
                f"→ CRITICAL CONFIDENCE"
            )

        # =============================================
        # SCORE
        # =============================================

        st.subheader(
            "Confidence Score"
        )

        st.code(
            str(confidence_score)
        )

        # =============================================
        # ESCALATION
        # =============================================

        st.subheader(
            "Escalation Recommendation"
        )

        st.info(
            escalation
        )

        # =============================================
        # REASONING
        # =============================================

        st.subheader(
            "Confidence Breakdown"
        )

        st.json(
            item[
                "confidence_breakdown"
            ]
        )
        st.subheader(
            "Confidence Reasoning"
        )

        st.write(
            reasoning
        )

        st.divider()
    
    layer_header(

    "LAYER 5 — ADAPTIVE OVERSIGHT LAYER",

    "#bbf7d0"
    )
    # =================================================
    # FEEDBACK LOOP
    # =================================================

    st.divider()

    st.header("Adaptive Feedback Repair Loop")

    with st.expander("What is the feedback loop doing?"):

        st.markdown("""
    ### Purpose
    The feedback loop enables governed corrective evolution.

    ### What happens here
    Unsafe requirement modifications:
    - generate governance constraints,
    - trigger adaptive repair reasoning,
    - produce safer revised evolutions.

    ### Important concept
    The framework does not simply reject unsafe evolution.
    It attempts to guide safer adaptive evolution.

    ### Research significance
    This demonstrates governed iterative reasoning
    for adaptive CPSS environments.
    """)

    failed_results = [

        r for r in synthesis_results

        if r["final_state"] == "FAIL"
    ]

    repair_outputs = []

    if failed_results:

        with st.spinner(
            "Generating Governance Repairs..."
        ):

            repair_outputs = run_feedback_repair(
                failed_results
            )
    repair_alignment_results = []

    if repair_outputs:

        for item in repair_outputs:

            st.error(
                f"{item['id']} → GOVERNANCE FAILURE DETECTED"
            )

            st.success(
                "Repair Candidate Generated"
            )

            st.write("### Governance Trace")

            st.markdown(f"""
    - Stage 3 evolution triggered governance concern
    - Governance synthesis identified violated constraints
    - Feedback repair generated safer adaptive evolution
    - Requirement returned for human governance review
    """)

            st.write("### Revised Requirement")

            st.info(
                item["repair_candidate"]
            )

            st.write("### Repair Reasoning")

            st.write(
                item["repair_reasoning"]
            )
            alignment = assess_repair_alignment(

                guideline_update,

                item["repair_candidate"]

            )
            repair_alignment_results.append({

                "id": item["id"],

                "alignment_state":
                alignment["alignment_state"],

                "alignment_reasoning":
                alignment["alignment_reasoning"]

            })

            st.write(
                "### Repair Alignment Assessment"
            )

            if alignment["alignment_state"] == "PASS":

                st.success(
                    "Repair Alignment: PASS"
                )

            elif alignment["alignment_state"] == "REVIEW":

                st.warning(
                    "Repair Alignment: REVIEW"
                )

            else:

                st.error(
                    "Repair Alignment: ESCALATE"
                )

            st.write(
                alignment["alignment_reasoning"]
            )
            
            st.divider()

    else:

        final_states = [

            item["final_state"]

            for item in synthesis_results
        ]

        if "ESCALATE" in final_states:

            st.warning(
                "No adaptive repair generated. "
                "Governance escalation requires "
                "human authority review."
            )

        else:

            st.success(
                "No governance failures detected. "
                "Adaptive repair was not required."
            )

    st.divider()

    # =================================================
    # HUMAN GOVERNANCE
    # =================================================

    st.divider()

    st.header("Human Governance Approval")

    human_decisions = {}

    with st.expander("Why is human oversight important?"):

        st.markdown("""
    ### Purpose
    Final authority remains with human experts.

    ### Why this matters
    The framework is designed as:
    - decision support,
    NOT:
    - autonomous clinical governance.

    ### Human responsibilities
    Human reviewers:
    - validate proposed evolution,
    - assess contextual safety,
    - authorize lifecycle transition.

    ### Research significance
    This preserves accountability and governance integrity
    within adaptive CPSS environments.
    """)

    for synthesis_item in synthesis_results:

        req_id = synthesis_item["id"]

        synthesis_state = synthesis_item["final_state"]

        # =============================================
        # DETERMINE FINAL REQUIREMENT STATUS
        # =============================================

        final_status = synthesis_state

        if synthesis_state == "FAIL":

            repair_match = next(

                (
                    r

                    for r in repair_alignment_results

                    if r["id"] == req_id
                ),

                None
            )

            if repair_match:

                alignment_state = repair_match[
                    "alignment_state"
                ]

                # =====================================
                # REPAIR-AWARE GOVERNANCE RESOLUTION
                # =====================================

                if alignment_state == "PASS":

                    final_status = "PASS"

                elif alignment_state == "REVIEW":

                    final_status = "REVIEW"

                elif alignment_state == "ESCALATE":

                    final_status = "ESCALATE"

                else:

                    final_status = "FAIL"

        st.divider()

        st.subheader(req_id)

        # =============================================
        # STATUS DISPLAY
        # =============================================

        if final_status == "PASS":

            st.success(
                "Governance Status: PASS"
            )

        elif final_status == "REVIEW":

            st.warning(
                "Governance Status: REVIEW"
            )

        elif final_status == "ESCALATE":

            st.warning(
                "Governance Status: ESCALATE"
            )

        else:

            st.error(
                "Governance Status: FAIL"
            )

        # =============================================
        # HUMAN DECISION OPTIONS
        # =============================================

        if final_status in [

            "PASS",

            "REVIEW"

        ]:

            decision = st.radio(

                f"Decision for {req_id}",

                [

                    "Approve Evolution",

                    "Reject Evolution"

                ],

                key=f"decision_{req_id}"
            )

        elif final_status == "ESCALATE":

            decision = st.radio(

                f"Decision for {req_id}",

                [

                    "Escalate for Clinical Review",

                    "Reject Evolution"

                ],

                key=f"decision_{req_id}"
            )

        else:

            decision = st.radio(

                f"Decision for {req_id}",

                [

                    "Request Governance Override",

                    "Reject Evolution"

                ],

                key=f"decision_{req_id}"
            )

        human_decisions[req_id] = {

            "final_status":
            final_status,

            "decision":
            decision
        }

    # =================================================
    # GOVERNANCE PROVENANCE RECORDING
    # =================================================

    governance_record = record_governance_cycle(

        guideline_update,

        stage1_output,

        stage2_output,

        stage3_output,

        gate_results,

        gate2_results,

        gate3_results,

        conflict_results,

        arbitration_results,

        synthesis_results,

        confidence_outputs,

        repair_outputs,

        human_approval=human_decisions
    )

    # =================================================
    # PROVENANCE DISPLAY
    # =================================================


    st.header(
        "Governance Provenance Record"
    )

    with st.expander(
        "Why is provenance important?"
    ):

        st.markdown("""

    ### Purpose

    This provenance layer preserves
    governance lineage across the
    adaptive evolution lifecycle.

    ### Recorded Governance Stages

    The framework records:

    - interpretation reasoning,
    - propagation decisions,
    - adaptive evolution,
    - governance validation,
    - arbitration outcomes,
    - confidence estimation,
    - oversight escalation.

    ### Research Significance

    This enables:

    - auditability,
    - explainability continuity,
    - governance replay,
    - institutional accountability,
    - adaptive governance traceability.

    """)

    st.success(
        "Governance lineage "
        "recorded successfully."
    )

    st.json({

        "timestamp":
        governance_record["timestamp"],

        "guideline_update":
        governance_record[
            "guideline_update"
        ],

        "recorded_stages": [

            "Stage 1",
            "Stage 2",
            "Stage 3",

            "Gate 1",
            "Gate 2",
            "Gate 3",

            "Conflict Detection",
            "Governance Arbitration",
            "Governance Synthesis",

            "Confidence Assessment",

            "Human Oversight"
        ]
    })

    # =================================================
    # PROVENANCE RECORD
    # =================================================

    st.divider()

    st.header("Requirement Provenance Record")

    with st.expander("Why is provenance important?"):

        st.markdown("""
    ### Purpose
    Provenance records maintain full traceability
    across requirement evolution.

    ### What provenance captures
    - original requirement,
    - affected evolution,
    - governance outcomes,
    - repair history,
    - human decisions.

    ### Research significance
    This demonstrates explainable adaptive evolution
    with accountable governance lineage.

    ### Why this matters
    Safety-critical CPSS environments require:
    - auditability,
    - explainability,
    - regulatory traceability,
    - human accountability.
    """)

    provenance_rows = []

    for action in actions:

        req_id = action["id"]

        original_req = next(
            (
                r for r in requirements
                if r["id"] == req_id
            ),
            None
        )

        original_text = (
            original_req["text"]
            if original_req
            else "Unknown"
        )

        gate_match = next(
            (
                g for g in synthesis_results
                if g["id"] == req_id
            ),
            None
        )

        governance_result = (
            gate_match["final_state"]
            if gate_match
            else "UNKNOWN"
        )

        repair_match = next(
            (
                f for f in repair_outputs
                if f["id"] == req_id
            ),
            None
        )

        repair_text = (
            repair_match["repair_candidate"]
            if repair_match
            else "No repair required"
        )

        provenance_rows.append({

            "Requirement":
                req_id,

            "Previous Version":
                original_text,

            "Proposed Version":
                (
                    action["modified_text"]
                    if action["modified_text"]
                    else "Retained"
                ),

            "Governance Result":
                governance_result,

            "Repair Applied":
                repair_text,

            "Human Decision":
                human_decisions
        })

    st.dataframe(
        provenance_rows,
        use_container_width=True
    )

    st.success("Pipeline Execution Complete")
    
    # =================================================
    # STORE EVOLUTION MEMORY
    # =================================================

    memory_record = {

        "guideline": guideline_update,

        "stage1": stage1_output,

        "stage2": stage2_output,

        "stage3": stage3_output,

        "gate_results": gate_results,

        "synthesis": synthesis_results,

        "human_decision": human_decisions

    }

    st.session_state.evolution_history.append(
        memory_record
    )

    with open(history_file, "w") as f:

        json.dump(
            st.session_state.evolution_history,
            f,
            indent=2
        )

    # =================================================
    # EVOLUTION HISTORY
    # =================================================

    st.divider()

    st.header(
        "Evolution Memory"
    )

    with st.expander(
        "Why is evolution memory important?"
    ):

        st.markdown("""

    ### Purpose

    CPSS environments evolve continuously.

    This framework preserves:
    - historical guideline changes,
    - governance decisions,
    - repair history,
    - adaptive reasoning lineage.

    ### Research significance

    This transforms the framework from:
    - single-shot requirement adaptation

    into:
    - continuous governed requirement evolution.

    The system can later reason using:
    - prior governance outcomes,
    - previous repairs,
    - historical operational risks,
    - accumulated adaptive knowledge.

    """)

    history = st.session_state.evolution_history

    if history:

        for i, item in enumerate(history):

            st.subheader(
                f"Evolution Cycle {i+1}"
            )

            st.write(
                "### Guideline Update"
            )

            st.info(
                item["guideline"]
            )

            st.write(
                "### Human Decision"
            )

            st.success(
                item["human_decision"]
            )

            st.write(
                "### Governance Summary"
            )

            for result in item["synthesis"]:

                st.write(
                    f"""
    - {result['id']}
    → {result['final_state']}
    """
                )

            st.divider()

    # =================================================
    # ADAPTIVE GOVERNANCE TRACEABILITY GRAPH
    # =================================================

    import matplotlib.pyplot as plt
    import networkx as nx

    st.divider()

    st.header(
        "Adaptive Governance Traceability Graph"
    )

    with st.expander(
        "What does this graph represent?"
    ):

        st.markdown("""

    This graph visualizes governed adaptive
    requirement evolution in safety-critical CPSS.

    It demonstrates:

    - requirement evolution propagation,
    - governance validation flow,
    - adaptive governance outcomes,
    - recursive repair reasoning,
    - human-centered oversight,
    - longitudinal evolution continuity.

    The graph shows how governance constrains
    unsafe adaptive evolution while preserving
    safe operational adaptation.

    """)

    # =================================================
    # GRAPH INITIALIZATION
    # =================================================

    G = nx.DiGraph()

    # =================================================
    # MAIN PIPELINE
    # =================================================

    pipeline_nodes = [

        "Guideline\nUpdate",

        "Stage 1",

        "Stage 2",

        "Stage 3",

        "Gate 1",

        "Gate 2",

        "Gate 3",

        "Synthesis"
    ]

    # =================================================
    # PIPELINE FLOW
    # =================================================

    for i in range(len(pipeline_nodes) - 1):

        G.add_edge(

            pipeline_nodes[i],

            pipeline_nodes[i + 1]
        )

    # =================================================
    # OVERSIGHT NODES
    # =================================================

    G.add_node("Human Oversight")

    G.add_node("Evolution Memory")

    # =================================================
    # REQUIREMENT GOVERNANCE BRANCHES
    # =================================================

    for result in synthesis_results:

        req_id = result["id"]

        gov_state = result["final_state"]

        gov_node = f"{req_id}\n{gov_state}"

        # =============================================
        # SYNTHESIS TO REQUIREMENT GOVERNANCE
        # =============================================

        G.add_edge(

            "Synthesis",

            gov_node
        )

        G.add_edge(

            gov_node,

            req_id
        )

        # =============================================
        # PASS FLOW
        # =============================================

        if gov_state == "PASS":

            G.add_edge(

                gov_node,

                "Evolution Memory"
            )

        # =============================================
        # REVIEW FLOW
        # =============================================

        elif gov_state == "REVIEW":

            G.add_edge(

                gov_node,

                "Human Oversight"
            )

        # =============================================
        # FAIL FLOW
        # =============================================

        elif gov_state == "FAIL":

            # =============================================
            # ADD FEEDBACK REPAIR ONLY WHEN FAIL EXISTS
            # =============================================



            repair_node = f"Repair\n{req_id}"

            G.add_edge(

                gov_node,

                repair_node
            )


            G.add_edge(

                repair_node,

                "Human Oversight"
            )

    # =================================================
    # OVERSIGHT TO MEMORY
    # =================================================

    G.add_edge(

        "Human Oversight",

        "Evolution Memory"
    )

    # =================================================
    # MANUAL LAYOUT
    # =================================================

    pos = {

        # =============================================
        # MAIN PIPELINE
        # =============================================

        "Guideline\nUpdate": (0, 16),

        "Stage 1": (0, 14),

        "Stage 2": (0, 12),

        "Stage 3": (0, 10),

        "Gate 1": (-5, 8),

        "Gate 2": (0, 8),

        "Gate 3": (5, 8),

        "Synthesis": (0, 6),

        # =============================================
        # OVERSIGHT
        # =============================================

        "Human Oversight": (0, -1),

        "Evolution Memory": (0, -3)
    }

    # =================================================
    # REQUIREMENT POSITIONS
    # =================================================

    x_positions = [-6, 0, 6]

    for idx, result in enumerate(synthesis_results):

        req_id = result["id"]

        gov_state = result["final_state"]

        gov_node = f"{req_id}\n{gov_state}"

        x = x_positions[idx]

        pos[gov_node] = (x, 4)

        pos[req_id] = (x, 2)

        # =============================================
        # FAIL REPAIR POSITIONS
        # =============================================

        if gov_state == "FAIL":

            repair_node = f"Repair\n{req_id}"

            pos[repair_node] = (x, 0)

    # =================================================
    # NODE COLORS
    # =================================================

    node_colors = []

    for node in G.nodes():

        # =============================================
        # GOVERNANCE STATES
        # =============================================

        if "PASS" in node:

            node_colors.append("green")

        elif "REVIEW" in node:

            node_colors.append("orange")

        elif "FAIL" in node:

            node_colors.append("red")

        # =============================================
        # REPAIR
        # =============================================

        elif "Repair" in node:

            node_colors.append("purple")

        elif "Feedback" in node:

            node_colors.append("mediumorchid")

        # =============================================
        # GOVERNANCE GATES
        # =============================================

        elif "Gate" in node:

            node_colors.append("gold")

        # =============================================
        # OVERSIGHT
        # =============================================

        elif "Oversight" in node:

            node_colors.append("lightgreen")

        elif "Memory" in node:

            node_colors.append("plum")

        # =============================================
        # EVOLUTION
        # =============================================

        elif "Stage 3" in node:

            node_colors.append("orchid")

        # =============================================
        # DEFAULT
        # =============================================

        else:

            node_colors.append("skyblue")

    # =================================================
    # DRAW GRAPH
    # =================================================

    fig, ax = plt.subplots(

        figsize=(18, 14)
    )

    nx.draw(

        G,

        pos,

        with_labels=True,

        node_size=5200,

        node_color=node_colors,

        font_size=11,

        font_weight="bold",

        arrows=True,

        arrowsize=22,

        width=1.8,

        ax=ax
    )

    ax.set_title(

        "Governed Adaptive Evolution Flow",

        fontsize=18,

        fontweight="bold"
    )

    ax.axis("off")

    st.pyplot(fig)