import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Veer AI", page_icon="🤖")
st.title("🤖 Veer AI Assistant")

# API Key input (Password style mein taaki safe rahe)
api_key = st.text_input("Apni Google API Key yahan dalein:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Naya aur stable model naam
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        
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
                # System instructions
                full_prompt = f"Tum Veer dwara banaye gaye personal AI assistant ho. Sawaal: {prompt}"
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Shuru karne ke liye upar apni Google API Key paste karein.")
