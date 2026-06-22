import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text

# पेज कॉन्फ़िगरेशन (यह सबसे ऊपर होना जरूरी है)
st.set_page_config(page_title="VEER AI", page_icon="💻", layout="centered")

# 1. डार्क थीम, नियॉन लेटर्स और असिस्टेंट बटन्स के लिए CSS
def local_css():
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(rgba(10, 15, 25, 0.85), rgba(10, 15, 25, 0.85)), 
                    url("https://images.unsplash.com/photo-1542831371-29b0f74f9713?q=80&w=1400&auto=format&fit=crop") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }
    
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    
    h1 {
        color: #6bf2ff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        font-weight: 300 !important;
        text-transform: uppercase;
        letter-spacing: 5px;
        text-shadow: 0 0 10px rgba(107, 242, 255, 0.8), 0 0 25px rgba(107, 242, 255, 0.5);
        margin-bottom: 5px !important;
    }
    
    .developer-text {
        color: #00ff66 !important;
        font-family: 'Courier New', Courier, monospace !important;
        font-weight: bold;
        letter-spacing: 2px;
        font-size: 14px;
        text-shadow: 0 0 8px rgba(0, 255, 102, 0.6);
        margin-top: 2px !important;
        margin-bottom: 2px !important;
    }

    div[data-testid="stChatMessage"] {
        background-color: rgba(8, 20, 30, 0.9) !important;
        border: 2px solid #00d2ff;
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.4);
        margin-bottom: 15px;
        padding: 15px !important;
    }

    p, span, div, label {
        color: #ffffff !important;
        font-family: 'Segoe UI', sans-serif !important;
    }
    
    .stChatInputContainer {
        background-color: rgba(5, 10, 15, 0.95) !important;
        border: 2px solid #00d2ff !important;
        border-radius: 8px !important;
    }
    
    .stChatInputContainer textarea {
        color: #ffffff !important;
    }

    .voice-label {
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold;
        margin-top: 15px;
    }

    /* मुख्य माइक और सबमिट बटन्स */
    button {
        background-color: #050a10 !important;
        border: 1px solid #00d2ff !important;
        color: #00d2ff !important;
        border-radius: 4px !important;
    }
    
    button:hover {
        background-color: #00d2ff !important;
        color: black !important;
        box-shadow: 0 0 10px #00d2ff;
    }

    /* 🔗 असिस्टेंट के स्पेशल नियॉन लिंक बटन का स्टाइल */
    .action-link {
        display: inline-block;
        padding: 10px 20px;
        background-color: #050a10;
        color: #00ff66 !
