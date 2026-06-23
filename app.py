import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text
import streamlit.components.v1 as components
from PIL import Image

# 1. ✨ CLEAN PROFESSIONAL THEME
st.set_page_config(page_title="VEER AI // ASSISTANT", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    /* व्हाइट और क्लीन लुक */
    .stApp {
        background-color: #ffffff !important;
    }
    h1 {
        color: #2c3e50 !important;
        text-align: center;
        font-family: sans-serif !important;
    }
    .stChatMessage {
        background-color: #f8f9fa !important;
        border: 1px solid #dee2e6 !important;
        border-radius: 10px !important;
    }
    .stButton>button {
        background-color: #007bff !important;
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
    st.error("API Key नहीं मिली। कृपया secrets में जोड़ें।")
    st.stop()

# Session States
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🤖 वीर AI असिस्टेंट")

# कंट्रोल हब
if st.button("🗑️ क्लियर चैट"):
    st.session_state.chat_history = []
    st.rerun()

# --- कैमरा और फाइल इनपुट ---
input_mode = st.radio("इनपुट तरीका:", ["📷 कैमरा", "📁 फोटो अपलोड"])
active_image = None

if input_mode == "📷 कैमरा":
    cam_shot = st.camera_input("फोटो खींचें:")
    if cam_shot:
        active_image = Image.open(cam_shot)
else:
    uploaded_image = st.file_uploader("फोटो चुनें...", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        active_image = Image.open(uploaded_image)

# --- CHAT INPUTS ---
text_input = st.chat_input("अपना सवाल लिखें...")

# चैट रेंडरर
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

# जेमिनी लॉजिक
if text_input:
    st.session_state.chat_history.append({"role": "user", "content": text_input})
    with st.chat_message("user"):
        st.write(text_input)

    with st.chat_message("assistant"):
        with st.spinner("सोच रहा हूँ..."):
            try:
                model = genai.GenerativeModel("gemini-2.0-flash")
                sys_prompt = "तुम वीर हो, अनुराग सर के पर्सनल असिस्टेंट। हमेशा हिंदी में संक्षिप्त और सटीक जवाब दो।"
                
                if active_image:
                    response = model.generate_content([sys_prompt, active_image, text_input])
                else:
                    response = model.generate_content([sys_prompt, text_input])
                
                reply = response.text
                st.write(reply)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                speak_natural(reply)
            except Exception as e:
                st.write("क्षमा करें सर, कोई तकनीकी दिक्कत आ रही है।")
    if "role" in chat and "content" in chat:
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
            reply = f"अनुराग सर, सर्वर कनेक्ट करने में थोड़ा समय लग रहा है। आपने पूछा था: '{final_input}'"
                
        placeholder.write(reply)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        speak_natural(reply)
