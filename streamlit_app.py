import os, time, logging, json, base64
import streamlit as st
from util.secrets import Secrets 
from llm.tools.lmodel_access import LModelAccess
from llm.tools.image_tools import ImageTools
from llm.tools.prompt_utils import PromptUtils
from streamlit_oauth import OAuth2Component
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit_js_eval import streamlit_js_eval


app_name = "VQA Chatbot"
init_model = "google/gemini-3-pro-preview"
local = True

app_dns = "http://localhost:8502/" if local else "https://l3vision-open-router.streamlit.app/"
log = st.logger.get_logger(__name__)
log.info(f"{app_name}app_dns: {app_dns}")

lma = LModelAccess(app_name, app_dns, Secrets.OPENROUTER_API_KEY.value)
image_tools = ImageTools()
models = lma.get_all_models()
default_model = lma.get_model_by_id(init_model)
default_index = models.index(default_model)

# supported file types
ENABLED_FILES_TYPES = ["jpeg", "jpg", "png", "gif", "pdf", "pptx", "ppt"]
PDF_MIME_TYPE = "application/pdf"
PPTX_MIME_TYPE = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
sb_initial_state = "expanded"

avatar_lkp = ({
    "Male" : "images/man.png",
    "Female" : "images/woman.png",
    "Hacker" : "images/hacker.png",
})
css = '''
    <style>
       [data-testid='stFileUploader'] {
           position: fixed;
           bottom: 100px;
           width: 40rem;
           padding: 10px;
        }
       [data-testid='stChatInput'] {
            width: 40rem;
            background-color: #f0f0f0;
            color: #333;
            padding: 1px;
            font-size: 12px;
        }
    </style>
    '''
def app_setup():
    st.set_page_config(
        page_title=app_name,
        page_icon=":earth_americas:",
        layout="wide",
        initial_sidebar_state=sb_initial_state,
    )
    init_sidebar()

def init_sidebar():
    with st.sidebar.expander(":blue[Chat Settings]", expanded=True):
        selected_model = st.selectbox("Model:", 
                                      models, key="active_model", 
                                      help="Choose an Open Source Model", 
                                      on_change=model_change,
                                      index=default_index
                                      )
        st.write(f"Active Model:  ***{selected_model}***")
        st.session_state.llm = lma.get_llm(selected_model, temperature=0.0)

        st.radio("Avatar:", 
            options=["Male", "Female", "Hacker"], 
            index=0, 
            horizontal=True,
            key="active_avatar",
            help="Choose your avatar",
            on_change=avatar_change,
        )
        st.session_state.user_avator = avatar_lkp[st.session_state.active_avatar]

def avatar_change():
    """
    Callback function to handle avatar change in the sidebar.
    """
    log.info(f"avatar_change to => {st.session_state.active_avatar}")
    # Update avatar based on user selection
    st.session_state.user_avator = avatar_lkp[st.session_state.active_avatar]

def model_change():    
    """
    Callback function to handle model change in the sidebar.
    """
    log.info(f"model_change to => {st.session_state.active_model}")
    # Reinitialize llm with chosen model
    st.session_state.llm = lma.get_llm(st.session_state.active_model, temperature=0.0) 

def get_session_id():
    session_id = get_script_run_ctx().session_id
    return session_id

def get_response(llm, img_byte_data, user_prompt, mime_type, session_id):             
    """
    Generate response from the VLM using the base64 encoded image, user prompt, mime type and session ID.
    Args:
        llm (ChatOpenAI): The LLM instance.
        encoded_image (str): Base64 encoded image data.
        user_prompt (str): The user's input prompt.
        session_id (str): The session ID for tracking.
    Returns:
        str: The generated response from the LLM.
    """
    prompt = PromptUtils.get_zshot_prompt(img_byte_data, user_prompt, mime_type)
    #chain = prompt | llm
    messages = llm.invoke([prompt])
    return messages.content

def get_user_info(id_token):
    """
    Get user information from the JWT ID token.
    Args:
        id_token (str): The JWT ID token containing claims about a user's identity.
    Returns:
        email (str): Authenticated User email address.
    """
    # verify signature for security
    payload = id_token.split(".")[1]
    # add padding to the payload, if required
    payload += "=" * (-len(payload) % 4)
    payload = json.loads(base64.b64decode(payload))
    email = payload["email"]
    return email

AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
# exchange authorization code for an access token
TOKEN_URL = "https://oauth2.googleapis.com/token"
# revoke the access token when user logs out
REVOKE_URL = "https://oauth2.googleapis.com/revoke"
REDIRECT_URI = app_dns
SCOPE = "openid email profile"

oauth2 = OAuth2Component(Secrets.OAUTH_CLIENT_ID.value, 
                         Secrets.OAUTH_CLIENT_SECRET.value, 
                         AUTHORIZATION_URL, 
                         TOKEN_URL, 
                         TOKEN_URL, 
                         REVOKE_URL)

# ------------------------
# 
#       Main App
# 
# ------------------------
def main():
    bot_avator = "images/chat-bot.png"
    
    if 'token' not in st.session_state:
        result = oauth2.authorize_button("Continue with Google", 
                                         REDIRECT_URI, SCOPE, 
                                         icon="data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' viewBox='0 0 48 48'%3E%3Cdefs%3E%3Cpath id='a' d='M44.5 20H24v8.5h11.8C34.7 33.9 30.1 37 24 37c-7.2 0-13-5.8-13-13s5.8-13 13-13c3.1 0 5.9 1.1 8.1 2.9l6.4-6.4C34.6 4.1 29.6 2 24 2 11.8 2 2 11.8 2 24s9.8 22 22 22c11 0 21-8 21-22 0-1.3-.2-2.7-.5-4z'/%3E%3C/defs%3E%3CclipPath id='b'%3E%3Cuse xlink:href='%23a' overflow='visible'/%3E%3C/clipPath%3E%3Cpath clip-path='url(%23b)' fill='%23FBBC05' d='M0 37V11l17 13z'/%3E%3Cpath clip-path='url(%23b)' fill='%23EA4335' d='M0 11l17 13 7-6.1L48 14V0H0z'/%3E%3Cpath clip-path='url(%23b)' fill='%2334A853' d='M0 37l30-23 7.9 1L48 0v48H0z'/%3E%3Cpath clip-path='url(%23b)' fill='%234285F4' d='M48 48L17 24l-4-3 35-10z'/%3E%3C/svg%3E"
                                         )
        if result:
            st.session_state.token = result.get('token')
            log.debug(st.session_state.token)
            # decode JWT id_token: contains user auth info (email)
            id_token = st.session_state.token.get("id_token")
            st.session_state.auth_email = get_user_info(id_token)
            st.rerun()
    else:
        log.info(f"User {st.session_state.auth_email} is already authenticated with Google OAuth2")
        session_id = get_session_id()
        log.info(f"Created Session ID: {session_id}")
        app_setup()
        viewport_height = streamlit_js_eval(js_expressions='window.parent.innerHeight', key='HEIGHT', want_output=True)
        viewport_width = streamlit_js_eval(js_expressions='window.parent.innerWidth', key='WIDTH', want_output=True)
        
        if viewport_height is None:
            log.error("Failed to retrieve viewport height. Defaulting to 800px")
            viewport_height = 800
        if viewport_width is None:
            log.error("Failed to retrieve viewport width. Defaulting to 800px")
            viewport_width = 800
        
        log.debug(f"Viewport height: {viewport_height}")
        log.debug(f"Viewport width: {viewport_width}")
        container_height_px = int(viewport_height * 0.4)
        warning_message_px = int(viewport_width * 0.7)
    
        if "messages" not in st.session_state:
            st.session_state.messages = []
        warning_placeholder = st.empty() # container for dynamic warnings
        
        if "active_model" in st.session_state:
            log.debug(f"active_model set in session => {st.session_state.active_model}")
            assert "llm" in st.session_state, "llm not set in session state!"

            log.info(f"container_height_px: {container_height_px}")
            message_container = st.container(height=container_height_px if container_height_px > 0 else None)
            with message_container:
                # Display chat messages from history
                for message in st.session_state.messages:
                    if message["role"] == "user":
                        with st.chat_message("user", avatar=st.session_state.user_avator):
                            st.markdown(message["content"])
                    else:
                        with st.chat_message("assistant", avatar=bot_avator):
                            st.markdown(message["content"])

            # Display file uploader and chat input
            st.markdown(css, unsafe_allow_html=True) 
            if ((uploaded_file := st.file_uploader("Choose a file", type=ENABLED_FILES_TYPES)) and 
                (prompt := st.chat_input("Describe this image"))):
        
                # Read file as bytes:
                mime_type = uploaded_file.type
                log.debug(f"Uploaded file mime_type: {mime_type}")
                if mime_type == PDF_MIME_TYPE:
                    log.debug("PDF document requires conversion to image")
                    byte_data = image_tools.pdf_to_jpeg(uploaded_file.getvalue())
                    mime_type = "image/jpeg"  # Reset: JPEG image
                elif mime_type == PPTX_MIME_TYPE:
                    log.debug("PPTX document requires conversion to image. Checking file size...")
                    file_size = uploaded_file.size
                    if file_size > 3 * 1024 * 1024:
                        log.error("PPTX file size is larger than the 3MB limit.")
                        with warning_placeholder:
                            st.warning("""
                                The uploaded Presentation is larger than the 3MB limit imposed by the API for converting to images!\n
                                Please remove it and then upload a smaller presentation size or convert it to PDF first.
                            """, icon="⚠️", width=warning_message_px)
                        return
                    byte_data = image_tools.pptx_to_jpeg(Secrets.CLOUDMERSIVE_API_KEY.value, uploaded_file.getvalue())
                    mime_type = "image/jpeg"  # Reset: JPEG image
                else:
                    byte_data = uploaded_file.getvalue()
                    #encoded_image = base64.b64encode(byte_data).decode('utf-8')
            
                # Add to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})
            
                with message_container:
                    with st.chat_message("user", avatar=st.session_state.user_avator):
                        st.markdown(prompt)

                    try:
                        # Get llm response
                        response = get_response(st.session_state.llm, byte_data, 
                                                prompt, mime_type, session_id)
                        # Add to chat history
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        with st.chat_message("assistant", avatar=bot_avator):
                            st.markdown(response)
                    except Exception as err:
                        log.error(f"{type(err)}: Error generating LLM response: {err}")
                        if type(err).__name__ == "RateLimitError":
                            st.exception(f"""
                               << Rate Limits >> have been exceeded on OpenRouter model endpoint: {st.session_state.active_model}
                                Sorry for the inconvenience! Please try again later. 
                                Exception: {err}
                            """)
                        else:
                            st.exception(f"Failed to generate LLM response! Exception: {err}")
                      
# end main()


if __name__ == "__main__":
    main()