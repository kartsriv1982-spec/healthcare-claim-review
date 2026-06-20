import streamlit as st

from services.auth_service import login

st.title("Healthcare Claim Review")

st.subheader("Login")

username = st.text_input(
    "Username"
)

password = st.text_input(
    "Password",
    type="password"
)

if st.button(
        "Login",
        key="login_button"):

    try:

        result = login(
            username,
            password
        )

        st.session_state["jwt"] = (
            result["token"]
        )

        st.session_state["authenticated"] = True

        st.session_state["username"] = (
            username
        )

        st.success(
            "Login Successful"
        )

    except Exception as ex:

        st.error(
            f"Login Failed : {str(ex)}"
        )