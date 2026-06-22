import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text

# पेज कॉन्फ़िगरेशन
st.set_page_config(page_title="VEER AI", page_icon="💻", layout="centered")

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
    h1 { color: #6bf2ff !important; font-family: 'Segoe UI', sans-serif !important; text-transform: uppercase; letter-spacing: 5px; text-shadow: 0 0 10px rgba(107, 242, 255, 0.8); }
    .developer-text { color: #00ff66 !important; font-family: 'Courier New', monospace; font-weight: bold; }
    div[data-testid="stChatMessage"] { background-color: rgba(8, 20, 30, 0.9) !important; border: 2px solid #00d2ff; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

local_css()

st.title("VEER AI")
st.markdown("<div class='developer-text'>SPECIALIST WORKSTATION</div>", unsafe_allow_html=True)
st.markdown("<div class='developer-text'>DEVELOPER: ANURAG // SECURE CONNECTION</div>", unsafe_allow_html=True)
st.write("---")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            if isinstance(message["content"], dict) and message["content"].get("type") == "link_button":
                st.write(message["content"]["text"])
                st.link_button(message["content"]["button_text"], message["content"]["url"])
            else:
                st.markdown(str(message["content"]))

    voice_input = speech_to_text(start_prompt="🎙️ START RECORDING", stop_prompt="STOP", language='hi', key='speech')
    text_input = st.chat_input("ENTER COMMAND...")
    prompt = voice_input if voice_input else text_input

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        clean_prompt = prompt.lower().replace(" ", "")
        url_to_open, assistant_reply, button_text = None, "", ""

        if "youtube" in clean_prompt:
            url_to_open, assistant_reply, button_text = "https://www.youtube.com", "यूट्यूब खोलने का लिंक तैयार है!", "🚀 OPEN YOUTUBE"
        elif "google" in clean_prompt:
            url_to_open, assistant_reply, button_text = "https://www.google.com", "गूगल बाबा का एक्सेस रेडी है।", "🔍 OPEN GOOGLE"
        elif "github" in clean_prompt:
            url_to_open, assistant_reply, button_text = "https://www.github.com", "गिटहब ओपन करने के लिए नीचे क्लिक करो।", "🐙 OPEN GITHUB"
        elif "instagram" in clean_prompt:
            url_to_open, assistant_reply, button_text = "https://www.instagram.com", "इंस्टाग्राम का लिंक हाजिर है!", "📸 OPEN INSTAGRAM"

        if url_to_open:
            with st.chat_message("assistant", avatar="🤖"):
                st.write(assistant_reply)
                st.link_button(button_text, url_to_open)
            st.session_state.messages.append({"role": "assistant", "content": {"type": "link_button", "text": assistant_reply, "button_text": button_text, "url": url_to_open}})
        else:
            with st.chat_message("assistant", avatar="🤖"):
                placeholder = st.empty()
                placeholder.markdown("`ANALYZING...`")
                try:
                    # Model name 'gemini-1.5-flash' sahi model hai
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(prompt)
                    placeholder.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    placeholder.markdown(f"❌ `ERROR: {str(e)}`")
else:
    st.error("⚠️ CRITICAL: GEMINI_API_KEY NOT FOUND.")
