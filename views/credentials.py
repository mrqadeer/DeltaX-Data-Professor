import streamlit as st
from components.input_components import get_credentials
from utils.contsant import PROVIDERS


def credentials_page():
    st.markdown("<h2>DeltaX Data Professor Credentials</h2>", unsafe_allow_html=True)
    st.markdown("<p>Before you get started, kindly get your API Keys from any of the following providers:</p>",unsafe_allow_html=True)
    for provider in PROVIDERS:
        st.markdown(f"""
        <div class="container mt-4">
            <div class="row">
                <div class="col-md-4 mb-4">
                    <div class="api-container">
                        <a href="{PROVIDERS[provider]['url']}" target="_blank" class="btn btn-primary w-100">{provider}</a>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    # Main app layout
    cols = st.columns([4.6,2,4])
    with cols[1]:
        sign_in = st.button("Get Started", key="get-started")
        if sign_in:

            get_credentials()


# if __name__ == "__main__":
credentials_page()
