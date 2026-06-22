import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text
import streamlit.components.v1 as components
from PIL import Image
import numpy as np
import cv2
import os
import time

# 1. पेज कॉन्फ़िगरेशन और हाई-विजिबिलिटी थीम (बिल्कुल पहले जैसा)
st.set_page_config(page_title="VEER AI // BIO_VISION_OS", page_icon="👁️", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(rgba(5, 10, 15, 0.96), rgba(5, 10, 15, 0.96)), 
                    url("https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1400&auto=format&fit=crop") !important; 
        background-size: cover !important; background-position: center !important; background-attachment: fixed !important;
    }
    h1 {color: #00ff66 !important; font-family: monospace; font-weight: bold; text-transform: uppercase; letter-spacing: 4px; text-shadow: 0 0 15px #00ff66;}
    .dev-text {color: #00d2ff !important; font-family: monospace; font-weight: bold; letter-spacing: 2px;}
    
    /* Lock Screen Styling */
    .lock-container { text-align: center; margin-top: 30px; }
    .hacker-eye { font-size: 100px; color: #00ff66; text-shadow: 0 0 25px #00ff66; animation: pulse 2s infinite; }
    .status-text { color: #ff3333; font-family: monospace; font-size: 18px; font-weight: bold; letter-spacing: 3px; margin-bottom: 20px; }
    
    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.05); opacity: 1; }
        100% { transform: scale(1); opacity: 0.8; }
    }
    
    div[data-testid="stChatMessage"] {
        background-color: rgba(5, 15, 10, 0.95) !important; 
        border: 2px solid #00ff66; 
        border-radius: 12px;
    }
    div[data-testid="stChatMessage"] p, div[data-testid="stChatMessage"] span, div[data-testid="stAppViewContainer"] p {
        color: #ffffff !important; 
        font-size: 16px !important;
        font-weight: 500 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. नेचुरल वॉइस इंजन
def speak_natural(text):
    clean_text = text.replace('"', '').replace("'", "").replace("\n", " ")
    js = f"""<script>
        window.speechSynthesis.cancel(); 
        var msg = new SpeechSynthesisUtterance('{clean_text}');
        msg.lang = 'hi-IN';
        window.speechSynthesis.speak(msg);
    </script>"""
    components.html(js, height=0)

# 3. सुधरा हुआ फेस मैचिंग एल्गोरिदम (Template Matching - जो सिर्फ तुम्हें पहचानेगा)
def verify_face(target_img, registered_path="anurag_face.png"):
    if not os.path.exists(registered_path):
        return False
    
    # रजिस्टर्ड इमेज लोड करें
    img1 = cv2.imread(registered_path, cv2.IMREAD_GRAYSCALE)
    
    # लाइव कैमरा इमेज को OpenCV फॉर्मेट में बदलें
    file_bytes = np.asarray(bytearray(target_img.read()), dtype=np.uint8)
    img2 = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
    
    # दोनों को रीसाइज़ करें
    img1 = cv2.resize(img1, (200, 200))
    img2 = cv2.resize(img2, (200, 200))
    
    # स्ट्रक्चरल मैचिंग लॉजिक
    res = cv2.matchTemplate(img2, img1, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)
    
    # 0.45 थ्रेशोल्ड - रोशनी कम-ज़्यादा होने पर भी यह सिर्फ आपके चेहरे को पास करेगा
    return max_val > 0.45

# API कॉन्फ़िगरेशन
if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"].strip():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API KEY MISSING! Check Streamlit Secrets.")
    st.stop()

# Session State
if "unlocked" not in st.session_state:
    st.session_state.unlocked = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_voice" not in st.session_state:
    st.session_state.last_voice = ""

# --- FACE REGISTRATION & LOCK SCREEN ---
if not st.session_state.unlocked:
    st.markdown("<div class='lock-container'>", unsafe_allow_html=True)
    st.title("🛡️ VEER BIOMETRIC EYE LOCK")
    
    # चेकिंग कि क्या फेस रजिस्टर्ड है
    if not os.path.exists("anurag_face.png"):
        st.markdown("<div class='status-text' style='color:#00d2ff;'>⚙️ FIRST TIME SETUP: FACE NOT REGISTERED</div>", unsafe_allow_html=True)
        reg_shot = st.camera_input("अनुराग सर, अपना चेहरा कैमरे के सामने लाएं और रजिस्टर करें:")
        if reg_shot:
            img = Image.open(reg_shot)
