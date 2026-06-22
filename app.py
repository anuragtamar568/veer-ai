import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text

# पेज कॉन्फ़िगरेशन (यह सबसे ऊपर होना जरूरी है)
st.set_page_config(page_title="VEER AI", page_icon="💻", layout="centered")

# 1. बैकग्राउंड इमेज और नियॉन टेक्स्ट लेटर्स के लिए पुराना परफेक्ट CSS
def local_css():
    st.markdown("""
    <style>
    /* पूरे ऐप के बैकग्राउंड को ट्रांसपेरेंट करना */
    [data-testid="stAppViewContainer"] {
        background-color: transparent !important;
    }
    
    /* स्पेशल हाई-टेक लैपटॉप बैकग्राउंड इमेज */
    .bg-img-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        overflow: hidden;
    }
    .bg-img-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        filter: brightness(0.35) contrast(1.1); /* इमेज को डार्क किया ताकि टेक्स्ट साफ़ दिखे */
    }
    
    /* VEER AI - डिज़ाइनर नियॉन टेक्स्ट लेटर्स */
    h1 {
        color: #6bf2ff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        font-weight: 300 !important;
        text-transform: uppercase;
        letter-spacing: 5px;
        text-shadow: 0 0 10px rgba(107, 242, 255, 0.8), 0 0 25px rgba(107, 242, 255, 0.5);
        margin-bottom: 5px !important;
    }
    
    /* सब-हेडिंग्स (Specialist Workstation) स्टाइल */
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

    /* चैट बॉक्स को पारदर्शी और नियॉन ब्लू बॉर्डर वाला बनाना */
    div[data-testid="stChatMessage"] {
        background-color: rgba(8, 20, 30, 0.85) !important;
        border: 2px solid #00d2ff;
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.4);
        margin-bottom: 15px;
        padding: 15px !important;
    }

    /* नॉर्मल टेक्स्ट का कलर (सफ़ेद) */
    p, span, div, label {
        color: #ffffff !important;
        font-family: 'Segoe UI', sans-serif !important;
    }
    
    /* चैट इनपुट कंटेनर स्टाइल */
    .stChatInputContainer {
        background-color: rgba(5, 10, 15, 0.95) !important;
        border: 2px solid #00d2ff !important;
        border-radius: 8px !important;
    }
    
    .stChatInputContainer textarea {
        color: #ffffff !important;
    }

    /* वॉयस कमांड टेक्स्ट */
    .voice-label {
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold;
        margin-top: 15px;
    }

    /* माइक बटन का हैकर स्टाइल */
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

    /* स्क्रॉलबार छिपाना */
    ::-webkit-scrollbar {
        width: 0px;
        background: transparent;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# नया फुल-वर्किंग प्रीमियम साइबर लैपटॉप बैकग्राउंड लिंक
st.markdown(
    '<div class="bg-img-container"><img src="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1400&auto=format&fit=crop"></div>',
    unsafe_allow_html=True
)

# हेडर लेआउट
st.title("VEER AI")
st.markdown("<div class='developer-text'>SPECIALIST WORKSTATION</div>", unsafe_allow_html=True)
st.markdown("<div class='developer-text'>DEVELOPER: ANURAG // SECURE CONNECTION</div>", unsafe_allow_html=True)
st.write("---")

# API Configuration
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # चैट हिस्ट्री स्क्रीन पर लोड करना (साफ़-सुथरे इमोजी सिम्बल्स के साथ)
    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "🤖"
