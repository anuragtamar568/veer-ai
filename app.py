import streamlit as st
import requests
import json
import time
import random

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="VEER AI // OS V4.0_PRO",
    page_icon="⚡",
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

# ================= MATRIX/CYBERPUNK GLOW CSS =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(rgba(0, 8, 0, 0.94), rgba(0, 0, 0, 0.98)), 
                url('https://unsplash.com') no-repeat center center fixed;
    background-size: cover;
}
header { visibility: hidden; }
footer { visibility: hidden; }

.main-title {
    text-align: center;
    font-size: 50px;
    font-weight: 900;
    color: #00ff41;
    text-shadow: 0 0 10px #00ff41, 0 0 25px #00ff41;
    font-family: 'Courier New', Consolas, monospace !important;
    margin-bottom: 20px;
}

[data-testid="stSidebar"] {
    background: rgba(0, 5, 0, 0.97) !important;
    border-right: 2px solid #00ff41;
    box-shadow: 5px 0 15px rgba(0, 255, 65, 0.1);
}
[data-testid="stSidebar"] * { color: #00ff41 !important; }

.cyber-card {
    background: rgba(0, 15, 0, 0.88);
    border: 2px solid #00ff41;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 0 15px rgba(0, 255, 65, 0.2);
}

.stChatMessage {
    background: rgba(0, 12, 0, 0.9) !important;
    border-left: 4px solid #00ff41 !important;
    border-top: 1px solid rgba(0,255,65,0.3) !important;
    border-bottom: 1px solid rgba(0,255,65,0.3) !important;
    border-right: 1px solid rgba(0,255,65,0.3) !important;
    border-radius: 8px !important;
    margin-bottom: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.5);
}

[data-testid="stChatInput"] {
    border: 2px solid #00ff41 !important;
    border-radius: 8px !important;
    background-color: #000000 !important;
    box-shadow: 0 0 25px rgba(0, 255, 65, 0.3) !important;
}

input[type="password"] {
    background-color: #000000 !important;
    color: #00ff41 !important;
    border: 2px solid #00ff41 !important;
    box-shadow: 0 0 20px rgba(0, 255, 65, 0.4) !important;
    font-size: 26px !important;
    letter-spacing: 12px !important;
    text-align: center !important;
}

p, span, div, label, h1, h2, h3, h4, li, small { 
    color: #00ff41 !important; 
    font-family: 'Courier New', Consolas, monospace !important; 
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
            <h3 style='margin-top:0;'>[ MAIN CORE ACCESS REQUIRED ]</h3>
            <small style='opacity: 0.8;'>SECURITY TERMINAL FOR ANURAG SIR</small>
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
        st.markdown("# ⚡ VEER AI OS V4")
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
    st.markdown("<h1 class='main-title'>⚡ VEER AI // MAIN CORE</h1>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='cyber-card'>
        <span style='color:#00ff41; font-weight:bold;'>[ ACTIVE SHIELD: {selected_mode} ]</span><br>
        <small>SECURE COUPLING ACCESSED BY OWNER // ENCRYPTION KEY: AES-256</small>
    </div>
    """, unsafe_allow_html=True)

    # Render Chat History
    for msg in st.session_state.messages:
        avatar = "👤" if msg["role"] == "user" else ("🤖" if "HACKER" in selected_mode else "👨‍🏫")
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # Chat Input Command
    input_hint = "Execute hacker query, Anurag Sir..." if "HACKER" in selected_mode else "Ask educational terminal, Anurag Sir..."
    prompt = st.chat_input(input_hint)

    if prompt:
        # Save user query
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
            
        # Get and save AI response with full chat history context
        with st.chat_message("assistant", avatar="🤖" if "HACKER" in selected_mode else "👨‍🏫"):
            with st.spinner("⚡ DECRYPTING SYSTEM RESPONSES..."):
                reply = fetch_smart_response(prompt, selected_mode, st.session_state.messages[:-1])
                st.markdown(reply)
                
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()
