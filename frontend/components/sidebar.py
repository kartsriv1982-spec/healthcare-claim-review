import streamlit as st


def render_sidebar():

    with st.sidebar:

        st.write(
            f"Welcome "
            f"{st.session_state.get('username','User')}"
        )

        if st.button(
                "Logout",
                key="logout_button"):

            st.session_state.clear()

            st.rerun()