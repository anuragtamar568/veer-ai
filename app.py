import streamlit as st
import google.generativeai as genai

# Page setup
st.set_page_config(page_title="Veer AI", page_icon="🤖")
st.title("🤖 Veer AI Assistant")

# Secret se API key uthao
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error("API Key secrets mein set nahi hai.")
    st.stop()

# Baaki code...
