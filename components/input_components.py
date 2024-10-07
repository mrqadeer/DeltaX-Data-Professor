# components/input_components.py
import time
import pandas as pd
import streamlit as st
from streamlit_mic_recorder import mic_recorder
from utils.contsant import PROVIDERS
from utils.get_models import get_provider
from typing import List, Tuple, Union, Optional,Any,Dict

# Define type aliases for clarity
UploadedFiles = Optional[List]
SelectedDatabase = Optional[str]
def get_model_and_key(provider_choice: str)-> Tuple[Optional[str], Optional[str]]:
    
    """
    Prompt the user to enter their API key and select a model for the given provider choice.

    Args:
        provider_choice (str): The name of the provider.

    Returns:
        Tuple[Optional[str], Optional[str]]: A tuple containing the API key and the selected model name. If the API key is not entered, both values are None.
    """

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
    """
    Prompt the user to sign in to the application by providing their username, selecting a provider, and entering their API key and model name.

    The user is prompted to enter their API key and select a model for the given provider choice in a separate dialog.

    If the user enters all the required information and clicks the "Submit" button, the signed_in flag is set to True and the user is redirected to the DeltaX Data Professor page.

    If the user does not enter all the required information, the signed_in flag remains False and the user stays on the sign-in page.

    Parameters:
        None

    Returns:
        None
    """
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
    
    """
    Prompts the user to select a file type and upload files of the selected type.

    If the user selects CSV or TSV, they are prompted to upload multiple files of the selected type.

    If the user selects XLSX, they are prompted to upload a single file and select one or more sheets from the uploaded file.

    Returns a list of uploaded files if the user selects CSV or TSV, or the uploaded file if the user selects XLSX. If the user does not upload any files, None is returned.

    Parameters:
        None

    Returns:
        Union[List[Any], Any]
    """
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
    """Prompts the user to select one or more sheets from the given list of sheets in an Excel file.

    The user is presented with a multiselect widget containing the given list of sheets. The selected sheets are stored in st.session_state['selected_sheets'] and returned as a list of strings.

    Args:
        sheets (List[str]): A list of sheet names to present to the user.

    Returns:
        List[str]: A list of sheet names selected by the user. If no sheets are selected, an empty list is returned.
    """

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
    """Get the database choice from the user.

    Presents the user with a selectbox containing the options "MySQL", "SQLite", and "PostgreSQL".
    Returns the selected database choice as a string.

    Parameters:
        None

    Returns:
        str: The selected database choice (one of "MySQL", "SQLite", or "PostgreSQL").
    """
    db_choice=st.selectbox("Select Database", ["MySQL", "SQLite", "PostgreSQL", ])
    return db_choice

def get_mysql_credentials() -> Dict:
    """
    Get the MySQL credentials from the user.

    Presents the user with six text input fields to enter the host, port, username, password, database, and table name for a MySQL database.

    Returns a dictionary with the MySQL credentials if all fields are filled, otherwise returns None.

    Parameters:
        None

    Returns:
        Dict: A dictionary with the MySQL credentials if all fields are filled, otherwise None.
    """
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
        return {"MySQL": {"host": host, "port": int(port), "username": user, "password": password, "database": database, "table": table}}
    else:
        
        return None

def get_sqlite_credentials() -> Dict:
    """Get the SQLite credentials from the user.

    Presents the user with two text input fields to enter the database and table name for a SQLite database.

    Returns a dictionary with the SQLite credentials if both fields are filled, otherwise returns None.

    Parameters:
        None

    Returns:
        Dict: A dictionary with the SQLite credentials if both fields are filled, otherwise None.
    """
    database = st.text_input("Database")
    table = st.text_input("Table")
    if all([database, table]):
        return {"SQLite": {"database": database, "table": table}}
    else:
        
        return None
        
def get_postgresql_credentials() -> Dict:
    """Get the PostgreSQL credentials from the user.

    Presents the user with six text input fields to enter the host, port, username, password, database, and table name for a PostgreSQL database.

    Returns a dictionary with the PostgreSQL credentials if all fields are filled, otherwise returns None.

    Parameters:
        None

    Returns:
        Dict: A dictionary with the PostgreSQL credentials if all fields are filled, otherwise None.
    """
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
        return {"PostgreSQL": {"host": host, "port": int(port), "user": user, "password": password, "database": database, "table": table}}
    else:
        
        return None


@st.dialog("Groq API Key For Voice Assistant")
def get_groq_api_key():
    """
    Presents the user with a text input field to enter their Groq API key.

    The user is prompted to enter their API key and click the "Submit" button.

    If the user enters a valid API key and clicks the "Submit" button, the API key is stored in the session state and the dialog is closed.

    If the user does not enter a valid API key and clicks the "Submit" button, the dialog remains open and the user is prompted to enter a valid API key.

    Parameters:
        None

    Returns:
        str: The Groq API key entered by the user, or None if the user did not enter a valid API key.
    """
    if 'groq_api_key' not in st.session_state:
        st.session_state['groq_api_key'] = None  # Start with None to track if key has been set

    if st.session_state['groq_api_key'] is None:
        groq_api_key = st.text_input("Enter your Groq API key", type="password")
        submit = st.button("Submit")

        if submit:
            st.session_state['groq_api_key'] = groq_api_key
            st.session_state['is_key'] = True
            st.success("Thanks for providing your Groq API key!.Close the dialog to continue")
    return st.session_state.get('groq_api_key', None)

def get_recording()-> bytes:
    """
    Record audio from the user's microphone and return the recorded audio as a bytes object.

    The user is presented with a "Start Recording" button. When the button is clicked, the microphone is enabled and the user can record audio. When the user is finished recording, they can click the "Stop Recording" button to save the recorded audio.

    The recorded audio is returned as a bytes object. If the user does not record any audio, None is returned.

    Parameters:
        None

    Returns:
        bytes: The recorded audio, or None if no audio was recorded.
    """
    recording = mic_recorder(
                        start_prompt="🎙️Start Recording",
                        stop_prompt="🛑 Stop Recording",
                        just_once=False,
                        use_container_width=False
                    )
    audio_bytes = recording['bytes'] if recording else None
    return audio_bytes