# components/input_components.py
import time
import streamlit as st
from utils.contsant import PROVIDERS
from utils.get_models import get_provider
from typing import List, Tuple, Union, Optional,Any

# Define type aliases for clarity
UploadedFiles = Optional[List]
SelectedDatabase = Optional[str]
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
    
def get_uploaded_files(file_type: str) -> Union[List[Any], Any]:
    """
    Prompt the user to upload files of a specific type.

    Parameters:
        file_type (str): The type of file to be uploaded (e.g., 'CSV', 'TSV', 'XLSX').

    Returns:
        Union[List[Any], Any]: The uploaded files, either as a list (multiple files) or a single file object.
    """
    if file_type == "CSV":
        uploaded_files=st.file_uploader("Choose CSV files", type=["csv"], accept_multiple_files=True)
        return uploaded_files if uploaded_files else None
    
    elif file_type == "TSV":
        uploaded_files=st.file_uploader("Choose TSV files", type=["tsv"], accept_multiple_files=True)
        return uploaded_files if uploaded_files else None
    elif file_type == "XLSX":
        uploaded_file=st.file_uploader("Choose XLSX files", type=["xlsx", "xls"], accept_multiple_files=False)
        import pandas as pd
        if uploaded_file is not None:
            sheets=pd.ExcelFile(uploaded_file).sheet_names
            sheets_names = get_sheet_choice(sheets)
            st.session_state['selected_sheets'] = sheets_names
            return uploaded_file if uploaded_file else None
    return None


def get_sheet_choice(sheets: List[str]) -> List[str]:
    """Get the list of sheet names from the user."""

    sheet_names = st.multiselect("Select Sheets", sheets)
    st.session_state['selected_sheets'] = sheet_names
    return sheet_names

def get_database_choice() -> SelectedDatabase:
    """Get the selected database type."""
    db_choice = st.selectbox("Select Database", 
                              ["MySQL", "SQLite", "PostgreSQL", 
                               "Snowflake", "Databricks", 
                               "Airtable", "GoogleBigQuery", 
                               "Yahoo Finance"])
    return db_choice

def get_data_source() -> Tuple[Union[UploadedFiles, SelectedDatabase], str]:
    """Get data source choice from the user."""
    data_source = st.selectbox("Select an option:", ["Upload File", "Connect to Database"], index=0)

    if data_source == "Upload File":
        file_choice = st.selectbox("Select file type", ["CSV", "TSV", "XLSX"])
        uploaded_files = get_uploaded_files(file_choice)
        return uploaded_files, "uploaded_files"

    elif data_source == "Connect to Database":
        db_choice = get_database_choice()
        return db_choice, "selected_db"

    return None, ""