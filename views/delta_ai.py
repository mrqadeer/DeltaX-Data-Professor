import streamlit as st
from components.display_components import display_welcome_message,display_dataframes
from components.input_components import get_data_source,get_databases_credentials
from src.hanlders.files_handlers import handle_uploaded_files
from src.hanlders.database_hanlders import MySQLConnector,PostgresConnector
from pandasai.connectors import SqliteConnector
def show_sign_in_button() -> None:
    """
    Display the sign-in button and redirect users to the login page when clicked.
    """
    # Define columns for button layout
    cols = st.columns([3.5, 2, 2])

    # Center the button in the second column
    with cols[1]:
        if st.button("Sign In"):
            # Redirect to the sign-in page when the button is clicked
            st.switch_page("views/credentials.py")


def delta_ai_page() -> None:
    """
    The main page for the DeltaX Data Professor application.
    It checks whether a user is signed in and displays the appropriate content.
    """
    # Check if the user is signed in
    if not st.session_state.get('signed_in', False):
        st.error("Please sign in to get in touch with DeltaX Data Professor.")
        st.markdown("""Click on the "Sign In" button to get started.""")

        # Display the sign-in button
        show_sign_in_button()
    else:
        # Welcome the user if they are signed in
        username = st.session_state.get('username', 'User')
        display_welcome_message(username)
        st.divider()
        
        with st.expander("Data Source", expanded=True):
            cols=st.columns(2)
            
            with cols[0]:
                
                uploaded_files =get_data_source(source='file')
                submit = st.button("Submit", key="submit")
                
                if submit:        
                    with st.spinner("Processing..."):
                        dfs=handle_uploaded_files(uploaded_files)
                        display_dataframes(dfs)
            with cols[1]:
                
                db_choice = get_data_source(source='database')
                credentials=get_databases_credentials(db_choice)
                connect=st.button("Connect", key="connect")
                if connect:
                    with st.spinner("Processing..."):
                        for db in credentials:
                            match db:
                                case 'MySQL':
                                    connector = MySQLConnector(**credentials[db])
                                    connector.connect()
                                    st.success("Connected to MySQL")
                                case 'SQLite':
                                    connector = SqliteConnector(config=credentials[db])
                                    st.success("Connected to SQLite")
                                case 'PostgreSQL':
                                    connector = PostgresConnector(**credentials[db])
                                    connector.connect()
                                    st.success("Connected to PostgressSQL")
                                case _:
                                    st.error("Database not supported")

delta_ai_page()
