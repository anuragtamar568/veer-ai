import streamlit as st
from google import genai
from gtts import gTTS
import os

# नया क्लाइंट सेटअप
client = genai.Client(api_key="AQ.Ab8RN6J_NE3BNQaXXF5CP_9QmXk3hKywE29DOsNQZGMukVQ6zA")

st.title("🤖 वीर: आपका पर्सनल एआई")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if user_input := st.chat_input("वीर से कुछ पूछें..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        try:
            # नए क्लाइंट का उपयोग
            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=user_input
            )
            reply = response.text
            st.write(reply)
            
            tts = gTTS(text=reply, lang='hi')
            tts.save("reply.mp3")
            st.audio("reply.mp3", format="audio/mp3", autoplay=True)
            
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.write("भाई, अभी कुछ तकनीकी दिक्कत है।")
            st.write(f"Error: {e}")
