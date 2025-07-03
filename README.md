# 📦 Visual QA Chatbot using Llama 3.2 Vision

A Visual QA application leveraging Meta's Llama 3.2 Vision 11B multi-modal language model (MMLM) at an OpenRouter endpoint.
User prompting seeks to obtain model insights regarding the visual input.  

## Llama 3.2 Vision

- **Language Model:** Llama 3.1 base
- **Image Encoder:** ViT-H/14 - a Vision Transformer with a 'H'uge 14x14 patch size. This H/14 ViT processes visual input in 14x14 pixel blocks
- **Training:** trained with datasets containing image-text pairs (standardized with CLIP). This enables the model to learn relationships between visual info and text descriptions
- **Vision Adapter:** integrates the image encoder data (image modality) with text tokens to the LM via cross-attention. This contrasts with CLIP, which maintains a single embedding space for both modalties

### Further Reading

For some further reading on Llama 3.2 visit [ai.meta.com](https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/)

## OpenRouter

[OpenRouter](https://openrouter.ai) provides a unified interface for leveraging LLMs with an API compatible with OpenAI

- Provides an endpoint with a built-in fallback API.  Alleviating the need to deal with API failures
- Integrates nicely with ChatOpenAI class in LangChain

## Demo App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://l3vision-open-router.streamlit.app/)
