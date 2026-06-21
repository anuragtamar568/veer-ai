import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os

# अपनी API Key यहाँ पेस्ट करें
genai.configure(api_key="AQ.Ab8RN6J_NE3BNQaXXF5CP_9QmXk3hKywE29DOsNQZGMukVQ6zA")

# मॉडल सेटअप
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🤖 वीर: आपका पर्सनल एआई")

if "messages" not in st.session_state:
    st.session_state.messages = []

# चैट हिस्ट्री
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# इनपुट
if user_input := st.chat_input("वीर से कुछ पूछें..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("with st.chat_message("assistant"):
        # पहले reply को खाली सेट कर दें
        reply = "क्षमा करें भाई, अभी जवाब नहीं मिल पा रहा है।"
        
        try:
            response = model.generate_content(user_input)
            reply = response.text
            st.write(reply)
            
            # आवाज़ जनरेट करना
            tts = gTTS(text=reply, lang='hi')
            tts.save("reply.mp3")
            st.audio("reply.mp3", format="audio/mp3", autoplay=True)
        except Exception as e:
            st.write("भाई, कुछ तकनीकी दिक्कत आ रही है।")
            with st.chat_message("assistant"):
            # यहाँ reply को पहले खाली सेट करें
            reply = "क्षमा करें भाई, अभी जवाब नहीं मिल पा रहा है।"
            
            try:
                response = model.generate_content(user_input)
                reply = response.text
                st.write(reply)
                
                # आवाज़ जनरेट करना
                tts = gTTS(text=reply, lang='hi')
                tts.save("reply.mp3")
                st.audio("reply.mp3", format="audio/mp3", autoplay=True)
            except Exception as e:
                st.write("भाई, कुछ तकनीकी दिक्कत आ रही है।")
                st.write(e)
            
            # अब यह लाइन 'with' ब्लॉक के अंदर है
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.write(f"Error details: {e}")
            
    # अब ये लाइन यहाँ होने पर एरर नहीं देगी
    st.session_state.messages.append({"role": "assistant", "content": reply})"):
        # AI से जवाब
        try:
            response = model.generate_content(user_input)
            reply = response.text
            st.write(reply)
            
            # आवाज़ जनरेट करना
            tts = gTTS(text=reply, lang='hi')
            tts.save("reply.mp3")
            st.audio("reply.mp3", format="audio/mp3", autoplay=True)
        except Exception as e:
            st.write("भाई, कुछ तकनीकी दिक्कत आ रही है।")
            st.write(e)
            
    st.session_state.messages.append({"role": "assistant", "content": reply})
