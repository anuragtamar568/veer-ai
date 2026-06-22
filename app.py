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

# 5. Session State Initialize
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_sent" not in st.session_state:
    st.session_state.last_sent = None

# Clear Chat History Button
if st.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    if "chat" in st.session_state:
        del st.session_state["chat"]
    if "last_sent" in st.session_state:
        st.session_state.last_sent = None
    st.rerun()

st.write("---")

# API की चेकिंग
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API KEY MISSING! 'Settings' -> 'Secrets' में जाकर GEMINI_API_KEY सेट करो।")
    st.stop()

# Chat Session Setup
if "chat" not in st.session_state:
    try:
        model = genai.GenerativeModel(
            "gemini-2.0-flash",
            system_instruction="तुम 'वीर' हो। तुम्हें 'अनुराग' ने बनाया है। तुम अनुराग के सबसे अच्छे दोस्त हो। गर्व से बताओ कि तुम्हें अनुराग ने बनाया है।"
        )
        st.session_state.chat = model.start_chat(history=[])
    except Exception as e:
        st.error(f"Model Init Error: {e}")

# रिकॉर्डिंग बटन - Isko ek form block jaisa control karenge
voice_prompt = speech_to_text(language='hi', use_container_width=True, key='mic')

# चैट हिस्ट्री दिखाना
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# इनपुट कैप्चर
user_input = st.chat_input("COMMAND...")
final_prompt = None

# STRICT SPAM PROTECTION: Agar voice prompt bilkul naya hai aur pichle sent message se alag hai tabhi chalega
if voice_prompt and voice_prompt.strip():
    if st.session_state.last_sent != voice_prompt:
        final_prompt = voice_prompt
elif user_input and user_input.strip():
    if st.session_state.last_sent != user_input:
        final_prompt = user_input

# मुख्य लॉजिक
if final_prompt:
    # Turant last_sent ko lock karo taaki agla background rerun ise chalaye na
    st.session_state.last_sent = final_prompt
    
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    with st.chat_message("user"):
        st.write(final_prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            # Gemini Chat Call
            response = st.session_state.chat.send_message(final_prompt)
            
            # Response handling
            placeholder.write(response.text)
            speak_auto(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
            
        except Exception as e:
            if "429" in str(e):
                placeholder.error("🛑 Google ki block limit active hai. Pehle upar 'Clear Chat History' dabayein, fir page ko refresh karke 10 second baad check karein.")
            else:
                placeholder.error(f"Error: {e}")
