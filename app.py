import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text

# 1. Specialist Cyber Station Theme (Futuristic & Intense)
def local_css():
    st.markdown("""
    <style>
    /* Futuristic Workstation Background */
    .stApp {
        background: linear-gradient(rgba(5, 10, 15, 0.9), rgba(5, 10, 15, 0.9)), 
                    url("https://r4.wallpaperflare.com/wallpaper/798/228/345/technology-alienware-keyboard-laptop-wallpaper-3920986de13a3d5be617f8df20b12fd5.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Main Headings (Futuristic 'Specialist' Style) */
    h1 {
        color: #e0f7ff !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        letter-spacing: 3px;
        text-shadow: 0 0 10px #00d2ff, 0 0 20px #00d2ff, 0 0 30px #00ff88;
    }
    
    /* Subheadings and Developer Credit */
    h2, h3, .developer-text {
        color: #00ff88 !important;
        font-family: 'Space Mono', monospace !important;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 0 8px #00ff88;
    }

    /* Normal Text & Chat Messages */
    p, span, div, label {
        color: #f0faff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        font-weight: 400;
    }
    
    code {
        color: #ff0055 !important;
        background-color: rgba(255, 0, 85, 0.1) !important;
        font-family: 'Space Mono', monospace !important;
    }
    
    /* Chat Message Styling (Sleek and Secure) */
    div[data-testid="stChatMessage"] {
        background-color: rgba(10, 20, 30, 0.85) !important;
        border: 2px solid #00d2ff;
        border-radius: 15px;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.3);
        margin-bottom: 15px;
        padding: 18px !important;
    }

    /* Chat Input Box (Modern Cyber-Tech) */
    .stChatInputContainer {
        background-color: #050a10 !important;
        border: 2px solid #00ff88 !important;
        border-radius: 30px !important;
    }
    
    .stChatInputContainer textarea {
        color: #ffffff !important;
        font-family: 'Space Mono', monospace !important;
    }

    /* Specialized Buttons Style */
    button {
        background-color: #050a10 !important;
        border: 2px solid #00ff88 !important;
        color: #00ff88 !important;
        border-radius: 25px !important;
        padding: 8px 25px !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.4s ease;
    }
    
    button:hover {
        background-color: #00ff88 !important;
        color: #050a10 !important;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.6);
        transform: scale(1.05);
    }

    /* Hide Scrollbar */
    ::-webkit-scrollbar {
        width: 0px;
        background: transparent;
    }
    </style>
    """, unsafe_allow_html=True)

# Page Configuration
st.set_page_config(page_title="VEER AI", page_icon="💻", layout="centered")
local_css()

# Header (High-Tech Design)
st.title("VEER AI")
st.markdown("<div class='developer-text'>SPECIALIST WORKSTATION</div>", unsafe_allow_html=True)
st.markdown("<div class='developer-text'>DEVELOPER: ANURAG // SECURE CONNECTION</div>", unsafe_allow_html=True)
st.write("---")

# API Configuration
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Voice Input
    st.write("🎙️ **VOICE COMMAND // INTERACT:**")
    voice_input = speech_to_text(
        start_prompt="START RECORDING",
        stop_prompt="STOP RECORDING",
        language='hi',
        key='speech'
    )

    text_input = st.chat_input("ENTER COMMAND...")
    prompt = voice_input if voice_input else text_input

    if prompt:
        with st.chat_message("user"):
            st.markdown(f"> {prompt}")
        st.session_state.messages.append({"role": "user", "content": f"> {prompt}"})

        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown("*PROCESSING COMMAND...*")
            
            try:
                # Specialist Persona Instruction
                model = genai.GenerativeModel(
                    "gemini-2.5-flash",
                    system_instruction=(
                        "Your name is 'VEER AI'. You are an extremely advanced and secure specialist AI, developed exclusively by 'ANURAG'. "
                        "You are fully loyal to ANURAG. Your communication style should be highly professional, intelligent, and incorporate a 'technical specialist' edge. "
                        "When asked about your origin, always proudly state that you are a creation of your developer and boss, Anurag."
                    )
                )
                response = model.generate_content(prompt)
                
                placeholder.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
            except Exception as e:
                placeholder.markdown(f"❌ TECHNICAL ERROR: {str(e)}")

else:
    st.error("⚠️ CRITICAL: GEMINI_API_KEY NOT FOUND. CHECK SECRETS.")
