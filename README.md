# 📦 Visual QA Chatbot using Multimodal Models

A Visual QA application leveraging mutliple multimodal LLMs (Gemini 3 Pro, Llama 4, and 3.2) available at OpenRouter endpoints.
User prompting seeks to obtain model insights regarding the visual input. The app accepts JPEG, PNG, GIF, PDF and PPT/PPTX formats.

**Please Note:** *Processing the Powerpoint format may be suboptimal. Powerpoints go through a conversion process using Cloudmersive APIs.*

## Gemini 3.0 Pro Preview

- **Architecture:** Sparse Mixture-of-Experts (MoE) with native multimodal support for text, vision, and audio inputs
- **Active Parameters:** not officially disclosed - *believed* to be 15-20B
- **Inputs:** token context up to 1M
- **Outputs:** text, with token context up to 64K 
- **Knowledge Cutoff:** January 2025


## Llama 4 Maverick

- **Architecture:** Sparse Mixture-of-Experts (MoE) with native multimodal support for text, vision, and audio inputs
- **Active Parameters:** 17B
- **Inputs:** token context up to 1M
- **Outputs:** text, with token context up to 8K
- **Knowledge Cutoff:** August 2024

## Llama 3.2 Vision

- **Language Model:** Llama 3.1 base
- **Image Encoder:** ViT-H/14 - a Vision Transformer with a 'H'uge 14x14 patch size. This H/14 ViT processes visual input in 14x14 pixel blocks
- **Training:** trained with datasets containing image-text pairs (standardized with CLIP). This enables the model to learn relationships between visual info and text descriptions
- **Vision Adapter:** integrates the image encoder data (image modality) with text tokens to the LM via cross-attention. This contrasts with CLIP, which maintains a single embedding space for both modalties

### Further Reading

For further reading about:
- **Google Gemini 3 Pro Preview** visit [Google Cloud](https://console.cloud.google.com/vertex-ai/publishers/google/model-garden/gemini-3-pro-preview?pli=1)
- **Llama 4 Maverick** visit [ai.meta.com](https://ai.meta.com/blog/llama-4-multimodal-intelligence/)
- **Llama 3.2 Vision** visit [ai.meta.com](https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/)
  

## OpenRouter

[OpenRouter](https://openrouter.ai) provides a unified interface for leveraging LLMs with an API compatible with OpenAI

- Provides an endpoint with a built-in fallback API.  Alleviating the need to deal with API failures
- Integrates nicely with the ChatOpenAI class in LangChain

## Demo App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://l3vision-open-router.streamlit.app/)
