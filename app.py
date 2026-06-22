import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text
import streamlit.components.v1 as components

# 1. पेज कॉन्फ़िगरेशन
st.set_page_config(page_title="VEER AI", page_icon="💻", layout="centered")

# 2. CSS स्टाइलिंग (आपकी पुरानी थीम)
def local_css():
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {background: linear-gradient(rgba(10, 15, 25, 0.85), rgba(10, 15, 25, 0.85)), url("https://images.unsplash.com/photo-1542831371-29b0f74f9713?q=80&w=1400&auto=format&fit=crop") !important; background-size: cover !important; background-position: center !important; background-attachment: fixed !important;}
        [data-testid="stHeader"] {background: transparent !important;}
        h1 {color: #6bf2ff !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important; font-weight: 300 !important; text-transform: uppercase; letter-spacing: 5px; text-shadow: 0 0 10px rgba(107, 242, 255, 0.8), 0 0 25px rgba(107, 242, 255, 0.5); margin-bottom: 5px !important;}
        .developer-text {color: #00ff66 !important; font-family: 'Courier New', Courier, monospace !important; font-weight: bold; letter-spacing: 2px; font-size: 14px; text-shadow: 0 0 8px rgba(0, 255, 102, 0.6); margin-top: 2px !important; margin-bottom: 2px !important;}
        div[data-testid="stChatMessage"] {background-color: rgba(8, 20, 30, 0.9) !important; border: 2px solid #00d2ff; border-radius: 12px; box-shadow: 0 0 15px rgba(0, 210, 255, 0.4); margin-bottom: 15px; padding: 15px !important;}
        p, span, div, label {color: #ffffff !important; font-family: 'Segoe UI', sans-serif !important;}
        .stChatInputContainer {background-color: rgba(5, 10, 15, 0.95) !important; border: 2px solid #00d2ff !important; border-radius: 8px !important;}
        .stChatInputContainer textarea {color: #ffffff !important;}
        .voice-label {color: #ffffff !important; font-family: 'Courier New', monospace !important; font-weight: bold; margin-top: 15px;}
        button {background-color: #050a10 !important; border: 1px solid #00d2ff !important; color: #00d2ff !important; border-radius: 4px !important;}
        button:hover {background-color: #00d2ff !important; color: black !important; box-shadow: 0 0 10px #00d2ff;}
        </style>
    """, unsafe_allow_html=True)

local_css()

# ऑटो-बोलने वाला फंक्शन
def speak_auto(text):
    clean_text = text.replace('"', '').replace("'", "")
    js = f"""
    <script>
        var msg = new SpeechSynthesisUtterance('{clean_text}');
        msg.lang = 'hi-IN';
        window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js, height=0)

# 3. ऐप सेटअप
st.title("VEER AI")
st.markdown("<div class='developer-text'>SPECIALIST WORKSTATION // DEVELOPED BY ANURAG</div>", unsafe_allow_html=True)
st.write("---")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# रिकॉर्डिंग बटन
st.markdown("<div class='voice-label'>🎙️ RECORD VOICE COMMAND:</div>", unsafe_allow_html=True)
voice_prompt = speech_to_text(language='hi', use_container_width=True, key='mic')

# चैट हिस्ट्री
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# इनपुट हैंडलिंग
prompt = voice_prompt if voice_prompt else st.chat_input("TYPE COMMAND...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            model = genai.GenerativeModel(
                "gemini-2.0-flash",
                system_instruction="तुम्हारा नाम 'वीर' है। तुम्हें 'अनुराग' ने बनाया है। तुम अनुराग के सबसे अच्छे दोस्त हो। हमेशा गर्व से बताओ कि तुम्हें अनुराग ने बनाया है।"
            )
            response = model.generate_content(prompt)
            placeholder.write(response.text)
            speak_auto(response.text) # वीर अपने आप बोलेगा
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("API Error!")
