import streamlit as st
import requests
import time
import random

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="VEER AI // MATRIX CORE v5",
    page_icon="🤖",
    layout="wide"
)

# ================= SYSTEM CONFIGURATION =================
SECRET_PASSCODE = "2026"
TIMEOUT_LIMIT = 300  # 5 Minutes Auto-Lock

# ================= SESSION STATE MANAGER =================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_activity" not in st.session_state:
    st.session_state.last_activity = time.time()

# Auto-Lock Logic
if st.session_state.authenticated:
    if time.time() - st.session_state.last_activity > TIMEOUT_LIMIT:
        st.session_state.authenticated = False
        st.rerun()
    st.session_state.last_activity = time.time()

# ================= HI-TECH SCI-FI THEME CSS =================
st.markdown("""
<style>
/* AI Specialist Background & Digital Grid Overlay */
.stApp {
    background: linear-gradient(rgba(0, 5, 2, 0.94), rgba(0, 10, 5, 0.98)), 
                url('https://unsplash.com') no-repeat center center fixed;
    background-size: cover;
}
header { visibility: hidden; }
footer { visibility: hidden; }

/* Glowing Neon Titles */
.main-title {
    text-align: center;
    font-size: 50px;
    font-weight: 900;
    color: #00ff41;
    text-shadow: 0 0 10px #00ff41, 0 0 25px #00ff41, 0 0 40px #00ff22;
    font-family: 'Courier New', Consolas, monospace !important;
    margin-bottom: 20px;
    letter-spacing: 3px;
    animation: glow-pulse 1.5s infinite alternate;
}

@keyframes glow-pulse {
    0% { text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41; }
    100% { text-shadow: 0 0 15px #00ff41, 0 0 35px #00ff41, 0 0 50px #00ff22; }
}

/* Glassmorphism Cyber Sidebar with Box Shadow */
[data-testid="stSidebar"] {
    background: rgba(0, 8, 3, 0.96) !important;
    border-right: 2px solid #00ff41 !important;
    box-shadow: 10px 0 30px rgba(0, 255, 65, 0.2) !important;
}
[data-testid="stSidebar"] * { color: #00ff41 !important; }

/* Sci-Fi Grid Box Template */
.cyber-card {
    background: rgba(0, 12, 4, 0.88);
    border: 2px solid #00ff41;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 25px;
    box-shadow: 0 0 25px rgba(0, 255, 65, 0.2), inset 0 0 15px rgba(0, 255, 65, 0.15);
    backdrop-filter: blur(5px);
}

/* Glowing Chat Messages Blocks */
.stChatMessage {
    background: rgba(0, 8, 2, 0.92) !important;
    border: 1.5px solid rgba(0, 255, 65, 0.4) !important;
    border-left: 6px solid #00ff41 !important;
    border-radius: 10px !important;
    margin-bottom: 15px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.7), 0 0 10px rgba(0, 255, 65, 0.08);
}

/* Glowing Text Engine For Letters */
.shine-text {
    color: #00ff41 !important;
    text-shadow: 0 0 8px #00ff41;
    font-weight: bold;
}

/* Input Fields and Buttons */
[data-testid="stChatInput"] {
    border: 2px solid #00ff41 !important;
    border-radius: 10px !important;
    background-color: #000200 !important;
    box-shadow: 0 0 35px rgba(0, 255, 65, 0.3) !important;
}

input[type="password"] {
    background-color: #000400 !important;
    color: #00ff41 !important;
    border: 2px solid #00ff41 !important;
    box-shadow: 0 0 25px rgba(0, 255, 65, 0.4) !important;
    font-size: 28px !important;
    letter-spacing: 15px !important;
    text-align: center !important;
    border-radius: 8px !important;
}

/* Global Font Override */
p, span, div, label, h1, h2, h3, h4, li, small, button { 
    color: #00ff41 !important; 
    font-family: 'Courier New', Consolas, monospace !important; 
}
</style>
""", unsafe_allow_html=True)

# ================= SCREEN 1: SECURE PASSCODE GATE =================
if not st.session_state.authenticated:
    st.markdown("<h1 class='main-title'>🔒 VEER AI // DECRYPT KEYBOARD</h1>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1.4, 1])
    
    with col2:
        st.markdown("<div class='cyber-card' style='text-align: center;'><h3 style='margin-top:0;'>[ MAIN CORE ACCESS REQUIRED ]</h3><span class='shine-text'>ENTER 4-DIGIT CRYPTO PIN FOR ANURAG SIR</span></div>", unsafe_allow_html=True)
        
        entered_code = st.text_input(
            "KEYWORD:", type="password", max_chars=4, 
            label_visibility="collapsed", key="passcode_widget"
        )
        
        if len(entered_code) == 4:
            if entered_code == SECRET_PASSCODE:
                st.session_state.authenticated = True
                st.session_state.last_activity = time.time()
                st.toast("✔️ CORE UNLOCKED.", icon="🟢")
                st.rerun()
            else:
                st.error("❌ DECRYPTION FAILED // ACCESS DENIED")

# ================= SCREEN 2: MAIN INTERFACE =================
else:
    # --- SIDEBAR DIAGNOSTICS ---
    with st.sidebar:
        st.markdown("# ⚡ VEER AI OS")
        st.success("👤 OWNER: ANURAG SIR")
        st.markdown("---")
        
        selected_mode = st.radio(
            "🧠 SYSTEM ENGINE:",
            ["🟢 CYBER HACKER CORE", "📚 INTELLECT TEACHER CORE"]
        )
        st.markdown("---")
        
        st.markdown("🖥️ **HARDWARE LOGS:**")
        st.caption(f"RAM Block: {random.randint(60, 65)}% | CPU: {random.randint(12, 22)}%")
        st.caption(f"Main Core Temp: {random.randint(40, 44)}°C | Status: ENCRYPTED")
        st.markdown("---")
        
        if st.button("🔒 LOCK TERMINAL", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
        if st.button("🗑️ WIPE MEMORY BARS", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    # --- ADVANCED ENGINE LOGIC ---
    def fetch_smart_response(user_prompt, mode, chat_history):
        if "HACKER" in mode:
            system_instruction = (
                "You are VEER AI, an elite autonomous cyber warfare intelligence custom-coded by 'Anurag Sir'. "
                "Always address the user as 'Anurag Sir' with absolute loyalty. Keep your tone analytical and professional."
            )
        else:
            system_instruction = (
                "You are VEER AI in Teacher Mode. You are a wise technical guide created by your brilliant student 'Anurag Sir'. "
                "Answer educational queries clearly in interactive Hindi/Hinglish."
            )
        
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            url = f"https://googleapis.com{api_key}"
            
            # Continuous conversation packet history formatting
            formatted_contents = []
            for msg in chat_history:
                role_type = "user" if msg["role"] == "user" else "model"
                formatted_contents.append({"role": role_type, "parts": [{"text": msg["content"]}]})
            
            formatted_contents.append({"role": "user", "parts": [{"text": user_prompt}]})
            
            payload = {
                "contents": formatted_contents,
                "system_instruction": {
                    "parts": [{"text": system_instruction}]
                }
            }
            
            response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=15)
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            return "Anurag Sir, मेनफ़्रेम सिगनल डिक्रीज हुआ है। (API Connection Error)"
        except Exception:
            return "Anurag Sir, पैकेट ट्रांसफर टाइमआउट हो गया है। (Server Timeout)"

    # --- MAIN CONSOLE RENDER ---
    st.markdown("<h1 class='main-title'>⚡ VEER AI // ARCHITECT PANEL</h1>", unsafe_allow_html=True)

    status_card_html = f"<div class='cyber-card'><span class='shine-text'>[ ACTIVE STATUS: {selected_mode} ONLINE ]</span><br><small>SECURE COUPLING ACCESSED BY OWNER // ENCRYPTION KEY: AES-256</small></div>"
    st.markdown(status_card_html, unsafe_allow_html=True)

    # Render History
    for msg in st.session_state.messages:
        avatar = "👤" if msg["role"] == "user" else ("🤖" if "HACKER" in selected_mode else "👨‍🏫")
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # Chat Input Box
    input_hint = "Execute hacker query, Anurag Sir..." if "HACKER" in selected_mode else "Ask educational terminal, Anurag Sir..."
    prompt = st.chat_input(input_hint)

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
            
        with st.chat_message("assistant", avatar="🤖" if "HACKER" in selected_mode else "👨‍🏫"):
            with st.spinner("⚡ DECRYPTING RESPONSES..."):
                reply = fetch_smart_response(prompt, selected_mode, st.session_state.messages[:-1])
                st.markdown(reply)
                
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()
