import streamlit as st
import requests
import PyPDF2

# 1. Page Configuration
st.set_page_config(page_title="VEER AI Pro", page_icon="🤖", layout="wide")

# 2. Custom Modern CSS
st.markdown("""
<style>
    .main { background-color: #0f172a; }
    .stChatMessage { border-radius: 15px; background: rgba(255, 255, 255, 0.05); }
    .stAppHeader { background: transparent; }
    h1 { color: #38bdf8; text-align: center; }
</style>
""", unsafe_allow_html=True)

# 3. Session State Init
if "authenticated" not in st.session_state: st.session_state.authenticated = False
if "messages" not in st.session_state: st.session_state.messages = []

# 4. Auth Screen
def login_screen():
    st.markdown("<h1>🔒 VEER AI Access</h1>", unsafe_allow_html=True)
    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            user = st.text_input("Username")
            pswd = st.text_input("Password", type="password")
            if st.button("Secure Login"):
                if user == "admin" and pswd == "veer123":
                    st.session_state.authenticated = True
                    st.rerun()
                else: st.error("Access Denied!")

# 5. Main App
def main_app():
    st.sidebar.title("🚀 VEER AI Controls")
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
    
    uploaded_file = st.sidebar.file_uploader("Upload Knowledge Base (PDF)", type="pdf")
    
    st.markdown("<h1>🤖 VEER AI Pro</h1>", unsafe_allow_html=True)

    # Chat logic
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask your assistant..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                api_key = st.secrets.get("GEMINI_API_KEY")
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                
                # Simple Request
                res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
                reply = res.json()["candidates"][0]["content"]["parts"][0]["text"] if res.status_code == 200 else "API Error."
                
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

if st.session_state.authenticated: main_app()
else: login_screen()
