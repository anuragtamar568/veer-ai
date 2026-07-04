import streamlit as st
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="VEER AI",
    page_icon="🤖",
    layout="wide"
)

# ---------------- SESSION ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f172a, #1e293b); }
.main-title { text-align: center; color: white; font-size: 40px; font-weight: 800; margin-bottom: 5px; }
.subtitle { text-align: center; color: #94a3b8; margin-bottom: 25px; }
[data-testid="stSidebar"] { background: #020617; }
.stChatMessage { border-radius: 12px; background: rgba(255,255,255,0.05); }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h1 class='main-title'>🤖 VEER AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Powered by Gemini 2.5 Flash</p>", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Settings")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.success("Gemini 2.5 Flash is Active")

# ---------------- GEMINI FUNCTION ----------------
def get_gemini_response(prompt):
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return "Error: API Key not found in secrets."
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        return f"API Error ({response.status_code}): {response.text}"
    except Exception as e:
        return f"Connection Error: {str(e)}"

# ---------------- CHAT HISTORY ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- INPUT ----------------
if prompt := st.chat_input("Type your message here..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("VEER is thinking..."):
            reply = get_gemini_response(prompt)
            st.markdown(reply)
    
    st.session_state.messages.append({"role": "assistant", "content": reply})
