import streamlit as st
from gtts import gTTS
import os

# ऐप का टाइटल
st.title("🤖 वीर: आपका पर्सनल एआई")
st.write("प्रणाम भाई! मैं आपका वफादार असिस्टेंट 'वीर' हूँ। कमांड दीजिए!")

# चैट हिस्ट्री के लिए सेशन स्टेट
if "messages" not in st.session_state:
    st.session_state.messages = []

# पुरानी चैट स्क्रीन पर दिखाना
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# यूज़र से इनपुट लेना
user_input = st.chat_input("यहाँ अपनी कमांड लिखें भाई...")

if user_input:
    # यूज़र का मैसेज स्क्रीन पर दिखाना
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # वीर का जवाब तैयार करना
    reply = f"जी भाई, आपने कहा '{user_input}'। मैंने आपकी कमांड नोट कर ली है और मैं इसपर काम कर रहा हूँ!"
    
    # वीर का जवाब स्क्रीन पर दिखाना
    with st.chat_message("assistant"):
        st.write(reply)
        
        # 🔊 यहाँ आवाज़ जनरेट हो रही है
        try:
            tts = gTTS(text=reply, lang='hi')
            tts.save("reply.mp3")
            # ऑडियो प्लेयर दिखाना जो अपने आप प्ले हो जाएगा
            st.audio("reply.mp3", format="audio/mp3", autoplay=True)
        except Exception as e:
            st.error("आवाज़ जनरेट करने में थोड़ी दिक्कत हुई भाई!")
            
    st.session_state.messages.append({"role": "assistant", "content": reply})
