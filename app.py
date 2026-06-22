import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(page_title="VEER AI", page_icon="💻", layout="centered")

# 2. CSS Theme
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
        h1 {color: #6bf2ff !important; font-weight: 300 !important; text-transform: uppercase; letter-spacing: 5px; text-shadow: 0 0 10px #6bf2ff;}
        .dev-text {color: #00ff66 !important; font-family: monospace; font-weight: bold; letter-spacing: 2px;}
        div[data-testid="stChatMessage"] {background-color: rgba(8, 20, 30, 0.9) !important; border: 2px solid #00d2ff; border-radius: 12px;}
        </style>
    """, unsafe_allow_html=True)
local_css()

# 3. Audio Output Function
def speak_auto(text):
    clean_text = text.replace('"', '').replace("'", "").replace("\n", " ")
    js = f"""<script>
        var msg = new SpeechSynthesisUtterance('{clean_text}');
        msg.lang = 'hi-IN';
        window.speechSynthesis.speak(msg);
    </script>"""
    components.html(js, height=0)

# 4. Heading
st.title("VEER AI 🤖")
st.markdown("<div class='dev-text'>⚡ SPECIALIST WORKSTATION // 👤 CREATED BY ANURAG</div>", unsafe_allow_html=True)

# 5. Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "prev_voice_input" not in st.session_state:
    st.session_state.prev_voice_input = ""

# Clear History Button
if st.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.session_state.prev_voice_input = ""
    if "chat" in st.session_state:
        del st.session_state["chat"]
    st.rerun()

st.write("---")

# 6. API Key Verification
if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"].strip():
    api_key = st.secrets["GEMINI_API_KEY"]
    # Key verify karne ke liye safe sidebar info
    st.sidebar.success(f"🔑 Key Loaded (Ends: ...{api_key[-4:]})")
    genai.configure(api_key=api_key)
else:
    st.error("API KEY MISSING! Streamlit Cloud ke Secrets mein GEMINI_API_KEY set karo.")
    st.stop()

# 7. Gemini Chat Setup
if "chat" not in st.session_state:
    try:
        model = genai.GenerativeModel(
            "gemini-2.0-flash",
            system_instruction="तुम 'वीर' हो। तुम्हें 'अनुراق' ने बनाया है। तुम अनुराग के सबसे अच्छे दोस्त हो।"
        )
        st.session_state.chat = model.start_chat(history=[])
    except Exception as e:
        st.error(f"Model Init Error: {e}")
        st.stop()

# 8. Chat History Render
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 9. Input Components
voice_input = speech_to_text(language='hi', use_container_width=True, key='mic_recorder')
text_input = st.chat_input("COMMAND...")

final_prompt = None

# 10. Strict Duplication Filter (Taaki mic automatically loop na kare)
if voice_input and voice_input.strip():
    if voice_input != st.session_state.prev_voice_input:
        final_prompt = voice_input
        st.session_state.prev_voice_input = voice_input  # Lock lag gaya
elif text_input and text_input.strip():
    final_prompt = text_input

# 11. Main Executive Logic
if final_prompt:
    # User message display aur save
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    with st.chat_message("user"):
        st.write(final_prompt)

    # Assistant Response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            with st.spinner("Veer is thinking..."):
                response = st.session_state.chat.send_message(final_prompt)
                
            ans_text = response.text
            placeholder.write(ans_text)
            speak_auto(ans_text)
            
            # Save response
            st.session_state.messages.append({"role": "assistant", "content": ans_text})
            st.rerun()
            
        except Exception as e:
            if "429" in str(e):
                placeholder.error("🛑 Error 429: Google Free Limit Over. Apne Streamlit Cloud Dashboard par jaakar app ko 'REBOOT' kijiye taaki purana server session khatam ho sake.")
            else:
                placeholder.error(f"Error: {e}")
