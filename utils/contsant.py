# utils/contsant.py
from utils.get_models import (
    get_provider
)

PROVIDERS= {
        "PandasAI": {"key":"PANDASAI_API_KEY","url":"https://www.pandabi.ai/admin/api-keys"},
        "OpenAI": {"key":"OPENAI_API_KEY","url":"https://platform.openai.com/api-keys"},
        "Google Gemini": {"key":"GOOGLE_API_KEY","url":"https://aistudio.google.com/app/apikey"},
        "Groq": {"key":"GROQ_API_KEY","url":"https://console.groq.com/keys"},
        "Antropic": {"key":"ANTROPIC_API_KEY","url":"https://console.anthropic.com/settings/keys"}
    }

