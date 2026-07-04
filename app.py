import streamlit as st
import requests
import PyPDF2

# 1. Page Config
st.set_page_config(page_title="VEER AI Pro", page_icon="🤖", layout="wide")

# 2. Simple Authentication Logic
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login_screen():
    st.markdown("<h1 style='text-align: center;'>VEER AI - Login</h1>", unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # Yahan aap apne credentials set karein
        if username == "admin" and password == "veer123":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid Username or Password")

# 3. Main App Logic
def main_app():
    st.markdown("<h1 class='main-title'>🤖 VEER AI Pro</h1>", unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.title("⚙️ Controls")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()
        
        uploaded_file = st.file_uploader("Upload PDF for AI to read", type="pdf")
        doc_text = ""
        if uploaded_file:
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                doc_text += page.extract_text()
            st.success("File uploaded!")

    # Chat UI
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Ask VEER AI..."):
        # Context management
        full_prompt = f"Context: {doc_text[:2000]} \n\n User Question: {prompt}" if doc_text else prompt
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Gemini API call
                api_key = st.secrets.get("GEMINI_API_KEY")
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                response = requests.post(url, json={"contents": [{"parts": [{"text": full_prompt}]}]})
                
                if response.status_code == 200:
                    reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    reply = "Error: Could not connect to AI."
                
                st.write(reply)
        
        st.session_state.messages.append({"role": "assistant", "content": reply})

# 4. Routing
if st.session_state.authenticated:
    main_app()
else:
    login_screen()
