import streamlit as st
from components.input_components import get_credentials

def credentials_page():

    st.header("Delta Data Professor Credentials", anchor=False)


    # HTML content with bulleted list and clickable links
    st.markdown("""
        <div class="api-container">
            <p>Before you get started, kindly get your API Keys from any of the following providers:</p>
            <ul>
                <li><a href="https://platform.openai.com/signup" target="_blank">OpenAI</a></li>
                <li><a href="https://cloud.google.com/gemini/" target="_blank">Google Gemini</a></li>
                <li><a href="https://groq.com/" target="_blank">Groq</a></li>
                <li><a href="https://huggingface.co/" target="_blank">HuggingFace</a></li>
                <li><a href="https://claude.ai/" target="_blank">Claude</a></li>
            </ul>
        </div>
        <br>
        """, unsafe_allow_html=True)



        # Main function to get credentials



    # Main app layout
    cols = st.columns(3)
    with cols[1]:
        sign_in = st.button("Sign In", key="sign_in")
        if sign_in:
            
            get_credentials()
        
# if __name__ == "__main__":
credentials_page()