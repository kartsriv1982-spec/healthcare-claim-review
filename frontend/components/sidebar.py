import streamlit as st

def render_sidebar():

    with st.sidebar:

        st.success(
            f"👤 {st.session_state.get('username')}"
        )

        st.divider()

        if st.button(
                "🚪 Logout",
                use_container_width=True):

            st.session_state.clear()

            st.switch_page(
                "pages/login.py"
            )