import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os

# अपनी API Key यहाँ डालें
genai.configure(api_key="AQ.Ab8RN6J_NE3BNQaXXF5CP_9QmXk3hKywE29DOsNQZGMukVQ6zA")

# मॉडल का नाम (Gemini 1.5 Flash बहुत तेज है)
model = genai.GenerativeModel('gemini-pro')

st.title("🤖 वीर: आपका पर्सनल एआई")
st.write("प्रणाम भाई! मैं आपका वफादार असिस्टेंट 'वीर' हूँ।")

# चैट हिस्ट्री शुरू करें
if "messages" not in st.session_state:
    st.session_state.messages = []

# पुरानी चैट दिखाएं
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# यूजर का इनपुट लें
if user_input := st.chat_input("अपनी बात यहाँ लिखें..."):
    # यूजर का मैसेज दिखाएं
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # असिस्टेंट का जवाब
    with st.chat_message("assistant"):
        reply = "क्षमा करें, मैं अभी जवाब नहीं दे पा रहा हूँ।"
        try:
            # AI से जवाब लें
            response = model.generate_content(user_input)
            reply = response.text
            st.write(reply)
            
            # आवाज़ में सुनाएं
            tts = gTTS(text=reply, lang='hi')
            tts.save("reply.mp3")
            st.audio("reply.mp3", format="audio/mp3", autoplay=True)
            
        except Exception as e:
            st.write("भाई, कुछ तकनीकी दिक्कत आ रही है।")
            st.write(f"Error: {e}")
            
    # चैट हिस्ट्री में सेव करें
    st.session_state.messages.append({"role": "assistant", "content": reply})
