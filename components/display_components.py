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

def display_dataframes(dfs: list) -> None:
    """
    Display dataframes in Streamlit.

    Args:
        dfs (list): A list of dataframes to display.
    """
    for i, df in enumerate(dfs):
        st.info(f"Dataframe {i+1} with {df.shape[0]} rows and {df.shape[1]} columns")
        st.dataframe(df.head(10), use_container_width=True)