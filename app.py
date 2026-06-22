import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text
import streamlit.components.v1 as components

# 1. पेज कॉन्फ़िगरेशन और हाई-विजिबिलिटी थीम
st.set_page_config(page_title="VEER AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(rgba(10, 15, 25, 0.95), rgba(10, 15, 25, 0.95)), 
                    url("https://images.unsplash.com/photo-1542831371-29b0f74f9713?q=80&w=1400&auto=format&fit=crop") !important; 
        background-size: cover !important; background-position: center !important; background-attachment: fixed !important;
    }
    h1 {color: #6bf2ff !important; font-weight: 300 !important; text-transform: uppercase; letter-spacing: 5px; text-shadow: 0 0 10px #6bf2ff;}
    .dev-text {color: #00ff66 !important; font-family: monospace; font-weight: bold; letter-spacing: 2px;}
    
    /* Text Visibility Fix: Chat text completely White */
    div[data-testid="stChatMessage"] {
        background-color: rgba(8, 20, 30, 0.95) !important; 
        border: 2px solid #00d2ff; 
        border-radius: 12px;
    }
    div[data-testid="stChatMessage"] p, div[data-testid="stChatMessage"] span, div[data-testid="stAppViewContainer"] p {
        color: #ffffff !important; 
        font-size: 16px !important;
        font-weight: 500 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("VEER AI 🤖")
st.markdown("<div class='dev-text'>⚡ REAL VOICE WORKSTATION // 👤 CREATED BY ANURAG</div>", unsafe_allow_html=True)
st.write("---")

# 2. नेचुरल ह्यूमन वॉइस स्क्रिप्ट (Bypasses robotic gTTS)
def speak_natural(text):
    clean_text = text.replace('"', '').replace("'", "").replace("\n", " ")
    js = f"""<script>
        window.speechSynthesis.cancel(); // Stop any overlapping audio
        var msg = new SpeechSynthesisUtterance('{clean_text}');
        msg.lang = 'hi-IN';
        msg.pitch = 1.0;
        msg.rate = 1.0;
        window.speechSynthesis.speak(msg);
    </script>"""
    components.html(js, height=0)

# 3. Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_processed" not in st.session_state:
    st.session_state.last_processed = None

# Clear Chat
if st.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.session_state.last_processed = None
    if "chat" in st.session_state:
        del st.session_state["chat"]
    st.rerun()

# 4. API की चेकिंग
if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"].strip():
    api_key = st.secrets["GEMINI_API_KEY"]
    st.sidebar.success(f"🔑 Key Active (Ends: ...{api_key[-4:]})")
    genai.configure(api_key=api_key)
else:
    st.error("API KEY MISSING! Settings -> Secrets में जाकर GEMINI_API_KEY सेट करो।")
    st.stop()

# 5. Chat Session Setup (Personality Injection)
if "chat" not in st.session_state:
    try:
        model = genai.GenerativeModel(
            "gemini-2.0-flash",
            system_instruction="तुम 'वीर' हो। तुम्हें 'अनुराग' ने बनाया है। तुम अनुराग के सबसे अच्छे दोस्त हो। हमेशा अनुराग भाई कहकर बात करो। आवाज में रोबोटिकपन नहीं होना चाहिए, एक सच्चे दोस्त की तरह हिंदी में बात करो। सीधे और सही जवाब दो।"
        )
        st.session_state.chat = model.start_chat(history=[])
    except Exception as e:
        st.error(f"Model Init Error: {e}")
        st.stop()

# 6. Chat History Render
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 7. Input Components
voice_prompt = speech_to_text(language='hi', use_container_width=True, key='mic')
user_input = st.chat_input("COMMAND...")

current_prompt = None

if voice_prompt and voice_prompt.strip():
    if st.session_state.last_processed != voice_prompt:
        current_prompt = voice_prompt
elif user_input and user_input.strip():
    current_prompt = user_input

# 8. Execution Logic (Gemini Brain + Natural Voice)
if current_prompt:
    st.session_state.last_processed = current_prompt
    st.session_state.messages.append({"role": "user", "content": current_prompt})
    
    with st.chat_message("user"):
        st.write(current_prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            with st.spinner("Veer is thinking..."):
                response = st.session_state.chat.send_message(current_prompt)
            
            ans_text = response.text
            placeholder.write(ans_text)
            st.session_state.messages.append({"role": "assistant", "content": ans_text})
            
            # Executing natural voice
            speak_natural(ans_text)
            st.rerun()
            
        except Exception as e:
            if "429" in str(e):
                placeholder.error("🛑 Google Free Quota error! Dashboard par jaakar App ko REBOOT karein taaki aapki nayi key active ho sake.")
            else:
                placeholder.error(f"Error: {e}")
