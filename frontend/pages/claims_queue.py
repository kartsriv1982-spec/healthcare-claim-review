import streamlit as st
import pandas as pd

import pandas as pd

from services.claim_service import get_claims

claims = get_claims()

df = pd.DataFrame(claims)

st.title("📋 Claims Queue")

st.dataframe(
    df,
    use_container_width=True
)