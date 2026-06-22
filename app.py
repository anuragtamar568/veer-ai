if api_key:
    genai.configure(api_key=api_key)
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        # Yahan ek test call karein
        response = model.generate_content(f"Tum Veer dwara banaye gaye ho. {prompt}")
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error: {e}. Check karein ki API Key sahi hai ya nahi.")
