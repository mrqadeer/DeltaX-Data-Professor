import streamlit as st

from components.display_components import (display_welcome_message, 
                                           display_dataframes,
                                           display_results,
                                           display_sign_in_button)
from components.input_components import (get_uploaded_files, 
                                         get_database,
                                         get_database_credentials,
                                         get_recording,get_groq_api_key)

from src.hanlders.files_handlers import handle_uploaded_files
from src.hanlders.database_hanlders import handle_database_connection
from src.hanlders.chatbot_handlers import chatbot_handler
from src.hanlders.transcription import transcribe_audio




def delta_ai_page() -> None:
    """
    The main page for the DeltaX Data Professor application.
    """
    # Check if the user is signed in
    if not st.session_state.get('signed_in', False):
        st.error("Please sign in to get in touch with DeltaX Data Professor.")
        st.markdown("""Click on the "Sign In" button to get started.""")
        display_sign_in_button()
        return

    # Welcome the user if they are signed in
    username = st.session_state.get('username', 'User')
    display_welcome_message(username)
    st.divider()

    # Initialize session state variables if they don't exist
    if 'file_uploaded' not in st.session_state:
        st.session_state['file_uploaded'] = False
    if 'db_connected' not in st.session_state:
        st.session_state['db_connected'] = False
    if 'process' not in st.session_state:
        st.session_state['process'] = False
    if 'dfs' not in st.session_state:
        st.session_state['dfs'] = None
    if 'voice' not in st.session_state:
        st.session_state['voice'] = False
    if 'is_key' not in st.session_state:
        st.session_state['is_key'] = False

    # Initialize local variables to None
    uploaded_files = None
    db_credentials = None

    # Sidebar: Select file upload or database connection
    with st.sidebar:
        source = st.selectbox("Select Source", ["Upload File", "Connect to Database"], index=0)

        if source == 'Upload File':
            st.session_state['dfs'] = None
            uploaded_files = get_uploaded_files()
            if uploaded_files:
                st.session_state['file_uploaded'] = True
            else:
                st.warning("Please upload a file to proceed")

        elif source == 'Connect to Database':
            st.session_state['dfs'] = None
            db_choice = get_database()
            db_credentials = get_database_credentials(db_choice=db_choice)
            if db_credentials:
                st.session_state['db_connected'] = True
            else:
                st.warning("Please connect to a database to proceed")

        # Process button (single button for both actions)
        process = st.button("Process")
        
        if process:
            st.session_state['process'] = True

        # Handle processing based on whether a file is uploaded or a database is connected
        if st.session_state['process']:
            if st.session_state['file_uploaded'] and uploaded_files is not None:
                st.session_state['dfs'] = handle_uploaded_files(uploaded_files)
            elif st.session_state['db_connected'] and db_credentials is not None:
                connector = handle_database_connection(db_credentials)
                st.session_state['dfs'] = [connector.execute()]

    # Display dataframes if available
    if st.session_state['dfs'] is not None:
        with st.expander("Data Preview"):
            display_dataframes(st.session_state['dfs'])
        
        cols = st.columns([2, 2, 6], gap="small")
        # st.session_state.clear()
        with cols[0]:
            voice_query = st.toggle("Voice Query", key="voice_query")
            
            if voice_query or st.session_state.get('voice', False):
                
                st.session_state['voice'] = True
                
                # Check if the API key is not already set
                if st.session_state.get('groq_api_key') is None:
                    get_groq_api_key()  # Only open the dialog if the key is not already set
                    st.session_state['is_key'] = True
        
        prompt=None          
        if st.session_state['is_key']: 
            with cols[1]:
                audio_bytes = get_recording()
                if audio_bytes is not None:
                    audio_prompt=transcribe_audio(audio_bytes)
                    if audio_prompt:
                        prompt=audio_prompt
                    
        
        with cols[2]:
            text_prompt = st.chat_input("Ask a question about the data")
        
            if text_prompt:
                prompt=text_prompt

        if prompt:
            st.markdown(
                """
                <div style='text-align: left;'>
                    <span style='color: yellow; padding-bottom: 10px;'>Question</span>
                </div>
                """, 
                unsafe_allow_html=True
            )

            st.code(prompt,language="text",wrap_lines=True)
            with st.spinner("Generating response..."):
                agent = chatbot_handler(dfs=st.session_state['dfs'], query=prompt)
                display_results(agent)


# Calling the function to display the page
delta_ai_page()
