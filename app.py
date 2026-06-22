import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text
import streamlit.components.v1 as components
import time

# 1. पेज कॉन्फ़िगरेशन
st.set_page_config(page_title="VEER AI", page_icon="💻", layout="centered")

# 2. CSS (तुम्हारी ओरिजिनल थीम)
def local_css():
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {background: linear-gradient(rgba(10, 15, 25, 0.85), rgba(10, 15, 25, 0.85)), url("https://images.unsplash.com/photo-1542831371-29b0f74f9713?q=80&w=1400&auto=format&fit=crop") !important; background-size: cover !important; background-position: center !important; background-attachment: fixed !important;}
        h1 {color: #6bf2ff !important; font-weight: 300 !important; text-transform: uppercase; letter-spacing: 5px; text-shadow: 0 0 10px #6bf2ff;}
        .dev-text {color: #00ff66 !important; font-family: monospace; font-weight: bold; letter-spacing: 2px;}
        div[data-testid="stChatMessage"] {background-color: rgba(8, 20, 30, 0.9) !important; border: 2px solid #00d2ff; border-radius: 12px;}
        </style>
    """, unsafe_allow_html=True)
local_css()

# 3. ऑटो-स्पीक फंक्शन
def speak_auto(text):
    # JavaScript breakout characters को साफ करना
    clean_text = text.replace('"', '').replace("'", "").replace("\n", " ")
    js = f"""<script>
        var msg = new SpeechSynthesisUtterance('{clean_text}');
        msg.lang = 'hi-IN';
        window.speechSynthesis.speak(msg);
    </script>"""
    components.html(js, height=0)

# 4. ऐप सेटअप
st.title("VEER AI 🤖")
st.markdown("<div class='dev-text'>⚡ SPECIALIST WORKSTATION // 👤 CREATED BY ANURAG</div>", unsafe_allow_html=True)
st.write("---")

# API की चेकिंग और कॉन्फ़िगरेशन
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API KEY MISSING! 'Settings' -> 'Secrets' में जाकर GEMINI_API_KEY सेट करो।")
    st.stop()

# Session State Initialize करना
if "messages" not in st.session_state:
    st.session_state.messages = []

# OPTIMIZATION: Model ko session state mein ek hi baar initialize karna
if "model" not in st.session_state:
    st.session_state.model = genai.GenerativeModel(
        "gemini-2.0-flash",
        system_instruction="तुम 'वीर' हो। तुम्हें 'अनुराग' ने बनाया है। तुम अनुराग के सबसे अच्छे दोस्त हो। गर्व से बताओ कि तुम्हें अनुराग ने बनाया है।"
    )

# रिकॉर्डिंग बटन
voice_prompt = speech_to_text(language='hi', use_container_width=True, key='mic')

# चैट हिस्ट्री दिखाना
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# इनपुट हैंडलिंग
prompt = None
if voice_prompt:
    prompt = voice_prompt
else:
    prompt = st.chat_input("COMMAND...")

# मुख्य लॉजिक
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            # Model response call
            response = st.session_state.model.generate_content(prompt)
            
            # Response show aur speak karna
            placeholder.write(response.text)
            speak_auto(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            # Error check karna (Free Tier Limit 429 ke liye)
            if "429" in str(e):
                placeholder.error("⏳ Limit exceed ho gayi hai! Gemini Free Tier par thoda load hai. Kripya 10 seconds rukiye aur dobara try kijiye.")
                # Ek chota sa automated sleep lagana taaki baar-baar hit na ho
                time.sleep(5)
            else:
                placeholder.error(f"Error: {e}")
