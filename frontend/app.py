import streamlit as st
st.set_page_config(
    page_title="Healthcare Claim Review",
    page_icon="🏥",
    layout="wide"
)

# Initialize session
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Redirect to login if not authenticated
if not st.session_state["authenticated"]:
    st.switch_page("pages/login.py")

st.title("🏥 Healthcare Insurance Claim Review Assistant")

st.success(
    f"Welcome {st.session_state.get('username', 'User')}"
)

st.markdown("""
### AI Powered Healthcare Claim Review Platform

- 📄 Claim Upload
- 🔍 OCR Extraction (Amazon Textract)
- 🤖 AI Claim Review
- 📊 Dashboard & Reporting
- 🔐 Secure Authentication

Use the left sidebar to navigate through the application.
""")