# src/hanlders/llm_handlers.py
from pandasai.llm import BambooLLM,GoogleGemini,LangchainLLM
from langchain_groq import ChatGroq
from langchain_openai.chat_models import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from typing import Union

def llm_handler(credentials:dict) -> Union[ChatGroq, ChatOpenAI, GoogleGemini, BambooLLM, ChatAnthropic]:
    """Get the LLM handler from the environment."""
    for provider in credentials:
        if provider == "Groq":
            
            langchain_llm=ChatGroq(model=credentials[provider]['model'],
                            temperature=credentials[provider]['temperature'],
                            api_key=credentials[provider]['api_key'])
            llm=LangchainLLM(langchain_llm=langchain_llm)
        elif provider == "OpenAI":
            langchain_llm=ChatOpenAI(model=credentials[provider]['model'],
                              temperature=credentials[provider]['temperature'],
                              api_key=credentials[provider]['api_key'])
            llm=LangchainLLM(langchain_llm=langchain_llm)
        elif provider == "Google Gemini":
            llm=GoogleGemini(model=credentials[provider]['model'],
                                     temperature=credentials[provider]['temperature'],
                                     api_key=credentials[provider]['api_key'])
        elif provider == "PandasAI":
            llm=BambooLLM(api_key=credentials[provider]['api_key'])
        elif provider == "Antropic":
            llm=ChatAnthropic(model=credentials[provider]['model'],
                              temperature=credentials[provider]['temperature'],
                              api_key=credentials[provider]['api_key'])
        else:
            raise ValueError("No LLM provider found in environment")
    return llm