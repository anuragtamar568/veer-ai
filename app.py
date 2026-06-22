import streamlit as st
import streamlit.components.v1 as components
import random

# Page Setup
st.set_page_config(page_title="VEER AI | Core Nexus", layout="wide")

# Theme: Full Hacker Dark Mode
st.markdown("""
    <style>
        .stApp { background: #000000; color: #00FF00; font-family: 'Courier New', Courier, monospace; }
        .stTextInput > div > div > input { background: #0d0d0d; color: #00FF00; border: 1px solid #00FF00; }
        .stButton>button { background: #000; color: #00FF00; border: 1px solid #00FF00; }
        .stButton>button:hover { background: #00FF00; color: #000; }
        .terminal-box { border: 1px solid #00FF00; padding: 20px; border-radius: 5px; background: #050505; }
    </style>
""", unsafe_allow_html=True)

# State
if "logged_in" not in st.session_state: st.session_state.logged_in = False

# Login Logic
if not st.session_state.logged_in:
    st.markdown("## ☣️ SYSTEM ACCESS REQUIRED")
    key = st.text_input("ENTER DECRYPTION KEY", type="password")
    if st.button("INITIATE"):
        if key == "veer123":
            st.session_state.logged_in = True
            st.rerun()
else:
    st.markdown("## 📟 VEER AI [ACTIVE]")
    
    # JavaScript for Voice & AI Power
    components.html("""
        <div class="terminal-box">
            <button id="mic-btn" style="background:transparent; color:#00FF00; border:1px solid #00FF00; padding:10px;">🎙️ VOICE COMMAND</button>
            <p id="status">System Ready, Master Anurag...</p>
        </div>
        <script>
            const btn = document.getElementById('mic-btn');
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.onresult = (event) => {
                const text = event.results[0][0].transcript;
                document.getElementById('status').innerText = 'Command: ' + text;
                const msg = new SpeechSynthesisUtterance('Yes Master Anurag, executing ' + text);
                window.speechSynthesis.speak(msg);
            };
            btn.onclick = () => recognition.start();
        </script>
    """, height=150)

    query = st.text_input("TYPE COMMAND:")
    if query:
        response = f"Processing '{query}'... Master Anurag, your AI is fully operational."
        st.markdown(f"<div class='terminal-box'>🤖 {response}</div>", unsafe_allow_html=True)
        # Voice Auto-trigger
        components.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{response}'));</script>", height=0)

    if st.button("LOGOUT"):
        st.session_state.logged_in = False
        st.rerun()
