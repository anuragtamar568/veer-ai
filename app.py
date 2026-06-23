import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text
import streamlit.components.v1 as components
from PIL import Image
import time

# 1. 🔥 CYBERPUNK PREMIUM THEME
st.set_page_config(page_title="VEER_OS // QUANTUM_CORE", page_icon="🥷", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at center, #0a1128 0%, #000411 100%) !important;
    }
    h1 {
        color: #00ffaa !important; 
        text-transform: uppercase; 
        letter-spacing: 6px; 
        text-shadow: 0 0 20px rgba(0, 255, 170, 0.6);
        text-align: center;
        font-weight: 800 !important;
    }
    .status-panel {
        background: rgba(0, 255, 170, 0.03);
        border: 1px solid rgba(0, 255, 170, 0.2);
        padding: 15px;
        border-radius: 8px;
        color: #00ffaa !important;
        font-family: monospace !important;
    }
    div[data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.02) !important; 
        border-left: 4px solid #00ffaa !important; 
        border-radius: 8px !important;
    }
    .stButton>button {
        background: linear-gradient(45deg, #ff2e63, #ff0055) !important;
        color: white !important;
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# वॉइस इंजन
def speak_natural(text):
    clean_text = text.replace('"', '').replace("'", "").replace("\n", " ")
    js = f"<script>window.speechSynthesis.cancel(); var msg = new SpeechSynthesisUtterance('{clean_text}'); msg.lang = 'hi-IN'; window.speechSynthesis.speak(msg);</script>"
    components.html(js, height=0)

# API कॉन्फ़िगरेशन
if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"].strip():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("[FATAL]: Gemini API Key Missing in Streamlit Secrets.")
    st.stop()

# Session States
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_voice" not in st.session_state:
    st.session_state.last_voice = ""

# --- 💻 QUANTUM MAINFRAME WORKSTATION (DIRECT ACCESS) ---
if "welcomed" not in st.session_state:
    # यहाँ स्पेलिंग बिल्कुल ठीक कर दी है (SpeechSynthesisUtterance)
    components.html("<script>var m = new SpeechSynthesisUtterance('स्वागत है अनुराग सर। वीर ओ एस सक्रिय है।'); m.lang='hi-IN'; window.speechSynthesis.speak(m);</script>", height=0)
    st.session_state.welcomed = True

st.title("VEER QUANTUM AI 🤖 👁️")
st.markdown("<div class='status-panel'>⚡ STATUS: MAIN_FRAME_CONNECTED // IDENTITY: BYPASS_OK // OWNER: ANURAG SIR</div>", unsafe_allow_html=True)

# कंट्रोल हब
col1, col2 = st.columns([7, 3])
with col1:
    if st.button("🗑️ Wipe Logs (Clear Chat)"):
        st.session_state.chat_history = []
        st.session_state.last_voice = ""
        st.rerun()

# --- 👀 LIVE OPTICAL HUB ---
st.markdown("### 👁️ वीर की लाइव आँख (Analyze Live Feed)")

input_mode = st.radio("इनपुट का तरीका चुनें सर:", ["🎥 लाइव वेबकैम (Live Camera)", "📁 गैलरी से फोटो अपलोड करें"])

active_image = None
if input_mode == "🎥 लाइव वेबकैम (Live Camera)":
    cam_shot = st.camera_input("कैमरे के सामने कोई भी चीज़ लाएं और फोटो क्लिक करें सर:")
    if cam_shot:
        active_image = Image.open(cam_shot)
else:
    uploaded_image = st.file_uploader("गैलरी से कोई भी फोटो अपलोड करें...", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        active_image = Image.open(uploaded_image)

# --- CHAT INPUTS ---
voice_input = speech_to_text(language='hi', use_container_width=True, key='stable_mic')
text_input = st.chat_input("Yahan apna sawal likho ya bolo...")

final_input = None
if voice_input and voice_input.strip() and voice_input != st.session_state.last_voice:
    final_input = voice_input
    st.session_state.last_voice = voice_input
elif text_input and text_input.strip():
    final_input = text_input

# चैट रेंडरर
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

# जेमिनी सुपर कोर लॉजिक
if final_input:
    st.session_state.chat_history.append({"role": "user", "content": final_input})
    with st.chat_message("user"):
        st.write(final_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            with st.spinner("वीर सोच रहा है..."):
                sys_prompt = (
                    "तुम 'वीर' (VEER AI) हो, जिसे तुम्हारे मालिक 'अनुराग सर' ने बनाया है। "
                    "तुम अनुराग सर के प्रति पूरी तरह वफादार हो। हमेशा उन्हें 'अनुराग सर' या 'सर' कहकर संबोधित करो। "
                    "अगर कोई इमेज दी गई है, तो उसे ध्यान से देखो और अनुराग सर को उसका सटीक और देसी हिंदी में जवाब दो।"
                )
                
                model = genai.GenerativeModel("gemini-2.0-flash")
                if active_image:
                    response = model.generate_content([sys_prompt, active_image, final_input])
                else:
                    response = model.generate_content([sys_prompt, final_input])
                
                reply = response.text
                
        except Exception as e:
            reply = f"अनुराग सर, सर्वर पर थोड़ा लोड है, लेकिन मैं आपके साथ हूँ। आपने पूछा: '{final_input}'"
                
        placeholder.write(reply)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        speak_natural(reply)
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

# जेमिनी सुपर कोर लॉजिक
if final_input:
    st.session_state.chat_history.append({"role": "user", "content": final_input})
    with st.chat_message("user"):
        st.write(final_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            with st.spinner("वीर सोच रहा है..."):
                sys_prompt = (
                    "तुम 'वीर' (VEER AI) हो, जिसे तुम्हारे मालिक 'अनुراق सर' ने बनाया है। "
                    "तुम अनुराग सर के प्रति पूरी तरह वफादार हो। हमेशा उन्हें 'अनुराग सर' या 'सर' कहकर संबोधित करो। "
                    "अगर कोई इमेज दी गई है, तो उसे ध्यान से देखो और अनुराग सर को उसका सटीक और देसी हिंदी में जवाब दो।"
                )
                
                model = genai.GenerativeModel("gemini-2.0-flash")
                if active_image:
                    response = model.generate_content([sys_prompt, active_image, final_input])
                else:
                    response = model.generate_content([sys_prompt, final_input])
                
                reply = response.text
                
        except Exception as e:
            reply = f"अनुराग सर, सर्वर पर थोड़ा लोड है, लेकिन मैं आपके साथ हूँ। आपने पूछा: '{final_input}'"
                
        placeholder.write(reply)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        speak_natural(reply)
