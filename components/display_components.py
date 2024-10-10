import streamlit as st
from pandasai import Agent
import os,pathlib


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
        st.dataframe(df, use_container_width=True)
  
def display_results(agent: Agent) -> None:
    """
    Display the results of the agent's computation in Streamlit.

    This function will automatically detect the type of result from the agent and display it
    accordingly. If the result is a dataframe, it will be displayed as a table. If the result is a
    plot, it will be displayed as an image. If the result is a string, it will be displayed as a
    paragraph. If the result is a number, it will be displayed as a number.

    The function will also display the code that was executed to generate the result and an
    explanation of the code.

    If the result is a plot, it will also be saved to a file and the user will be given the option
    to download the plot as an image.

    If the result is None, an error message will be displayed.

    :param agent: The agent that generated the result
    """
    PLOT_PATH=pathlib.Path(__file__).parent.parent.joinpath('exports/charts/temp_chart.png')
    # agent.clear_memory()
    result=agent.last_result
    code=agent.last_code_executed

    if 'download' not in st.session_state:
        st.session_state['download'] = False
    if result is not None:
        
        with st.expander("Result",expanded=True):
            if result['type'] == 'string':
                # st.info(result['value'])
                st.code(result['value'],language='text')
            elif result['type'] == 'dataframe':
                st.dataframe(result['value'],use_container_width=True)
            elif result['type'] == 'plot':
                st.image(result['value'], use_column_width=True)
            elif result['type'] == 'number':
                st.code(result['value'],language='text')
                # st.info(result['value'])
        st.divider()
        with st.expander("Explanation",expanded=True):
            st.markdown(agent.explain())
        st.divider()
        with st.expander("Code",expanded=True):
            if code is not None:
                st.code(code,language='python',line_numbers=True,wrap_lines=True)
        if os.path.exists(PLOT_PATH):
            st.divider()
            with st.expander("Chart",expanded=True):
                st.image(str(PLOT_PATH), use_column_width=True)
             # Open the image file in binary mode
            with open(PLOT_PATH, "rb") as image_file:
                download_chart = st.download_button("Download Chart", image_file, "chart.png", "image/png")
            
            if download_chart or st.session_state.get('download', False):
                st.session_state['download'] = True
                
    else:
        st.error('We are unable to retrieve any result. Please check your question and try again.')