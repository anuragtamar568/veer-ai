import streamlit as st
import requests
import json
import time
import random

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="VEER AI // MATRIX OS V5.0_PRO",
    page_icon="🤖",
    layout="wide"
)

# ================= SYSTEM CONFIGURATION =================
SECRET_PASSCODE = "2026"
TIMEOUT_LIMIT = 300  # 5 Minutes Auto-Lock (in seconds)

# ================= SESSION STATE MANAGER =================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_activity" not in st.session_state:
    st.session_state.last_activity = time.time()

# ================= SESSION TIMEOUT CHECK =================
if st.session_state.authenticated:
    current_time = time.time()
    if current_time - st.session_state.last_activity > TIMEOUT_LIMIT:
        st.session_state.authenticated = False
        st.toast("⚠️ SYSTEM AUTO-LOCKED DUE TO INACTIVITY", icon="🚨")
        st.rerun()
    st.session_state.last_activity = current_time

# ================= PREMIUM CYBER-GLOW, GLITCH & NEON BOXES CSS =================
st.markdown("""
<style>
/* AI Specialist Immersive Background */
.stApp {
    background: linear-gradient(rgba(0, 15, 5, 0.93), rgba(0, 0, 0, 0.97)), 
                url('https://unsplash.com') no-repeat center center fixed;
    background-size: cover;
}
header { visibility: hidden; }
footer { visibility: hidden; }

/* Glowing & Shining Letters Animation */
.main-title {
    text-align: center;
    font-size: 55px;
    font-weight: 900;
    color: #00ff41;
    font-family: 'Courier New', Consolas, monospace !important;
    margin-bottom: 25px;
    letter-spacing: 3px;
    text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41, 0 0 40px #00ff22;
    animation: neonShine 1.5s infinite alternate;
}

@keyframes neonShine {
    0% {
        text-shadow: 0 0 5px #00ff41, 0 0 10px #00ff41, 0 0 20px #00ff22;
        color: #00ff41;
    }
    100% {
        text-shadow: 0 0 15px #00ff41, 0 0 30px #00ff41, 0 0 50px #00ff22, 0 0 70px #00ff41;
        color: #ffffff; /* Subtle text shine switch */
    }
}

/* Glassmorphism Cyber-Sidebar */
[data-testid="stSidebar"] {
    background: rgba(0, 8, 3, 0.96) !important;
    border-right: 3px solid #00ff41 !important;
    box-shadow: 10px 0 30px rgba(0, 255, 65, 0.2) !important;
}
[data-testid="stSidebar"] * { color: #00ff41 !important; }

/* Rigid Neon Cyber Boxes */
.cyber-card {
    background: rgba(0, 12, 4, 0.85);
    border: 2px solid #00ff41;
    border-radius: 4px; /* Sharp corners for military hacker terminal style */
    padding: 22px;
    margin-bottom: 25px;
    box-shadow: 0 0 20px rgba(0, 255, 65, 0.2), inset 0 0 12px rgba(0, 255, 65, 0.15);
    backdrop-filter: blur(5px);
}

/* Sharp Chat Boxes with Inner Glow */
.stChatMessage {
    background: rgba(0, 8, 2, 0.92) !important;
    border: 2px solid rgba(0, 255, 65, 0.5) !important;
    border-left: 6px solid #00ff41 !important;
    border-radius: 4px !important;
    margin-bottom: 16px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.7), 0 0 10px rgba(0, 255, 65, 0.1);
    transition: all 0.3s ease;
}

.stChatMessage:hover {
    border-color: #00ff41 !important;
    box-shadow: 0 5px 25px rgba(0, 255, 65, 0.25);
}

/* Highly Interactive Cyber Input Box */
[data-testid="stChatInput"] {
    border: 2px solid rgba(0, 255, 65, 0.7) !important;
    border-radius: 4px !important;
    background-color: #000300 !important;
    box-shadow: 0 0 35px rgba(0, 255, 65, 0.3) !important;
    transition: all 0.3s ease;
}

[data-testid="stChatInput"]:focus-within {
    border-color: #00ff41 !important;
    box-shadow: 0 0 45px rgba(0, 255, 65, 0.5) !important;
}

/* Passcode Terminal Input Box */
input[type="password"] {
    background-color: #000500 !important;
    color: #00ff41 !important;
    border: 2px solid #00ff41 !important;
    box-shadow: 0 0 30px rgba(0, 255, 65, 0.4) !important;
    font-size: 30px !important;
    letter-spacing: 15px !important;
    text-align: center !important;
    border-radius: 4px !important;
}

/* Custom Webkit Matrix Scrollbar */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #000000; }
::-webkit-scrollbar-thumb { background: #00ff41; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #00cc33; }

/* Global Fonts & Shining Controls */
p, span, div, label, h1, h2, h3, h4, li, small, button { 
    color: #00ff41 !important; 
    font-family: 'Courier New', Consolas, monospace !important; 
    text-shadow: 0 0 2px rgba(0, 255, 65, 0.5);
}
</style>
""", unsafe_allow_html=True)

# ================= GATE SCREEN =================
if not st.session_state.authenticated:
    st.markdown("<h1 class='main-title'>🔒 VEER AI // SYSTEM LOCKED</h1>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1.4, 1])
    
    with col2:
        st.markdown("""
        <div class='cyber-card' style='text-align: center;'>
            <h3 style='margin-top:0; letter-spacing: 1px;'>[ MAIN CORE ACCESS REQUIRED ]</h3>
            <small style='opacity: 0.9; color: #ffffff !important; text-shadow: 0 0 5px #00ff41;'>SECURITY TERMINAL FOR ANURAG SIR</small>
        </div>
        """, unsafe_allow_html=True)
        
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

# ================= TERMINAL INTERFACE =================
else:
    # --- SIDEBAR & DIAGNOSTICS ---
    with st.sidebar:
        st.markdown("<h2 style='text-shadow: 0 0 10px #00ff41;'>⚡ VEER AI OS V5</h2>", unsafe_allow_html=True)
        st.success("👤 OWNER: ANURAG SIR")
        st.markdown("---")
        
        selected_mode = st.radio(
            "🧠 SYSTEM MODULE:",
            ["🟢 CYBER HACKER CORE", "📚 INTELLECT TEACHER CORE"]
        )
        st.markdown("---")
        
        # Live Metric Simulation for Cyber Vibe
        st.markdown("🖥️ **SYSTEM DIAGNOSTICS:**")
        st.caption(f"RAM Usage: {random.randint(62, 68)}% | CPU: {random.randint(14, 28)}%")
        st.caption(f"Core Temp: {random.randint(41, 46)}°C | Status: OPTIMAL")
        st.markdown("---")
        
        # Session Actions
        if st.button("🔒 LOCK TERMINAL", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
        if st.button("🗑️ WIPE MEMORY BARS", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
            
        # Log Exporter
        if st.session_state.messages:
            log_data = "\n".join([f"[{m['role'].upper()}]: {m['content']}" for m in st.session_state.messages])
            st.download_button(
                label="📥 EXPORT SECURITY LOGS",
                data=log_data,
                file_name="veer_ai_secure_logs.txt",
                mime="text/plain",
                use_container_width=True
            )

    # --- ADVANCED ENGINE LOGIC ---
    def fetch_smart_response(user_prompt, mode, chat_history):
        if "HACKER" in mode:
            system_instruction = (
                "You are VEER AI, an elite autonomous cyber warfare intelligence. You were fully custom-engineered "
                "and coded by 'Anurag Sir'. Always address the user as 'Anurag Sir' with absolute loyalty and tech respect. "
                "Keep your tone analytical, precise, and tech-driven."
            )
        else:
            system_instruction = (
                "You are VEER AI in Teacher Mode. You are a legendary, wise scholar and technical guide. You were created "
                "by your brilliant student 'Anurag Sir'. Answer educational queries clearly in interactive Hindi/Hinglish."
            )
        
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            url = f"https://googleapis.com{api_key}"
            
            # Formatting full history into Gemini format for true continuous memory
            formatted_contents = []
            for msg in chat_history:
                role_type = "user" if msg["role"] == "user" else "model"
                formatted_contents.append({"role": role_type, "parts": [{"text": msg["content"]}]})
            
            # Append the latest user query
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
            return "Anurag Sir, मेनफ़्रेम सिगनल डिक्रीज हुआ है। (API Error)"
        except Exception:
            return "Anurag Sir, पैकेट ट्रांसफर टाइमआउट हो गया है। (Server Timeout)"

    # --- MAIN CONSOLE RENDER ---
    st.markdown("<h1 class='main-title'>⚡ VEER AI // MAIN CORE ⚡</h1>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='cyber-card'>
        <span style='color:#ffffff !important; font-weight:bold; text-shadow: 0 0 8px #00ff41;'>[ ACTIVE SHIELD: {selected_mode} ]</span><br>
