

PANDASAI_MODELS=["BambooLLM"]
OPENAI_MODELS=[
    "gpt-4",
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4-0613",
    "gpt-4-turbo",
    "gpt-4-turbo-0613",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-instruct",
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-16k-0613",
]
GOOGLE_MODLES=["gemini-1.5-pro","gemini-1.0-pro-002","gemini-1.5-flash"]
GROQ_MODELS=['llama-3.1-70b-versatile', 'llama-3.2-1b-preview', 
             'llama3-groq-8b-8192-tool-use-preview', 
             'llama-3.2-11b-vision-preview', 
             'llama3-groq-70b-8192-tool-use-preview', 
             'llama3-8b-8192', 'llama-3.2-11b-text-preview', 
             'llama-guard-3-8b', 'llama-3.1-8b-instant', 
             'llama-3.2-90b-text-preview', 'llama-3.2-3b-preview', 
             'llama3-70b-8192']
ANTROPIC_MODELS=['claude-3-5-sonnet-20240620','claude-3-sonnet-20240229','claude-3-opus-20240229','claude-3-haiku-20240307']

PROVIDERS= {
        "PandasAI": {"key":"PANDASAI_API_KEY","PandasAI":PANDASAI_MODELS,"url":"https://www.pandabi.ai/admin/api-keys"},
        "OpenAI": {"key":"OPENAI_API_KEY","OpenAI":OPENAI_MODELS,"url":"https://platform.openai.com/api-keys"},
        "Google Gemini": {"key":"GOOGLE_API_KEY","Google Gemini":GOOGLE_MODLES,"url":"https://aistudio.google.com/app/apikey"},
        "Groq": {"key":"GROQ_API_KEY","Groq":GROQ_MODELS,"url":"https://console.groq.com/keys"},
        "Antropic": {"key":"ANTROPIC_API_KEY","Antropic":ANTROPIC_MODELS,"url":"https://console.anthropic.com/settings/keys"}
    }

