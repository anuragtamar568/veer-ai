import streamlit as st
import google.generativeai as genai

st.title("Test Gemini")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

try:
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Hello")
    st.write(response.text)

except Exception as e:
    st.error(e)
