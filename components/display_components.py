import streamlit as st
from pandasai import Agent
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


def display_sign_in_button() -> None:
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

def display_dataframes(dfs: list) -> None:
    """
    Display dataframes in Streamlit.

    Args:
        dfs (list): A list of dataframes to display.
    """
    for i, df in enumerate(dfs):
        st.info(f"Dataframe {i+1} with {df.shape[0]} rows and {df.shape[1]} columns")
        st.dataframe(df.head(10), use_container_width=True)
        
def display_results(agent: Agent) -> None:
    result=agent.last_result
    code=agent.last_code_executed
    
    if result is not None:
        cols=st.columns(2,gap='small',vertical_alignment='center')
        with cols[0]:
            if result['type'] == 'string':
                st.info(result['value'])
            elif result['type'] == 'dataframe':
                st.dataframe(result['value'],use_container_width=True)
            elif result['type'] == 'plot':
                st.image(result['value'], use_column_width=True)
            elif result['type'] == 'number':
                st.info(result['value'])
        with cols[1]:
            with st.expander("Code",expanded=True):
                if code is not None:
                    st.code(code,language='python')
        with st.expander("Explanation",expanded=True):
            st.markdown(agent.explain())
    else:
        st.error('We are unable to retrieve any result. Please check your question and try again.')