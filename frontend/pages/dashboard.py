import streamlit as st

st.title("📊 Dashboard")

col1, col2, col3, col4 = st.columns(4)

from services.dashboard_service import (
    get_dashboard_metrics
)
metrics = get_dashboard_metrics()

col1.metric(
    "Total Claims",
    metrics["total_claims"]
)

col2.metric(
    "Pending Review",
    metrics["pending_review"]
)

col3.metric(
    "Approved Today",
    metrics["approved_today"]
)

col4.metric(
    "Rejected Today",
    metrics["rejected_today"]
)

st.divider()

st.subheader("Claims Overview")

chart_data = {
    "Approved": 87,
    "Rejected": 13,
    "Pending": 24
}

st.bar_chart(chart_data)