import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os

# अपनी API Key यहाँ डालें
genai.configure(api_key="AQ.Ab8RN6J_NE3BNQaXXF5CP_9QmXk3hKywE29DOsNQZGMukVQ6zA")

st.title("🤖 वीर: आपका पर्सनल एआई")
st.write("प्रणाम भाई! मैं आपका वफादार असिस्टेंट 'वीर' हूँ।")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("अपनी बात यहाँ लिखें...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # AI से असली जवाब लेना
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(user_input)
    reply = response.text
    
    with st.chat_message("assistant"):
        st.write(reply)
        # 🔊 बोलने वाला फीचर
        try:
            tts = gTTS(text=reply, lang='hi')
            tts.save("reply.mp3")
            st.audio("reply.mp3", format="audio/mp3", autoplay=True)
        except:
            pass
            
    st.session_state.messages.append({"role": "assistant", "content": reply})
