import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="VEER AI", layout="centered")

# API Setup
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash') # Naya model
except Exception as e:
    st.error("API Key ka issue hai, check karo.")

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
            response = model.generate_content(f"You are VEER AI, assistant of Anurag. Reply: {query}")
            st.write(f"🤖: {response.text}")
        except Exception as e:
            st.write("Error aaya: ", e)
