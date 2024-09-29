# utils/get_models.py
import openai
import groq
import streamlit as st
import google.generativeai as google
from openai import (
    OpenAIError,
    APIStatusError,
    RateLimitError,
    APITimeoutError,
    BadRequestError,
    APIConnectionError,
    AuthenticationError,
    InternalServerError,
)

class ModelProvider:
    """Base class for all model providers.

    This class defines the interface for retrieving models from various AI service providers.
    Subclasses should implement the `get_models` method.
    """

    def __init__(self, api_key: str) -> None:
        """Initialize the provider with the given API key.

        Args:
            api_key (str): The API key for accessing the provider's services.
        """
        self.api_key = api_key

    def get_models(self) -> list[str]:
        """Retrieve a list of models from the provider.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Subclasses should implement this method.")


class PandasAIProvider(ModelProvider):
    """Provider for the PandasAI models."""

    def get_models(self) -> list[str]:
        """Get the list of models available in PandasAI.

        Returns:
            list[str]: A list containing the available models.
        """
        return ["BambooLLM"]


class OpenAIProvider(ModelProvider):
    """Provider for the OpenAI models."""

    def get_models(self) -> list[str]:
        """Get the list of text chat models available in OpenAI.

        Returns:
            list[str]: A list containing the text chat model IDs.

        Raises:
            APIConnectionError: If there is a connection error.
            AuthenticationError: If the authentication fails.
            BadRequestError: If the request is malformed.
            RateLimitError: If the rate limit is exceeded.
            InternalServerError: If there is an internal server error.
            APIStatusError: If there is a status error.
            APITimeoutError: If the request times out.
            OpenAIError: For other OpenAI-related errors.
        """
        try:
            client = openai.Client(api_key=self.api_key)
            models = client.models.list().to_dict()
            text_chat_models = [
                model['id'] for model in models['data']
                if any(keyword in model['id'] for keyword in ['gpt', 'davinci', 'turbo'])
            ]
            return text_chat_models
        except (APIConnectionError, AuthenticationError, BadRequestError, 
                RateLimitError, InternalServerError, APIStatusError, 
                APITimeoutError, OpenAIError) as e:
            st.error(f"{e.body.get('message')}")
            return []  # Return an empty list in case of error
        except Exception as e:
            st.error(f"An unexpected error occurred in OpenAI: {e}")
            return []


class GoogleGeminiProvider(ModelProvider):
    """Provider for the Google Gemini models."""

    def get_models(self) -> list[str]:
        """Get the list of Gemini models available in Google.

        Returns:
            list[str]: A list containing the available Gemini models.

        Raises:
            Exception: For any errors that occur while retrieving models.
        """
        try:
            google.configure(api_key=self.api_key)
            models = google.list_models()
            gemini_models = [
                model.name.split("/")[1] for model in models
                if "gemini" in model.name and "vision" not in model.name
            ]
            return gemini_models
        except Exception as e:
            st.error(f"An error occurred in Google Gemini: {e}")
            return []


class GroqProvider(ModelProvider):
    """Provider for the Groq models."""

    def get_models(self) -> list[str]:
        """Get the list of models available in Groq.

        Returns:
            list[str]: A list containing the available Groq model IDs.

        Raises:
            groq.AuthenticationError: If authentication fails.
            groq.APIConnectionError: If there is a connection error.
            groq.APIStatusError: If there is a status error.
            groq.APIError: For other Groq-related errors.
            Exception: For any other errors.
        """
        try:
            client = groq.Client(api_key=self.api_key)
            models = client.models.list().data
            return [
                model.id for model in models
                if model.id not in ['whisper-large-v3', 'distil-whisper-large-v3-en']
            ]
        except (groq.AuthenticationError, groq.APIConnectionError, 
                groq.APIStatusError, groq.APIError) as e:
            st.error(f"{e.body.get('error').get('message')}")
            return []  # Return an empty list in case of error
        except Exception as e:
            st.error(f"An error occurred in Groq: {e}")
            return []


class AnthropicProvider(ModelProvider):
    """Provider for the Anthropic models."""

    def get_models(self) -> list[str]:
        """Get the list of available models from Anthropic.

        Returns:
            list[str]: A list containing the available Anthropic models.
        """
        return [
            'claude-3-5-sonnet-20240620',
            'claude-3-sonnet-20240229',
            'claude-3-opus-20240229',
            'claude-3-haiku-20240307'
        ]


def get_provider(provider_name: str, api_key: str) -> ModelProvider | None:
    """Retrieve the appropriate model provider class based on the provider name.

    Args:
        provider_name (str): The name of the provider.
        api_key (str): The API key for accessing the provider's services.

    Returns:
        ModelProvider | None: An instance of the corresponding provider class, or None if not found.
    """
    provider_map = {
        "PandasAI": PandasAIProvider,
        "OpenAI": OpenAIProvider,
        "Google Gemini": GoogleGeminiProvider,
        "Groq": GroqProvider,
        "Antropic": AnthropicProvider
    }
    
    provider_class = provider_map.get(provider_name)
    if provider_class:
        return provider_class(api_key)
    else:
        st.error(f"Unknown provider: {provider_name}")
        return None


def main() -> None:
    """Main function to execute the model provider retrieval.

    This function checks for the API key and retrieves models from the specified provider.
    """
    api_key = "OPENAI_API_KEY"
    if not api_key:
        print("API key is not set.")
        return

    provider_name = "OpenAI"  # Change this to select different providers.
    provider = get_provider(provider_name, api_key)

    if provider:
        models = provider.get_models()
        st.write(models)


if __name__ == "__main__":
    main()
