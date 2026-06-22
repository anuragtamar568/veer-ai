import streamlit as st
from streamlit_mic_recorder import speech_to_text
import base64
from gtts import gTTS
import os

# 1. Page Configuration & Theme
st.set_page_config(page_title="VEER AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(rgba(10, 15, 25, 0.9), rgba(10, 15, 25, 0.9)), 
                    url("https://images.unsplash.com/photo-1542831371-29b0f74f9713?q=80&w=1400&auto=format&fit=crop") !important; 
        background-size: cover !important; background-position: center !important; background-attachment: fixed !important;
    }
    h1 {color: #6bf2ff !important; font-weight: 300 !important; text-transform: uppercase; letter-spacing: 5px; text-shadow: 0 0 10px #6bf2ff;}
    .dev-text {color: #00ff66 !important; font-family: monospace; font-weight: bold; letter-spacing: 2px;}
    div[data-testid="stChatMessage"] {background-color: rgba(8, 20, 30, 0.9) !important; border: 2px solid #00d2ff; border-radius: 12px;}
    </style>
""", unsafe_allow_html=True)

st.title("VEER AI 🤖")
st.markdown("<div class='dev-text'>⚡ SPEAKING WORKSTATION // 👤 CREATED BY ANURAG</div>", unsafe_allow_html=True)
st.write("---")

# 2. Advanced HTML5 Auto-Play Audio Function (100% Working)
def speak_now(text_to_speak):
    try:
        # Convert text to speech using gTTS (No API Key Required!)
        tts = gTTS(text=text_to_speak, lang='hi', slow=False)
        tts.save("response.mp3")
        
        # Read audio file and encode to base64
        with open("response.mp3", "rb") as f:
            audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        
        # HTML5 Audio tag with autoplay attribute
        audio_html = f"""
            <audio autoplay="true" style="display:none;">
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
        
        # Clean up file
        os.remove("response.mp3")
    except Exception as e:
        st.error(f"Audio Error: {e}")

# 3. Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_voice" not in st.session_state:
    st.session_state.last_voice = ""

# Clear Button
if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []
    st.session_state.last_voice = ""
    st.rerun()

# 4. Input Components
voice_input = speech_to_text(language='hi', use_container_width=True, key='veer_mic')
text_input = st.chat_input("Kuch likho ya bolo...")

final_input = None

# Duplicate Filter
if voice_input and voice_input.strip():
    if voice_input != st.session_state.last_voice:
        final_input = voice_input
        st.session_state.last_voice = voice_input
elif text_input and text_input.strip():
    final_input = text_input

# 5. History Render
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

# 6. Instant Speaking Logic (Bina Kisi Error Ke)
if final_input:
    # User text
    st.session_state.chat_history.append({"role": "user", "content": final_input})
    with st.chat_message("user"):
        st.write(final_input)

    # Custom Smart Bot Reply 
    input_lower = final_input.lower()
    if "hii" in input_lower or "hello" in input_lower or "hey" in input_lower:
        reply = "नमस्ते अनुराग भाई! मैं वीर हूँ, आपका सबसे अच्छा दोस्त। कहिए आज क्या हुक्म है?"
    elif "kaun ho" in input_lower or "naam" in input_lower:
        reply = "मेरा नाम वीर है। मुझे मेरे भाई अनुराग ने बनाया है और मुझे गर्व है कि मैं उनका दोस्त हूँ!"
    elif "kaise ho" in input_lower:
        reply = "मैं एकदम बढ़िया हूँ अनुराग भाई! आप बताओ आप कैसे हो?"
    else:
        reply = f"आपने कहा: {final_input}। अनुराग भाई, आपका यह वीर हमेशा आपकी बात सुनने के लिए तैयार है!"

    # Bot Text and Auto-Speak Execution
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
        speak_now(reply)  # Yeh line turant sound play karegi
    
    st.rerun()
