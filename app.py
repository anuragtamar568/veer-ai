import streamlit as st
import google.generativeai as genai
import time

# Page Setup
st.set_page_config(page_title="VEER AI | Core Nexus", layout="wide")

# Google AI Configuration
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

# Styling: Ultimate Hacker Terminal Look
st.markdown("""
    <style>
        .stApp { background: #000; color: #00FF00; font-family: 'Courier New', monospace; }
        .stTextInput > div > div > input { background: #0d0d0d; color: #00FF00; border: 1px solid #00FF00; }
        .terminal-box { border: 1px solid #00FF00; padding: 20px; border-radius: 5px; background: #050505; box-shadow: 0 0 10px #00FF00; }
    </style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("## ☣️ SYSTEM ACCESS REQUIRED")
    key = st.text_input("ENTER DECRYPTION KEY", type="password")
    if st.button("INITIATE"):
        if key == "veer123":
            st.session_state.logged_in = True
            st.rerun()
else:
    st.markdown("## ☣️ VEER AI [CORE NEXUS ONLINE]")
    
    # User Input
    user_input = st.text_input("TYPE COMMAND FOR MASTER ANURAG:")
    
    if user_input:
        with st.spinner("Decoding..."):
            # Gemini AI Response
            response = model.generate_content(f"You are VEER AI, a tactical assistant created by Anurag. Answer this in the user's language: {user_input}")
            ans = response.text
            
            # Typewriter Effect
            st.markdown("<div class='terminal-box' id='response'></div>", unsafe_allow_html=True)
            placeholder = st.empty()
            full_text = ""
            for char in ans:
                full_text += char
                placeholder.markdown(f"<div class='terminal-box'>{full_text}█</div>", unsafe_allow_html=True)
                time.sleep(0.01)
            
            # Voice Output
            st.components.v1.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{ans[:200]}'));</script>", height=0)

    if st.button("LOGOUT"):
        st.session_state.logged_in = False
        st.rerun()
