import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Veer AI", page_icon="🤖")
st.title("🤖 Veer AI Assistant")

# Pehle API Key mangna zaroori hai
api_key = st.text_input("Apni Google API Key yahan paste karein:", type="password")

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
                # Yahan humne aapka naam set kar diya hai
                response = model.generate_content(f"Tum ek assistant ho jise Veer ne banaya hai. Sawaal: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.write("Shuru karne ke liye upar apni API key dalein.")
