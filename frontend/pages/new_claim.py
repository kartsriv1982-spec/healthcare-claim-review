import streamlit as st

from services.claim_service import upload_claim

st.title("📤 New Claim Submission")

uploaded_file = st.file_uploader(
    "Upload Claim Document",
    type=["pdf", "png", "jpg"]
)

claim_type = st.selectbox(
    "Claim Type",
    ["Hospitalization", "Outpatient", "Dental"]
)

if st.button(
    "Process Claim",
    key="process_claim_btn"
):

    if uploaded_file is None:

        st.warning(
            "Please upload a claim document."
        )

    else:

        result = upload_claim(
            uploaded_file
        )

        st.success(
            f"Claim Created : {result['claim_id']}"
        )