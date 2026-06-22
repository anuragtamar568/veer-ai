import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text
import streamlit.components.v1 as components

# 1. पेज कॉन्फ़िगरेशन
st.set_page_config(page_title="VEER AI", page_icon="💻", layout="centered")

# 2. CSS स्टाइलिंग (तुम्हारी ओरिजिनल थीम - No Change)
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
        div.stLinkButton > a {background-color: #050a10 !important; color: #00ff66 !important; border: 2px solid #00ff66 !important; border-radius: 6px !important; font-family: 'Courier New', monospace !important; font-weight: bold !important; letter-spacing: 1px !important; box-shadow: 0 0 10px rgba(0, 255, 102, 0.3) !important; transition: all 0.3s ease !important; display: inline-flex !important; align-items: center !important; justify-content: center !important; padding: 10px 20px !important; text-decoration: none !important;}
        div.stLinkButton > a:hover {background-color: #00ff66 !important; color: #050a10 !important; box-shadow: 0 0 15px #00ff66 !important;}
        ::-webkit-scrollbar {width: 0px; background: transparent;}
        </style>
    """, unsafe_allow_html=True)

local_css()

# 3. बोलने वाला फंक्शन (Javascript आधारित - एकदम नेचुरल आवाज़)
def speak_js(text):
    js_code = f"""
    <script>
        var msg = new SpeechSynthesisUtterance("{text.replace('"', '')}");
        msg.lang = 'hi-IN';
        window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js_code, height=0)

# 4. ऐप्स की लिस्ट
APPS_LIST = {
    "youtube": {"url": "https://www.youtube.com", "text": "यूट्यूब खोल रहा हूँ भाई!", "btn": "OPEN YOUTUBE"},
    "google": {"url": "https://www.google.com", "text": "गूगल सर्च हाजिर है!", "btn": "OPEN GOOGLE"},
    "instagram": {"url": "https://www.instagram.com", "text": "इंस्टाग्राम खोल रहा हूँ!", "btn": "OPEN INSTAGRAM"},
    "chatgpt": {"url": "https://chatgpt.com", "text": "चैटजीपीटी खोल रहा हूँ।", "btn": "OPEN CHATGPT"}
}

st.title("VEER AI")
st.markdown("<div class='developer-text'>SPECIALIST WORKSTATION</div>", unsafe_allow_html=True)
st.write("---")

# 5. API Setup
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# हिस्ट्री दिखाएं
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        if isinstance(message["content"], dict):
            st.write(message["content"]["text"])
            st.link_button(message["content"]["btn"], message["content"]["url"])
        else:
            st.markdown(str(message["content"]))

# 6. इनपुट
prompt = st.chat_input("ENTER COMMAND...")

if prompt:
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    clean_prompt = prompt.lower()
    found_app = next((info for app, info in APPS_LIST.items() if app in clean_prompt), None)

    with st.chat_message("assistant", avatar="🤖"):
        if found_app:
            st.write(found_app["text"])
            st.link_button(found_app["btn"], found_app["url"])
            speak_js(found_app["text"])
            st.session_state.messages.append({"role": "assistant", "content": found_app["text"]})
        else:
            placeholder = st.empty()
            placeholder.markdown("`ANALYZING...`")
            try:
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(prompt)
                placeholder.markdown(response.text)
                speak_js(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                placeholder.markdown("अरे यार, कुछ गड़बड़ हो गई!")
