# src/hanlders/chatbot_handlers.py

import streamlit as st
import pandas as pd
from pandasai import SmartDatalake,Agent
from pandasai.responses import StreamlitResponse
from .llm_handlers import llm_handler
from typing import List,Tuple
def chatbot_handler(dfs: List[pd.DataFrame],query: str) -> SmartDatalake:
    """Handle chatbot queries using PandasAI.

    Args:
        query (str): The query to be processed.
        provider (str): The provider to be used for processing the query.
        api_key (str): The API key to be used for authentication.
        model (str): The model to be used for processing the query.
        temperature (float, optional): The temperature to be used for processing the query. Defaults to 0.7.

    Returns:
        str: The processed query.
    """
    # Use the factory to get the correct LLM handler
    llm = llm_handler(credentials=st.session_state['credentials'])

    
    config={'llm':llm,
            'response_parser':StreamlitResponse,
            }
    
    agent=Agent(dfs=dfs,config=config)
    
    agent.chat(query)
    return agent