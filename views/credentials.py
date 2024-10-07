import streamlit as st
from components.input_components import get_credentials


def credentials_page():
    """
    This function is the main page for the user to enter their credentials
    to get access to the DeltaX Data Professor application.

    The page displays a heading and a brief description of the application.
    The user is then asked to enter their username, select a provider, and
    enter their API key and model name.

    If the user enters all the required information and clicks the "Submit"
    button, the signed_in flag is set to True and the user is redirected to
    the DeltaX Data Professor page.

    If the user does not enter all the required information, the signed_in
    flag remains False and the user stays on the sign-in page.
    """
    st.markdown("<h2>DeltaX Data Professor Credentials</h2>", unsafe_allow_html=True)
    
    st.markdown("<span>Sign in to get access to DeltaX Data Professor</span>", unsafe_allow_html=True)
    # Main app layout
    cols = st.columns([4.6,2,4])
    with cols[1]:
        sign_in = st.button("Get Started", key="get-started")
        if sign_in:

            get_credentials()


# if __name__ == "__main__":
credentials_page()
