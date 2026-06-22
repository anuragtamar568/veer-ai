import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="VEER AI", layout="centered", initial_sidebar_state="collapsed")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Simplified CSS - No complex quotes
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none !important; }
        .stApp { background-color: #020205 !important; }
        h2, h3, p, div { color: #00ff66 !important; font-family: Courier New !important; }
    </style>
""", unsafe_allow_html=True)

# Main UI
if not st.session_state.logged_in:
    st.markdown("## [ VEER A.I. LOCKED ]")
    password = st.text_input("ENTER KEY", type="password")
    if st.button("UNLOCK"):
        if password == "veer123":
            st.session_state.logged_in = True
            st.rerun()
else:
    st.markdown("### 🔓 VEER A.I. ONLINE")
    
    query = st.text_input("COMMAND:", placeholder="Type here...")
    
    if query:
        reply = "Command executed Master Anurag. My brain was created by you."
        st.markdown(f"🤖 **VEER AI:** {reply}")
        
        # Voice (Simple JS)
        tts_js = f"""
        <script>
            const s = new SpeechSynthesisUtterance("{reply}");
            s.lang = 'en-IN';
            window.speechSynthesis.speak(s);
        </script>
        """
        components.html(tts_js, height=1)

    if st.button("LOGOUT"):
        st.session_state.logged_in = False
        st.rerun()
