import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="VEER AI", layout="centered")

# API Setup - Robust
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # 'gemini-pro' har jagah support karta hai
    model = genai.GenerativeModel('gemini-pro') 
except Exception as e:
    st.error("API Key ka issue hai. Secrets check karo.")

st.markdown("<style>.stApp {background:#000; color:#0f0; font-family:monospace;}</style>", unsafe_allow_html=True)

st.markdown("## 📟 VEER AI [CORE NEXUS]")
query = st.text_input("COMMAND:")

if query:
    try:
        # Prompt
        response = model.generate_content(f"You are VEER AI, assistant of Anurag. Reply: {query}")
        st.write(f"🤖: {response.text}")
    except Exception as e:
        st.error(f"Error: {e}")
