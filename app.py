import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Veer AI", page_icon="🤖")
st.title("🤖 Veer AI Assistant")

# API Key input
api_key = st.text_input("Apni Google API Key yahan paste karein:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # Naya model use karein jo abhi active hai
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Purani baatein dikhayein
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # User ka input
        if prompt := st.chat_input("Mujhse kuch puchiye..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                # System prompt fix kiya gaya hai
                full_prompt = f"Tum ek personal assistant ho jise Veer ne banaya hai. Sawaal: {prompt}"
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"Error: {e}. (Tip: Agar error aaye toh apni API key check karein ki wo Google AI Studio mein active hai.)")
else:
    st.info("Shuru karne ke liye upar apni API key dalein.")
