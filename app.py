import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="Veer AI", page_icon="🤖")

st.title("🤖 Veer AI Assistant")
st.write("Main aapka personal assistant hoon, jise aapne banaya hai.")

# API Key setup (Streamlit secrets mein save karna best hai)
api_key = st.text_input("Apni Google API Key dalein:", type="password")

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
            response = model.generate_content(f"Tum Veer dwara banaye gaye ho. {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
