# components/input_components.py
import time
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
                               "Airtable", "GoogleBigQuery"])
    
    return db_choice


def get_databases_credentials(db_choice: str) -> Tuple[str, str]:
    """Get the database credentials from the user."""
    match db_choice:
        case "MySQL":
            return get_mysql_credentials()
        case "SQLite":
            return get_sqlite_credentials()
        case "PostgreSQL":
            return get_postgresql_credentials()
        case "Snowflake":
            return get_snowflake_credentials()
        case "Databricks":
            return get_databricks_credentials()
        case "Airtable":
            return get_airtable_credentials()
        case "GoogleBigQuery":
            return get_google_bigquery_credentials()
        case _:
            return None, None
    

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
    return {"MySQL": {"host": host, "port": port, "username": user, "password": password, "database": database, "table": table}}
    

def get_sqlite_credentials() -> Dict:
    """Get SQLite credentials from the user."""
    database = st.text_input("Database")
    table = st.text_input("Table")
    return {"SQLite": {"database": database, "table": table}}
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

    return {"PostgreSQL": {"host": host, "port": port, "user": user, "password": password, "database": database, "table": table}}
    
def get_snowflake_credentials() -> Dict:
    """Get Snowflake credentials from the user."""
    cols = st.columns(3, gap="small",vertical_alignment="center")
    with cols[0]:
        account = st.text_input("Account","ehxzojy-ue47135")
    with cols[1]:
        database = st.text_input("Database","SNOWFLAKE_SAMPLE_DATA")
    with cols[2]:
        username = st.text_input("Username","test")

    with cols[0]:
        password = st.text_input("Password","*****", type="password")
    with cols[1]:
        table = st.text_input("Table","lineitem")
    with cols[2]:
        warehouse = st.text_input("Warehouse","COMPUTE_WH")
    dbSchema = st.text_input("Database Schema","tpch_sf1")
    return {"Snowflake": {"account": account, "database": database, "username": username, "password": password, "table": table, "warehouse": warehouse, "dbSchema": dbSchema}}
    
    
def get_databricks_credentials() -> Dict:
    """Get Databricks credentials from the user."""
    cols = st.columns(3, gap="small",vertical_alignment="center")
    with cols[0]:
        host = st.text_input("Host", "adb-*****.azuredatabricks.net")
    with cols[1]:
        database = st.text_input("Database", "default")
    with cols[2]:
        token= st.text_input("Token", "dapidfd412321", type="password")

    with cols[0]:
        port = st.text_input("Port", "443")
    with cols[1]:
        table = st.text_input("Table", "loan_payments_data")
    with cols[2]:
        httpPath = st.text_input("HTTP Path", "/sql/1.0/warehouses/213421312")
    return {"Databricks": {"host": host, "database": database, "token": token, "port": port, "table": table, "httpPath": httpPath}}
    
def get_airtable_credentials() -> Dict:
    """Get Airtable credentials from the user."""
    
    base_id = st.text_input("Base ID")
    table_name = st.text_input("Table Name")
    api_key = st.text_input("API Key")

    return {"Airtable": {"base_id": base_id, "table_name": table_name, "api_key": api_key}}

def get_google_bigquery_credentials() -> Dict:
    """Get Google BigQuery credentials from the user."""
   
    cols=st.columns(2, gap="small",vertical_alignment="center")
    with cols[0]:
        credentials_path = st.text_input("Credentials Path", "path to keyfile.json")
    with cols[1]:
        database = st.text_input("Database", "dataset_name")
    with cols[0]:
        table = st.text_input("Table", "table_name")
    with cols[1]:
        projectID = st.text_input("Project ID", "Project_id_name", type="password")

    return {"Google BigQuery": {"credentials_path": credentials_path, "database": database, "table": table, "projectID": projectID}}
   

def get_data_source(source:str) -> str:
    """Get data source choice from the user."""
    # data_source = st.selectbox("Select an option:", ["Upload File", "Connect to Database"], index=0)
    if source=='file':
        file_choice = st.selectbox("Select file type", ["CSV", "TSV", "XLSX"])
        uploaded_files = get_uploaded_files(file_choice)
        return uploaded_files
    else:
        db_choice = get_database_choice()
        st.session_state["db_choice"] = db_choice

        return db_choice
