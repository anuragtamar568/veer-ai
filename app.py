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
st.write("---")

# API की चेकिंग
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API KEY MISSING! 'Settings' -> 'Secrets' में जाकर GEMINI_API_KEY सेट करो।")
    st.stop()

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat Session setup
if "chat" not in st.session_state:
    model = genai.GenerativeModel(
        "gemini-2.0-flash",
        system_instruction="तुम 'वीर' हो। तुम्हें 'अनुराग' ने बनाया है। तुम अनुराग के सबसे अच्छे दोस्त हो। गर्व से बताओ कि तुम्हें अनुराग ने बनाया है।"
    )
    st.session_state.chat = model.start_chat(history=[])

# रिकॉर्डिंग बटन
voice_prompt = speech_to_text(language='hi', use_container_width=True, key='mic')

# चैट हिस्ट्री दिखाना (Duplicate messages filter karne ke liye unique tracking)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# इनपुट कैप्चर और डुप्लीकेट प्रोटेक्शन लॉजिक
prompt = None
user_input = st.chat_input("COMMAND...")

if voice_prompt and voice_prompt.strip():
    # Mic se input mila, check karein ki kya ye wahi purana text toh nahi jo rerun ho raha hai
    if "last_processed_voice" not in st.session_state or st.session_state.last_processed_voice != voice_prompt:
        prompt = voice_prompt
        st.session_state.last_processed_voice = voice_prompt  # Mark as processed
elif user_input and user_input.strip():
    prompt = user_input

# मुख्य लॉजिक (Sirf tabhi chalega jab real naya prompt ho)
if prompt:
    # Double check to prevent automated reload spam
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            # Gemini Call
            response = st.session_state.chat.send_message(prompt)
            
            # Output & Speech
            placeholder.write(response.text)
            speak_auto(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
            # Response aane ke baad page ko clean refresh kar do taaki mic ka purana data session se udd jaye
            st.rerun()
            
        except Exception as e:
            if "429" in str(e):
                placeholder.error("⏳ Google Free Tier ki RPM (Requests Per Minute) limit hit hui hai. Kripya 15-20 seconds rukiye aur page refresh karke try kijiye!")
                time.sleep(3)
            else:
                placeholder.error(f"Error: {e}")
