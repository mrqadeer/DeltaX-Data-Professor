# components/input_components.py
import time
import pandas as pd
import streamlit as st
from utils.contsant import PROVIDERS
from utils.get_models import get_provider
from typing import List, Tuple, Union, Optional,Any,Dict

# Define type aliases for clarity
UploadedFiles = Optional[List]
SelectedDatabase = Optional[str]
def get_model_and_key(provider_choice: str):
    
    key = None
    for provider in PROVIDERS:
        if provider== provider_choice:
            key = st.text_input(PROVIDERS[provider]['key'], type="password")
            if key:
                llm_choice=st.selectbox(f"{provider} Models",sorted(get_provider(provider, key).get_models()))
            else:
                llm_choice=st.selectbox(f"{provider} Models",[])
    return  key,llm_choice


@st.dialog("Sign In to get touch in DeltaX")
def get_credentials():
    st.session_state['username'] = st.text_input("Username")
    st.session_state['provider'] = st.selectbox("Provider", ["PandasAI", "OpenAI", "Google Gemini", "Groq", "Antropic"])
    st.markdown(f"<span style='color: yellow;'>Get {PROVIDERS[st.session_state['provider']]['key']}&nbsp;</span><a href='{PROVIDERS[st.session_state['provider']]['url']}' target='_blank'>here</a>", unsafe_allow_html=True)
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
        st.session_state['credentials'] = {
                                        st.session_state['provider']:{
                                           'api_key': st.session_state['api_key'], 
                                           'model': st.session_state['llm_choice'],
                                           'temperature': 0.7}
                                            }
        st.session_state['signed_in'] = True
        time.sleep(1.5)
        st.switch_page("views/delta_ai.py")
        
    else:
        return 
    
def get_uploaded_files() -> Union[List[Any], Any]:
    
    file_type = st.selectbox("Select file type", ["CSV", "TSV", "XLSX"])
    if file_type == "CSV":
        uploaded_files=st.file_uploader("Choose CSV files", type=["csv"], accept_multiple_files=True)
        st.session_state['is_uploaded'] = True
        return uploaded_files if uploaded_files else None
    
    elif file_type == "TSV":
        uploaded_files=st.file_uploader("Choose TSV files", type=["tsv"], accept_multiple_files=True)
        st.session_state['is_uploaded'] = True
        return uploaded_files if uploaded_files else None
    elif file_type == "XLSX":
        uploaded_file=st.file_uploader("Choose XLSX files", type=["xlsx", "xls"], accept_multiple_files=False)
        if uploaded_file is not None:
            sheets=pd.ExcelFile(uploaded_file).sheet_names
            sheets_names = get_sheet_choice(sheets)
            st.session_state['selected_sheets'] = sheets_names
            st.session_state['is_uploaded'] = True
            return uploaded_file if uploaded_file else None
    return None


def get_sheet_choice(sheets: List[str]) -> List[str]:
    """Get the list of sheet names from the user."""

    sheet_names = st.multiselect("Select Sheets", sheets)
    st.session_state['selected_sheets'] = sheet_names
    return sheet_names

def get_database_credentials(db_choice: str) -> Tuple[str, str]:
    """Get the database credentials from the user."""
    match db_choice:
        case "MySQL":
            return get_mysql_credentials()
        case "SQLite":
            return get_sqlite_credentials()
        case "PostgreSQL":
            return get_postgresql_credentials()

        case _:
            return None, None
def get_database():
    db_choice=st.selectbox("Select Database", ["MySQL", "SQLite", "PostgreSQL", ])
    return db_choice

def get_mysql_credentials() -> Dict:
    """Get MySQL credentials from the user."""
    cols = st.columns(3, gap="small",vertical_alignment="center")
    with cols[0]:
        host = st.text_input("Host", "localhost")
    with cols[1]:
        port = st.text_input("Port", "3306")
    with cols[2]: 
        user = st.text_input("User")
    cols = st.columns(3, gap="small",vertical_alignment="center")
    with cols[0]:
        password = st.text_input("Password", type="password")
    with cols[1]:
        database = st.text_input("Database")
    with cols[2]:
        table = st.text_input("Table")
    if all([host, port, user, password, database, table]):
        return {"MySQL": {"host": host, "port": port, "username": user, "password": password, "database": database, "table": table}}
    else:
        
        return None

def get_sqlite_credentials() -> Dict:
    """Get SQLite credentials from the user."""
    database = st.text_input("Database")
    table = st.text_input("Table")
    if all([database, table]):
        return {"SQLite": {"database": database, "table": table}}
    else:
        
        return None
        
def get_postgresql_credentials() -> Dict:
    """Get PostgreSQL credentials from the user."""
    cols = st.columns(3, gap="small",vertical_alignment="center")
    with cols[0]:
        host = st.text_input("Host", "localhost")
    with cols[1]:
        port = st.text_input("Port", "3306")
    with cols[2]: 
        user = st.text_input("User")
    with cols[0]:
        password = st.text_input("Password", type="password")
    with cols[1]:
        database = st.text_input("Database")
    with cols[2]:
        table = st.text_input("Table")
    if all([host, port, user, password, database, table]):
        return {"PostgreSQL": {"host": host, "port": port, "user": user, "password": password, "database": database, "table": table}}
    else:
        
        return None

   