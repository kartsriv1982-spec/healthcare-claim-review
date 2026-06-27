import streamlit as st
from services.auth_service import login

st.set_page_config(
    page_title="Login",
    page_icon="🔐",
    layout="centered"
)

# Already logged in?
if st.session_state.get("authenticated"):
    st.switch_page("app.py")

# Center card
col1, col2, col3 = st.columns([1, 2, 1])

with col2:

    st.markdown(
        """
        <div style='text-align:center'>
            <h1>🏥</h1>
            <h2>Healthcare Claim Review</h2>
            <p>AI Powered Claim Processing Platform</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    username = st.text_input(
        "Username",
        placeholder="Enter username"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter password"
    )

    if st.button(
        "🔐 Login",
        use_container_width=True,
        key="login_btn"
    ):

        if not username or not password:

            st.warning(
                "Username and Password are required"
            )

        else:

            try:

                result = login(
                    username,
                    password
                )

                st.session_state["jwt"] = (
                    result["token"]
                )

                st.session_state["authenticated"] = True

                st.session_state["username"] = username

                st.success(
                    "Login Successful"
                )

                st.switch_page("app.py")

            except Exception as ex:

                st.error(
                    "Invalid username or password"
                )

    st.divider()

    st.caption(
        "Healthcare Insurance Claim Review System v1.0"
    )