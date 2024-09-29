import streamlit as st
from components.display_components import display_welcome_message
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

delta_ai_page()
