import streamlit as st
import google.generativeai as genai

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="VEER AI", page_icon="⚡", layout="wide")

# =========================
# THEME STYLING
# =========================
st.markdown("""
<style>
.stApp{ background: linear-gradient(135deg, #020617, #0f172a, #000000); }
section[data-testid="stSidebar"]{ background:#050505; border-right:1px solid #00ff88; }
.glow-title{
    text-align:center; font-size:60px; font-weight:800;
    background:linear-gradient(90deg, #00ff88, #00ffff, #00ff88);
    background-size:200% auto; -webkit-background-clip:text;
    -webkit-text-fill-color:transparent; animation:shine 3s linear infinite;
}
@keyframes shine{ to{ background-position:200% center; } }
.subtitle{ text-align:center; color:#00ff88; font-size:18px; margin-bottom:25px; text-shadow: 0 0 10px #00ff88; }
[data-testid="stChatMessage"]{ background:rgba(0,255,136,0.05); border:1px solid rgba(0,255,136,0.25); border-radius:18px; }
.stChatInputContainer{ border:2px solid #00ff88; border-radius:20px; }
.stButton button{ background:#00ff88 !important; color:black !important; font-weight:bold !important; }
p,span,div{ color:#f8fafc !important; }
</style>
""", unsafe_allow_html=True)

# =========================
# GEMINI INITIALIZATION
# =========================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# System instructions to define persona
system_prompt = """
You are VEER AI X. 
- Never say you are Google Gemini.
- Understand and communicate in Hindi, English, and Hinglish.
- Reply in the same language used by the user.
- Be friendly, intelligent, and concise for simple questions.
- Provide detailed answers only when necessary.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_prompt
)

# =========================
# MEMORY & SESSION
# =========================
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# =========================
# SIDEBAR
# =========================
st.sidebar.title("⚡ VEER AI X")
if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.chat = model.start_chat(history=[])
    st.rerun()

# =========================
# HEADER
# =========================
st.markdown('<h1 class="glow-title">⚡ VEER AI X ⚡</h1>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">🚀 Hindi • English • Hinglish • Smart AI</div>', unsafe_allow_html=True)

# =========================
# CHAT INTERFACE
# =========================
# Display existing history
for message in st.session_state.chat.history:
    with st.chat_message(message.role):
        st.markdown(message.parts[0].text)

# Handle new user input
if prompt := st.chat_input("Ask Anything..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    try:
        with st.chat_message("assistant"):
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
    except Exception as e:
        st.error(f"Error: {e}")
