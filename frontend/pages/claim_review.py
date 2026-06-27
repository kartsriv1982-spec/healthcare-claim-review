
import streamlit as st
import requests
# ==================================================
# Authentication Check
# ==================================================

if not st.session_state.get("authenticated", False):
    st.switch_page("pages/login.py")

# ==================================================
# Configuration
# ==================================================

API_BASE_URL = "http://localhost:8000/api/v1"

# ==================================================
# Page Setup
# ==================================================

st.set_page_config(
    page_title="Claim Review",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Human-in-the-Loop Claim Review")

# ==================================================
# Session Initialization
# ==================================================

if "claim_data" not in st.session_state:
    st.session_state["claim_data"] = None

if "review_result" not in st.session_state:
    st.session_state["review_result"] = None

if "submission_success" not in st.session_state:
    st.session_state["submission_success"] = None

if "submission_error" not in st.session_state:
    st.session_state["submission_error"] = None


# ==================================================
# Success / Error Messages
# ==================================================

if st.session_state["submission_success"]:

    st.toast(
        st.session_state["submission_success"],
        icon="✅"
    )

    st.session_state["submission_success"] = None

if st.session_state["submission_error"]:

    st.toast(
        st.session_state["submission_error"],
        icon="❌"
    )

    st.session_state["submission_error"] = None



# ==================================================
# Claim Selection
# ==================================================

claim_id = st.text_input(
    "Claim ID",
    value="CLM-1001"
)

# ==================================================
# Load Claim
# ==================================================

col1, col2 = st.columns([2, 1])

with col1:

    if st.button(
        "📂 Load Claim",
        use_container_width=True
    ):

        try:

            response = requests.get(
                f"{API_BASE_URL}/claims/{claim_id}/review"
            )

            response.raise_for_status()

            st.session_state["claim_data"] = (
                response.json()
            )

            st.session_state["review_result"] = None

            st.success(
                "Claim Loaded Successfully"
            )

        except Exception as ex:

            st.error(
                f"Failed to load claim: {str(ex)}"
            )

with col2:

    if st.button(
        "🔄 Reset",
        use_container_width=True
    ):

        st.session_state["claim_data"] = None
        st.session_state["review_result"] = None

        st.rerun()

# ==================================================
# Claim Information
# ==================================================

if st.session_state["claim_data"]:

    claim = st.session_state["claim_data"]

    st.divider()

    st.subheader("📋 Claim Information")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Claim ID:** "
            f"{claim.get('claim_id')}"
        )

        st.write(
            f"**Status:** "
            f"{claim.get('status')}"
        )

    with col2:

        status = claim.get("status", "")

        if status == "OCR_COMPLETED":

            st.success("✅ OCR Completed")

        elif status == "PROCESSING":

            st.warning("⏳ OCR Pending")

        elif status == "PENDING_HUMAN_REVIEW":

            st.success("✅ AI Review Completed")

        elif status == "APPROVED":

            st.success("✅ Claim Approved")

        elif status == "REJECTED":

            st.error("❌ Claim Rejected")

        elif status == "REQUEST_INFO":

            st.warning("📄 Additional Information Requested")

        else:

            st.info(status)

# ==================================================
# OCR Output
# ==================================================

if st.session_state["claim_data"]:

    claim = st.session_state["claim_data"]

    st.divider()

    st.subheader("📄 OCR Extracted Text")

    st.text_area(
        label="OCR Output",
        value=claim.get(
            "ocr_text",
            "No OCR text available"
        ),
        height=250,
        disabled=True
    )

# ==================================================
# AI Review Trigger
# ==================================================

claim_data = st.session_state["claim_data"]

if (
    claim_data
    and not st.session_state["review_result"]
    and claim_data.get("status") not in [
        "APPROVED",
        "REJECTED",
        "REQUEST_INFO"
    ]
):
    st.divider()

    if st.button(
        "🚀 Start AI Review",
        use_container_width=True
    ):

        try:

        # --------------------------------------
        # Step 1 : OCR Extraction
        # --------------------------------------

            with st.spinner("Running OCR Extraction..."):

                ocr_response = requests.post(
                    f"{API_BASE_URL}/claims/{claim_id}/extract"
                )

                ocr_response.raise_for_status()

                # Refresh claim data so OCR text appears immediately
                claim_response = requests.get(
                    f"{API_BASE_URL}/claims/{claim_id}/review"
                )

                claim_response.raise_for_status()

                st.session_state["claim_data"] = claim_response.json()

            # --------------------------------------
            # Step 2 : AI Review
            # --------------------------------------

            with st.spinner("Running AI Review..."):

                    review_response = requests.post(
                        f"{API_BASE_URL}/claims/{claim_id}/review"
                    )

                    review_response.raise_for_status()

                    result = review_response.json()

                    # ------------------------------------------
                    # Validation Failed
                    # ------------------------------------------

                    if not result.get("validation_status", True):

                        st.session_state["review_result"] = result

                    else:

                        st.session_state["review_result"] = result

            st.rerun()

        except Exception as ex:

            st.error(f"Review Failed: {str(ex)}")

# ==================================================
# Validation Failure
# ==================================================

if (

    st.session_state["review_result"]

    and

    not st.session_state["review_result"].get(
        "validation_status",
        True
    )

):

    result = st.session_state["review_result"]

    st.divider()

    st.error("❌ Validation Failed")

    st.warning(result.get("message"))

    st.subheader("Missing Mandatory Fields")

    for field in result.get("missing_fields", []):

        st.write(f"• {field}")

# ==================================================
# AI Recommendation
# ==================================================



if (

    st.session_state["review_result"]

    and

    st.session_state["review_result"].get(
        "validation_status",
        True
    )

):

    result = st.session_state["review_result"]

    st.divider()

    st.subheader(
        "🤖 AI Recommendation"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Recommendation",
            result.get(
                "recommendation",
                "N/A"
            )
        )

    with col2:

        st.metric(
            "Confidence",
            f"{result.get('confidence',0)}%"
        )

    st.info(
        result.get(
            "summary",
            "No summary available"
        )
    )

    findings = result.get(
        "findings",
        []
    )

    if findings:

        st.subheader("🔎 Findings")

        for finding in findings:

            st.write(
                f"✅ {finding}"
            )

# ==================================================
# Human Review Section
# ==================================================

if (

    st.session_state["review_result"]

    and

    st.session_state["review_result"].get(
        "validation_status",
        True
    )

    and

    st.session_state["claim_data"]["status"]

    not in [

        "APPROVED",

        "REJECTED",

        "REQUEST_INFO"

    ]

):
    st.divider()

    st.subheader(
        "👨 Human Review"
    )

    # AI recommendation from review result
    ai_recommendation = st.session_state["review_result"].get(
        "recommendation",
        "APPROVE"
    )

    options = [
        "APPROVE",
        "REJECT",
        "REQUEST_INFO"
    ]
    st.info(
        f"🤖 AI Recommendation: {ai_recommendation}"
    )
    decision = st.radio(
        "Reviewer Decision",
        options,
        index=options.index(ai_recommendation)
            if ai_recommendation in options
            else 0,
        horizontal=True
    )

    comments = st.text_area(
            "Reviewer Comments"
    )

    reviewer = st.text_input(
        "Reviewer Name",
        value=st.session_state.get(
            "username",
            "Reviewer"
        )
    )

    if st.button(
        "✅ Submit Decision",
        use_container_width=True
    ):

        payload = {

            "decision":
                decision,

            "comments":
                comments,

            "reviewed_by":
                reviewer
        }

        try:

            response = requests.post(
                f"{API_BASE_URL}/claims/{claim_id}/human-review",
                json=payload
            )

            response.raise_for_status()

            st.session_state["submission_success"] = (
                        f"Decision '{decision}' submitted successfully by {reviewer}."
)

            # Return page to pre-review state

            st.session_state[
                "review_result"
            ] = None

            claim_response = requests.get(
                f"{API_BASE_URL}/claims/{claim_id}/review"
            )

            claim_response.raise_for_status()

            st.session_state["claim_data"] = claim_response.json()

            st.session_state["review_result"] = None


            st.rerun()

        except Exception as ex:

            st.session_state["submission_error"] = (
            f"Submission Failed: {str(ex)}"
            )

            st.rerun()

# ==================================================
# Audit Information
# ==================================================

if st.session_state["claim_data"]:

    st.divider()

    st.subheader("📋 Audit Information")

    st.write(
        f"**Reviewer:** "
        f"{st.session_state.get('username', 'N/A')}"
    )

    st.write(
        f"**Claim ID:** "
        f"{claim_id}"
    )

    with st.expander("🔍 View Complete Audit Trail"):

        try:

            response = requests.get(
                f"{API_BASE_URL}/claims/{claim_id}/audit"
            )

            response.raise_for_status()

            audit_logs = response.json()

            for log in audit_logs:

                st.markdown(
                    f"""
**Stage:** {log["stage"]}

**Actor:** {log["actor"]}

**Action:** {log["action"]}

**Time:** {log["created_date"]}

---
"""
                )

        except Exception as ex:

            st.error(
                f"Unable to load audit trail: {str(ex)}"
            )