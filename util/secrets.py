from enum import Enum
import streamlit as st


class Secrets(Enum):
    OAUTH_CLIENT_ID = st.secrets.oauth_client_id
    OAUTH_CLIENT_SECRET = st.secrets.oauth_client_secret
    OPENROUTER_API_KEY = st.secrets.openrouter_api_key
    CLOUDMERSIVE_API_KEY = st.secrets.cloudmersive_api_key
    