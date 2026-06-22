import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Veer AI", page_icon="🤖")
st.title("🤖 Veer AI Assistant")

# Hum yahan 'st.text_input' use kar rahe hain
# Ye code wahan 'Secrets' wali error nahi dega
api_key = st.text_input("Apni Google API Key yahan dalein:", type="password")

if api_key:
    try:
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
                response = model.generate_content(f"Tum ek personal assistant ho jise Veer ne banaya hai. Sawaal: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Shuru karne ke liye upar apni Google API Key paste karein.")
