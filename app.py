import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="VEER AI | Core Nexus", layout="centered")

# CSS Styling
st.markdown("""
    <style>
        .stApp { background-color: #000000; color: #00FF00; font-family: monospace; }
        .stTextInput > div > div > input { background: #111; color: #0f0; border: 1px solid #0f0; }
        .stButton>button { border: 1px solid #0f0; color: #0f0; background: #000; }
        .terminal-text { color: #00FF00; font-family: monospace; font-size: 18px; }
    </style>
""", unsafe_allow_html=True)

# API Setup
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Secrets setup missing. Check Streamlit Cloud 'Secrets'.")

st.markdown("## 📟 VEER AI [CORE NEXUS]")

query = st.text_input("COMMAND:")

if query:
    try:
        # Prompt Engineering for a tactical assistant role
        full_prompt = f"You are VEER AI, a high-tech assistant created by Anurag. Keep your responses short, tactical, and cool. User asked: {query}"
        response = model.generate_content(full_prompt)
        
        st.markdown(f"<div class='terminal-text'>🤖 VEER: {response.text}</div>", unsafe_allow_html=True)
        
        # Audio Trigger
        audio_js = f"""
        <script>
            var msg = new SpeechSynthesisUtterance("{response.text.replace('"', '')}");
            msg.lang = 'en-US';
            window.speechSynthesis.speak(msg);
        </script>
        """
        st.components.v1.html(audio_js, height=0)
    except Exception as e:
        st.error(f"AI Connection Error: {e}")
