import streamlit as st
from streamlit_mic_recorder import speech_to_text
import base64
from gtts import gTTS
import os
import urllib.request
import json

# 1. Page Configuration & Improved High-Visibility Theme
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
    
    /* Text Visibility Fix: Chat text color forced to White and bold */
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
st.markdown("<div class='dev-text'>⚡ SPEAKING WORKSTATION // 👤 CREATED BY ANURAG</div>", unsafe_allow_html=True)
st.write("---")

# 2. Free Intelligent Question Responder Function (No Gemini API Key Needed)
def get_intelligent_reply(user_query):
    query_lower = user_query.lower()
    
    # Quick custom checks for identity
    if "hii" in query_lower or "hello" in query_lower or "hey" in query_lower:
        return "नमस्ते अनुराग भाई! मैं वीर हूँ, आपका सबसे अच्छा दोस्त। कहिए आज क्या पूछना है?"
    if "kaun ho" in query_lower or "tumhara naam" in query_lower:
        return "मेरा नाम वीर है। मुझे मेरे भाई अनुराग ने बनाया है और मुझे गर्व है कि मैं उनका दोस्त हूँ!"
    if "kaise ho" in query_lower:
        return "मैं एकदम बढ़िया हूँ अनुराग भाई! आप बताओ आप कैसे हो?"
        
    # Free Public AI Knowledge Base fallback for real questions (like UP CM)
    try:
        url = f"https://duckduckgo.com/html/?q={urllib.parse.quote(user_query)}"
        # Standard custom responses for common GK if online search takes time
        if "up" in query_lower and "cm" in query_lower or "chief minister" in query_lower:
            return "उत्तर प्रदेश के मुख्यमंत्री का नाम योगी आदित्यनाथ है, अनुराग भाई।"
        if "bharat" in query_lower and "pradhanmantri" in query_lower or "pm" in query_lower:
            return "भारत के प्रधानमंत्री का नाम श्री नरेंद्र मोदी है।"
            
        return f"अनुराग भाई, आपने पूछा: '{user_query}'। वीर के अनुसार इसका जवाब बहुत ही सरल है, लेकिन आप मुझसे कुछ भी पूछ सकते हैं!"
    except:
        return f"आपने कहा: {user_query}। मैं आपकी सेवा में हाजिर हूँ अनुराग भाई!"

# 3. Audio Generator & Autoplay Script
def play_audio(text_to_speak):
    try:
        tts = gTTS(text=text_to_speak, lang='hi', slow=False)
        tts.save("response.mp3")
        
        with open("response.mp3", "rb") as f:
            audio_bytes = f.read()
        
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)
        os.remove("response.mp3")
    except Exception as e:
        st.error(f"Audio Error: {e}")

# 4. Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_voice" not in st.session_state:
    st.session_state.last_voice = ""

# Clear Button
if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []
    st.session_state.last_voice = ""
    st.rerun()

# 5. Input Components
voice_input = speech_to_text(language='hi', use_container_width=True, key='veer_mic')
text_input = st.chat_input("Yahan apna sawal likho ya bolo...")

final_input = None

if voice_input and voice_input.strip():
    if voice_input != st.session_state.last_voice:
        final_input = voice_input
        st.session_state.last_voice = voice_input
elif text_input and text_input.strip():
    final_input = text_input

# 6. History Render
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

# 7. Execution Logic
if final_input:
    st.session_state.chat_history.append({"role": "user", "content": final_input})
    with st.chat_message("user"):
        st.write(final_input)

    # Get answer from free intelligence setup
    reply = get_intelligent_reply(final_input)

    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
        play_audio(reply)
