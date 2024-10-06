# src/hanlders/chatbot_handlers.py

import streamlit as st
import pandas as pd
from pandasai import SmartDatalake,Agent
from pandasai.responses import StreamlitResponse
from .llm_handlers import llm_handler
from typing import List,Tuple
def chatbot_handler(dfs: List[pd.DataFrame],query: str) -> Agent:
    """
    Create an Agent that can process a query given a list of Pandas DataFrames.
    
    Parameters:
        dfs (List[pd.DataFrame]): A list of Pandas DataFrames that the Agent will use to answer the query.
        query (str): The query to be answered by the Agent.
    
    Returns:
        Agent: The created Agent.
    """
    llm = llm_handler(credentials=st.session_state['credentials'])

    
    config={'llm':llm,
            'response_parser':StreamlitResponse,
            }
    
    agent=Agent(dfs=dfs,config=config)
    
    agent.chat(query)
    return agent