import streamlit as st

from services.claim_service import (
    get_claim_review,
    submit_decision
)

st.title("🔍 Claim Review")

# ------------------------------------
# Claim Selection
# ------------------------------------

claim_id = st.text_input(
    "Claim ID",
    value="CLM-1001"
)

try:

    data = get_claim_review(claim_id)

    col1, col2, col3 = st.columns(3)

    # ------------------------------------
    # Extracted Claim Data
    # ------------------------------------

    with col1:

        st.subheader("Extracted Data")

        # Mock values for Sprint-2
        st.text("Patient ID : P12345")
        st.text("Patient : John Doe")
        st.text("Hospital : City Hospital")
        st.text("Amount : $1200")

    # ------------------------------------
    # Policy Context
    # ------------------------------------

    with col2:

        st.subheader("Policy Context")

        st.info("""
Policy Section 4.2

Coverage Limit : $5000

Patient Eligible
""")

    # ------------------------------------
    # AI Recommendation
    # ------------------------------------

    with col3:

        st.subheader("AI Recommendation")

        decision = data.get(
            "recommendation",
            "UNKNOWN"
        )

        confidence = data.get(
            "confidence",
            0
        )

        if decision == "APPROVE":

            st.success(decision)

        elif decision == "REJECT":

            st.error(decision)

        else:

            st.warning(decision)

        st.metric(
            "Confidence",
            f"{confidence}%"
        )

    st.divider()

    # ------------------------------------
    # Human Review Notes
    # ------------------------------------

    notes = st.text_area(
        "Adjuster Notes"
    )

    col4, col5 = st.columns(2)

    # ------------------------------------
    # Approve Claim
    # ------------------------------------

    with col4:

        if st.button(
            "Approve Claim",
            key="approve_claim_btn",
            width="stretch"
        ):

            result = submit_decision(
                claim_id=claim_id,
                decision="APPROVE",
                comments=notes
            )

            st.success(
                f"Claim {result['decision']} successfully"
            )

    # ------------------------------------
    # Reject Claim
    # ------------------------------------

    with col5:

        if st.button(
            "Reject Claim",
            key="reject_claim_btn",
            width="stretch"
        ):

            result = submit_decision(
                claim_id=claim_id,
                decision="REJECT",
                comments=notes
            )

            st.error(
                f"Claim {result['decision']} successfully"
            )

except Exception as e:

    st.error(
        f"Unable to load claim review data.\n\n{str(e)}"
    )