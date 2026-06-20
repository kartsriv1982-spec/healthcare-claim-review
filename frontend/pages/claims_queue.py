import streamlit as st
import pandas as pd

from components.sidebar import render_sidebar

render_sidebar()

if not st.session_state.get(
        "authenticated",
        False):

    st.error(
        "Please login first"
    )

    st.stop()

from services.claim_service import get_claims

claims = get_claims()

df = pd.DataFrame(claims)

st.title("📋 Claims Queue")

st.dataframe(
    df,
    use_container_width=True
)