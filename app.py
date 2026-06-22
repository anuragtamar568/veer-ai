import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text
from PIL import Image

# पेज कॉन्फ़िगरेशन
st.set_page_config(page_title="VEER AI", page_icon="💻", layout="centered")

# 1. डार्क थीम, नियॉन लेटर्स और रोबोटिक वॉयस के लिए स्क्रिप्ट
def local_css_and_js():
    # CSS फॉर डार्क नियॉन थीम
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(rgba(10, 15, 25, 0.85), rgba(10, 15, 25, 0.85)), url("https://images.unsplash.com/photo-1542831371-29b0f74f9713?q=80&w=1400&auto=format&fit=crop") !important;
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
        color: #00ff66 !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold;
        margin-top: 15px;
    }
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
    div.stLinkButton > a {
        background-color: #050a10 !important;
        color: #00ff66 !important;
        border: 2px solid #00ff66 !important;
        border-radius: 6px !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important;
        letter-spacing: 1px !important;
        box-shadow: 0 0 10px rgba(0, 255, 102, 0.3) !important;
        transition: all 0.3s ease !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 10px 20px !important;
        text-decoration: none !important;
    }
    div.stLinkButton > a:hover {
        background-color: #00ff66 !important;
        color: #050a10 !important;
        box-shadow: 0 0 15px #00ff66 !important;
    }
    ::-webkit-scrollbar {
        width: 0px;
        background: transparent;
    }
    </style>
    """, unsafe_allow_html=True)

local_css_and_js()

# रोबोटिक आवाज़ जनरेट करने वाला जावास्क्रिप्ट फंक्शन
def robot_speak(text_to_say):
    clean_text = text_to_say.replace("'", "\\'").replace("\n", " ")
    js_code = f"""
    <script>
    if ('speechSynthesis' in window) {{
        window.speechSynthesis.cancel(); // पुरानी आवाज़ रोको
        var msg = new SpeechSynthesisUtterance('{clean_text}');
        
        // रोबोटिक इफ़ेक्ट के लिए सेटिंग्स:
        msg.pitch = 0.4;  // आवाज़ को बहुत भारी (Deep) बनाने के लिए
        msg.rate = 0.85;  // थोडा धीरे बोलने के लिए ताकि रोबोट जैसा लगे
        msg
