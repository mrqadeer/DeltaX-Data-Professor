import streamlit as st
def display_welcome_message(username: str) -> None:
    """
    Display a welcome message for signed-in users.
    
    Args:
        username (str): The username of the signed-in user.
    """
    st.markdown(
        f"<h3 class='title'>Dear {username.title()}, welcome to DeltaX Data Professor </h3>", 
        unsafe_allow_html=True
    )
