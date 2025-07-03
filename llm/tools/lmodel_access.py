from langchain_openai import ChatOpenAI
import streamlit as st

class LModelAccess:
    """
    Model access object for OperRouter model operations.
    """

    
    model_repository = {
        "llama": [
            "meta-llama/llama-3.2-11b-vision-instruct:free"               #  Llama 3.2 11B Vision - Multi-modal 

        ],
    }
   

    def __init__(self, api_key=None):
        """
        Initialize the LModelAccess class.
        """
        self.log = st.logger.get_logger(__name__)
        self.log.debug("LModelAccess initialized")
        self.api_base_url = "https://openrouter.ai/api/v1"
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
            model_name=model_name
        )
        return llm

