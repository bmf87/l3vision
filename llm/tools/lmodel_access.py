from langchain_openai import ChatOpenAI
import streamlit as st

class LModelAccess:
    """
    Model access object for OperRouter model operations.
    """

    
    model_repository = {
        "llama": [
            "meta-llama/llama-3.2-11b-vision-instruct",               #  Llama 3.2 11B Vision - Multi-modal 
            "meta-llama/llama-4-maverick",                            # Llama 4 Maverick - Multi-modal
        ],
        "google": [
            "google/gemini-3-pro-preview"                             # Gemini 3.0 Pro Preview - Multi-modal
        ]
    }
   

    def __init__(self, app_name, app_dns, api_key=None):
        """
        Initialize the LModelAccess class.
        """
        self.log = st.logger.get_logger(__name__)
        self.app_name = app_name
        self.app_dns = app_dns
        self.api_base_url = "https://openrouter.ai/api/v1"
        self.log.debug("LModelAccess initialized for app: %s", self.app_name)
        if api_key is None:
            self.log.critical("OpenRouter API key was not provided!")
            raise ValueError("OpenRouter API key must be provided!")
        self.api_key = api_key


    
    def get_model_by_provider(self, provider):
        """
        Get the model Ids by provider.

        Args:
            provider (str): The name of the provider (e.g., 'nvidia', 'deepseek').

        Returns:
            list: A list of model Ids for the specified provider.
        """
        if provider in self.model_repository:
            return self.model_repository[provider]
        else:
            raise ValueError(f"Provider '{provider}' not found in model repository.")
    
    def get_model_by_id(self, model_id):
        models = self.get_all_models()
        try:
            index = models.index(model_id)
        except ValueError:
            raise ValueError(f"Model '{model_id}' not found in model repository.")
        return models[index]
    

    def get_all_models(self):
        models = list()
        for key in self.model_repository:
            models.extend(self.get_model_by_provider(key))
        return models 
            
    
    def get_llm(self, model_name, temperature=0.0):
        """
        Get the LLM instance for the specified model name.

        Args:
            model_name (str): The name of the model.
            temperature (float): The temperature for the model. Default is 0.0.

        Returns:
            ChatOpenAI: An instance of the ChatOpenAI class.
        """
        llm = ChatOpenAI(
            temperature=temperature,
            openai_api_key=self.api_key,
            openai_api_base=self.api_base_url,
            model_name=model_name,
            default_headers={
                "X-Title": self.app_name,
                "HTTP-Referer": self.app_dns
            },
        )
        return llm

