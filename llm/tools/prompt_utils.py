import base64
import streamlit as st
from langchain_core.messages import HumanMessage
from langchain_core.messages.utils import count_tokens_approximately

class PromptUtils:
    """
    Utility class for handling prompt templates.
    """
    log = st.logger.get_logger(__name__)


    @staticmethod
    def encode_image(image_byte_data):
        """
        Encodes an image to a base64 string.

        Args:
            image_byte_data (byte): Byte object of the image to encode.

        Returns:
            str: Base64-encoded string of the image, or None if an error occurs.
        """    
        try:
            return base64.b64encode(image_byte_data).decode("utf-8")
        except Exception as e:
            PromptUtils.log.critical(f"Error base64 encoding image data: {e}")
            return None
    
    @staticmethod 
    def assess_token_count(message):
        """
        Checks the token count of a message.

        Args:
            message (HumanMessage): The message to check.

        Returns:
            int: The token count of the message.
        """
        try:
            token_count = count_tokens_approximately([message])
            estimated_bytes = token_count * 4 # Estimate 1 token = 4 chars
            estimated_kb = estimated_bytes / 1024
            PromptUtils.log.info(f"Prompt token count: {token_count}")
            PromptUtils.log.info(f"Estimated prompt size: {estimated_kb:.2f} KB")
        except Exception as e:
            PromptUtils.log.inform(f"Error checking token count: {e}")
    
    @staticmethod    
    def get_zshot_prompt(image_byte_data, user_prompt, mime_type="image/jpeg"):
        """
        Creates a prompt for performing VQA on a single image.

        Args:
            image_byte_data (byte): byte object of image.
            user_prompt (str): User prompt.

        Returns:
            dict or None: The user message dictionary, or None if image encoding fails.
        """
        try:
            prompt = f"You are a helpful AI assistant that analyzes images and provides detailed responses. {user_prompt}"
            message = HumanMessage(
                content=[
                    {"type": "text", "text": prompt},
                    {
                        "type": "image",
                        "source_type": "base64",
                        "data": PromptUtils.encode_image(image_byte_data),
                        "mime_type": mime_type,
                    },
                ],
            )
        except Exception as e:
            PromptUtils.log.critical(f"Error creating zero-shot prompt: {e}")
            raise RuntimeError(f"Failed to create zero-shot prompt. Please check the image content and try again! Exception: {e}")
        PromptUtils.assess_token_count(message)
        return message