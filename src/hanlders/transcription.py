# Function to send audio bytes to Groq for transcription
import io
import streamlit as st
from groq import Groq
import groq
def transcribe_audio(audio_bytes,api_key, model="whisper-large-v3"):
    
    """
    Sends audio bytes to Groq for transcription.

    Args:
        audio_bytes (bytes): Raw audio bytes to be transcribed
        model (str, optional): Model to use for transcription. Defaults to "whisper-large-v3"

    Returns:
        str: Transcription of the audio

    Raises:
        groq.AuthenticationError: If Groq API key authentication fails
        groq.APIConnectionError: If Groq API connection fails
        groq.APIStatusError: If Groq API returns an error status
        groq.APIError: If Groq API returns an error response
        Exception: If any other error occurs
    """
    # Convert audio bytes to a file-like object using io.BytesIO
    try:
        client = Groq(api_key=api_key)
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = "recorded_audio.wav"  # Assign a name with the appropriate extension

        # Send the audio file to Groq API for translation/transcription
        translation = client.audio.translations.create(
            file=("recorded_audio.wav", audio_file.read()),  # Pass the audio file as expected by the API
            model=model,  # Model to use for transcription
            response_format="json",  # Get response in JSON format
            temperature=0.3  # Optional, adjust the temperature for creative responses if needed
        )

        # Return the transcription text
        return translation.text
    except groq.AuthenticationError as e:
        st.error(f"AuthenticationError: {e.body.get('error').get('message')}")
    except groq.APIConnectionError as e:
        st.error(f"APIConnectionError: {e.body.get('error').get('message')}")
    except groq.APIStatusError as e:
        st.error(f"APIStatusError: {e.body.get('error').get('message')}")
    except groq.APIError as e:
        st.error(f"APIError: {e.body.get('error').get('message')}")
    except Exception as e:
        st.error(f"An error occurred: {e}")