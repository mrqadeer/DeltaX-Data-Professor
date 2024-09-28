import streamlit as st


# Initialize session states for credentials
if 'provider_choice' not in st.session_state:
    st.session_state['provider_choice'] = None
if 'llm_choice' not in st.session_state:
    st.session_state['llm_choice'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = 'Qadeer'
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = None
if 'signed_in' not in st.session_state:
    st.session_state['signed_in'] = False

    

st.set_page_config(
    page_title="DeltaX Data Professor",
    page_icon=":robot:",
    layout="wide",
    initial_sidebar_state="expanded",
)

def load_css():
    with open("static/css/style.css") as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

load_css()
# Page setup
home_page=st.Page(
    title="Home",
    page="views/home.py",
    icon=":material/home:",
    default=True,
    
)
credentials_page=st.Page(
    title="Credentials",
    page="views/credentials.py",
    icon=":material/lock:",
    default=False,
    
)

delta_ai_page=st.Page(
    title="DeltaX Data Professor",
    page="views/delta_ai.py",
    icon=":material/robot:",
    default=False,
)
# pg=st.navigation(pages=[home_page,credentials_page,axis_ai_page])
# Navigation with 
pg = st.navigation(
    {
        "Home": [home_page],
        "Sign In": [credentials_page],
        "DeltaX Assistant": [delta_ai_page],
    }
)
st.logo("static/assets/logo/delta.png")
if __name__ == "__main__":
    pg.run()

