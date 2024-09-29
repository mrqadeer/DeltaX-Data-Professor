# components/input_components.py
import time
import streamlit as st
from utils.contsant import PROVIDERS
from utils.get_models import get_provider
def get_model_and_key(provider_choice: str):
    
    key = None
    for provider in PROVIDERS:
        if provider== provider_choice:
            key = st.text_input(PROVIDERS[provider]['key'], type="password")
            if key:
                llm_choice=st.selectbox(f"{provider} Models",get_provider(provider, key).get_models())
            else:
                llm_choice=st.selectbox(f"{provider} Models",[])
    return  key,llm_choice


@st.dialog("Sign In to get touch in DeltaX")
def get_credentials():
    st.session_state['username'] = st.text_input("Username")
    st.session_state['provider'] = st.selectbox("Provider", ["PandasAI", "OpenAI", "Google Gemini", "Groq", "Antropic"])
    st.session_state['api_key'], st.session_state['llm_choice'] = get_model_and_key(st.session_state['provider'])
    
    # Check if all fields are filled to enable the submit button
    if st.session_state['username'] and st.session_state['provider'] and st.session_state['api_key'] and st.session_state['llm_choice']:
        st.session_state['signed_in'] = True
        
    else:
        st.session_state['signed_in'] = False

    submit = st.button("Submit", disabled=not st.session_state['signed_in'],key="submit")

    if submit:
        # if save_credentials(st.session_state['llm_choice'], st.session_state['api_key']):
        st.success(f"Nice to have you {st.session_state['username'].title()}!")
        st.session_state['signed_in'] = True
        time.sleep(1.5)
        st.switch_page("views/delta_ai.py")
        
    else:
        return 
    