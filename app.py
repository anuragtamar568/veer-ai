import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text

# पेज कॉन्फ़िगरेशन (यह सबसे ऊपर होना जरूरी है)
st.set_page_config(page_title="VEER AI", page_icon="💻", layout="centered")

# 1. डार्क थीम, नियॉन लेटर्स और यूआई सेटिंग्स के लिए CSS
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

    ::-webkit-scrollbar {
        width: 0px;
        background: transparent;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# हेडर लेआउट
st.title("VEER AI")
st.markdown("<div class='developer-text'>SPECIALIST WORKSTATION</div>", unsafe_allow_html=True)
st.markdown("<div class='developer-text'>DEVELOPER: ANURAG // SECURE CONNECTION</div>", unsafe_allow_html=True)
st.write("---")

# JavaScript से ब्राउज़र में नई टैब खोलने का फंक्शन
def open_website(url):
    js = f"window.open('{url}', '_blank');"
    st.components.v1.html(f"<script>{js}</script>", height=0, width=0)

# API Configuration
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # चैट हिस्ट्री स्क्रीन पर लोड करना
    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # वॉयस इनपुट सेक्शन
    st.markdown("<div class='voice-label'>🎙️ VOICE COMMAND // INTERACT:</div>", unsafe_allow_html=True)
    voice_input = speech_to_text(
        start_prompt="START RECORDING",
        stop_prompt="STOP RECORDING",
        language='hi',
        key='speech'
    )

    text_input = st.chat_input("ENTER COMMAND...")
    prompt = voice_input if voice_input else text_input

    if prompt:
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # --- असिस्टेंट फीचर: कीवर्ड्स डिटेक्ट करना ---
        clean_prompt = prompt.lower()
        url_to_open = None
        assistant_reply = ""

        if "youtube" in clean_prompt or "यूट्यूब" in clean_prompt:
            url_to_open = "https://www.youtube.com"
            assistant_reply = "हाँ भाई, अभी खोलता हूँ यूट्यूब तुम्हारे लिए! एक नई टैब चेक करो।"
        elif "google" in clean_prompt or "गूगल" in clean_prompt:
            url_to_open = "https://www.google.com"
            assistant_reply = "लो भाई, गूगल बाबा को ओपन कर दिया है नई टैब में।"
        elif "github" in clean_prompt or "गिटहब" in clean_prompt:
            url_to_open = "https://www.github.com"
            assistant_reply = "बिल्कुल अनुराग भाई, गिटहब ओपन कर रहा हूँ।"
        elif "instagram" in clean_prompt or "इंस्टाग्राम" in clean_prompt:
            url_to_open = "https://www.instagram.com"
            assistant_reply = "चलो भाई, इंस्टाग्राम खोल दिया है। रील्स देखने का मन है क्या? 😉"

        # अगर कोई असिस्टेंट कमांड मिल गया
        if url_to_open:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(assistant_reply)
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
            open_website(url_to_open)
        else:
            # अगर नॉर्मल सवाल है, तो AI दोस्त की तरह जवाब देगा
            with st.chat_message("assistant", avatar="🤖"):
                placeholder = st.empty()
                placeholder.markdown("`ANALYZING COMMAND...`")
                
                try:
                    model = genai.GenerativeModel(
                        "gemini-2.5-flash",
                        system_instruction=(
                            "तुम्हारा नाम 'वीर' है। तुम कोई रोबोट या मशीन नहीं हो, बल्कि एक बेहद समझदार, कूल और दोस्ताना एआई असिस्टेंट हो। "
                            "तुम्हें सिर्फ और सिर्फ 'अनुराग' ने बनाया है। तुम्हारी बात करने की भाषा एकदम नेचुरल, आम इंसानों जैसी और हिंदी-इंग्लिश मिक्स (Hinglish) होनी चाहिए। "
                            "बातचीत में 'Greetings', 'प्रोटोकॉल्स' जैसे भारी-भरकम शब्दों का इस्तेमाल बिल्कुल मत करो। "
                            "जैसे कोई दोस्त आपस में बात करते हैं (जैसे 'अरे भाई', 'हाँ यार', 'बिल्कुल'), वैसे बात करो। "
                            "शुरुआत में या पहली बार पूछने पर एक बार गर्व से बता देना कि तुम्हें अनुराग ने बनाया है, लेकिन हर जवाब में बार-बार नाम मत दोहराना।"
                        )
                    )
                    response = model.generate_content(prompt)
                    
                    placeholder.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    
                except Exception as e:
                    placeholder.markdown(f"❌ `SYSTEM ERROR: {str(e)}`")

else:
    st.error("⚠️ CRITICAL: GEMINI_API_KEY NOT FOUND.")
