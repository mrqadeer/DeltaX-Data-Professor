import streamlit as st
from components.display_components import display_welcome_message,display_dataframes
from components.input_components import get_data_source
from src.hanlders.files_handlers import handle_uploaded_files
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
            data_source,tag =get_data_source()
            submit = st.button("Submit")
        if submit:
            with st.expander("Data", expanded=False):    
                if tag=="uploaded_files" and data_source is not None:
                    with st.spinner("Processing..."):
                        dfs=handle_uploaded_files(data_source)
                        display_dataframes(dfs)
  
                elif tag=="selected_db":
                    st.write(data_source)
        else:
            pass
delta_ai_page()
