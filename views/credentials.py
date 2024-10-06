import streamlit as st
from components.input_components import get_credentials
from utils.contsant import PROVIDERS


def credentials_page():
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
