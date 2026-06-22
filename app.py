import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS # यह नई लाइन है
import os

# ... (बाकी CSS और हेडर कोड वैसा ही रहेगा) ...

# AI रिस्पांस के साथ ऑडियो जोड़ने का नया फंक्शन
def speak_text(text):
    tts = gTTS(text=text, lang='hi')
    tts.save("response.mp3")
    audio_file = open("response.mp3", "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")

# ... (कोड का बाकी हिस्सा) ...

    # जहाँ AI का जवाब आता है, वहां इसे कॉल करें:
    if found_app:
        with st.chat_message("assistant", avatar="🤖"):
            st.write(found_app["text"])
            st.link_button(found_app["btn"], found_app["url"])
            speak_text(found_app["text"]) # यह लाइन ऑडियो प्ले कर देगी
        st.session_state.messages.append({...})

    else:
        with st.chat_message("assistant", avatar="🤖"):
            # ... (ट्राई ब्लॉक के अंदर)
                response = model.generate_content(prompt)
                placeholder.markdown(response.text)
                speak_text(response.text) # यहाँ भी बोलकर सुनाएगा
                st.session_state.messages.append({"role": "assistant", "content": response.text})
