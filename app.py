import streamlit as st
import google.generativeai as genai

# Page setup
st.set_page_config(page_title="Veer AI", page_icon="🤖")
st.title("🤖 Veer AI Assistant")
st.write("Main Veer dwara banaya gaya AI hoon.")

# Secrets se API Key uthao (Input box hat gaya hai)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error("API Key set nahi hai. 'Manage App' -> 'Settings' -> 'Secrets' mein jaakar GOOGLE_API_KEY add karein.")
    st.stop()

# Chat history handle karein
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani chats dikhayein
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User ka input
if prompt := st.chat_input("Mujhse kuch puchiye..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Personal instruction
        full_prompt = f"Tumhe Veer ne banaya hai. Hamesha apna naam Veer AI batana. Sawaal: {prompt}"
        try:
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("AI jawab dene mein asamarth hai. API key check karein.")
