import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="VEER AI", layout="centered")

# Safe API Key Loading
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Configuration Error: {e}")
    st.stop()

# UI Styles
st.markdown("<style>.stApp {background:#000; color:#0f0; font-family:monospace;}</style>", unsafe_allow_html=True)

if "logged_in" not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    key = st.text_input("ENTER KEY", type="password")
    if st.button("UNLOCK"):
        if key == "veer123":
            st.session_state.logged_in = True
            st.rerun()
else:
    query = st.text_input("COMMAND:")
    if query:
        try:
            # Response generation
            response = model.generate_content(f"You are VEER AI, assistant of Anurag. Reply: {query}")
            ans = response.text
            st.write(f"🤖: {ans}")
        except Exception as e:
            st.error(f"Gemini API Error: {e}")
