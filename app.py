import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import base64

st.set_page_config(page_title="Veer AI", page_icon="🤖")
st.title("🤖 Veer AI Assistant")

# API Key input
api_key = st.text_input("Apni Google API Key yahan dalein:", type="password")

# Voice function
def play_voice(text):
    tts = gTTS(text=text, lang='hi')
    tts.save("response.mp3")
    audio_file = open("response.mp3", "rb")
    audio_bytes = audio_file.read()
    b64 = base64.b64encode(audio_bytes).decode()
    audio_html = f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}"></audio>'
    st.markdown(audio_html, unsafe_allow_html=True)

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Mujhse kuch puchiye..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = model.generate_content(f"Tum Veer ho. Sawaal: {prompt}")
            st.markdown(response.text)
            play_voice(response.text) # Yahan se voice play hogi
            st.session_state.messages.append({"role": "assistant", "content": response.text})
