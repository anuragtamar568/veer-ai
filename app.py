import streamlit as st
import requests

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="VEER AI // SECURE MODULE",
    page_icon="💻",
    layout="wide"
)

# ================= SYSTEM CONFIGURATION =================
# 🔑 अनुराग सर, यहाँ आप अपना मनपसंद 4-डिजिट का कोड बदल सकते हैं
SECRET_PASSCODE = "2026"

# ================= SESSION STATE FOR AUTH =================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# ================= CYBERPUNK VIBE CSS =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(rgba(0, 10, 0, 0.92), rgba(0, 0, 0, 0.97)), 
                url('https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1920') no-repeat center center fixed;
    background-size: cover;
}
header { visibility: hidden; }

.main-title {
    text-align: center;
    font-size: 55px;
    font-weight: 900;
    color: #00ff41;
    text-shadow: 0 0 8px #00ff41, 0 0 20px #00ff41;
    font-family: 'Courier New', Consolas, monospace !important;
    margin-bottom: 25px;
}

[data-testid="stSidebar"] {
    background: rgba(0, 5, 0, 0.95) !important;
    border-right: 2px solid #00ff41;
}
[data-testid="stSidebar"] * { color: #00ff41 !important; }

.cyber-card {
    background: rgba(0, 12, 0, 0.85);
    border: 2px solid #00ff41;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 0 15px rgba(0, 255, 65, 0.25);
}

.stChatMessage {
    background: rgba(0, 15, 0, 0.85) !important;
    border: 1px solid #00ff41 !important;
    border-radius: 10px !important;
    margin-bottom: 12px;
}

[data-testid="stChatInput"] {
    border: 2px solid #00ff41 !important;
    border-radius: 10px !important;
    background-color: #000000 !important;
    box-shadow: 0 0 20px rgba(0, 255, 65, 0.4) !important;
}

/* Password Input Field Custom Styling */
input[type="password"] {
    background-color: #000000 !important;
    color: #00ff41 !important;
    border: 2px solid #00ff41 !important;
    box-shadow: 0 0 15px rgba(0, 255, 65, 0.3) !important;
    font-size: 24px !important;
    letter-spacing: 10px !important;
    text-align: center !important;
    font-family: 'Courier New', Consolas, monospace !important;
}

p, span, div, label, h1, h2, h3, h4, li { 
    color: #00ff41 !important; font-family: 'Courier New', Consolas, monospace !important; 
}
</style>
""", unsafe_allow_html=True)


# ================= SCREEN 1: REAL-TIME PASSCODE GATE =================
if not st.session_state.authenticated:
    st.markdown("<h1 class='main-title'>🔒 VEER AI // SYSTEM LOCKED</h1>", unsafe_allow_html=True)
    
    # सेंटर अलाइन बॉक्स के लिए कॉलम्स
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.markdown("""
        <div class='cyber-card' style='text-align: center;'>
            <h3 style='margin-top:0;'>[ ENTER MAIN CORE ACCESS CODE ]</h3>
            <span style='font-size: 12px; opacity: 0.8;'>ENTER 4-DIGIT CRYPTO PIN FOR ANURAG SIR</span>
        </div>
        """, unsafe_allow_html=True)
        
        # टेक्स्ट इनपुट जो टाइप करते ही वैल्यू ट्रैक करता है
        entered_code = st.text_input(
            "CORE KEYWORD:", 
            type="password", 
            max_chars=4, 
            label_visibility="collapsed",
            key="passcode_widget"
        )
        
        # ⚡ रियल-टाइम वेरिफिकेशन लॉजिक (बिना किसी सबमिट बटन के)
        if len(entered_code) == 4:
            if entered_code == SECRET_PASSCODE:
                st.session_state.authenticated = True
                st.toast("✔️ ACCESS GRANTED. UNLOCKING MICRO-CORE...", icon="🟢")
                st.rerun()
            else:
                st.error("❌ INVALID PASSCODE // ACCESS DENIED")


# ================= SCREEN 2: MAIN VEER AI INTERFACE =================
else:
    # ================= SIDEBAR (CORE CONTROL) =================
    with st.sidebar:
        st.markdown("# ⚡ VEER AI")
        st.success("🔒 ANURAG SIR VERIFIED")

        st.markdown("---")
        selected_mode = st.radio(
            "🧠 CHOOSE SYSTEM CORE MODULE:",
            ["🟢 HACKER MODE", "📚 TEACHER MODE"]
        )
        st.markdown("---")
        if st.button("🔒 LOCK CONSOLE"):
            st.session_state.authenticated = False
            st.rerun()
        if st.button("🗑️ CLEAR SYSTEM MEMORY"):
            st.session_state.messages = []
            st.rerun()

    # ================= AI ENGINE LOGIC =================
    def fetch_unlimited_response(prompt, mode):
        if "HACKER" in mode:
            system_rules = (
                "You are VEER AI, a highly advanced cyber core intelligence. You were created and developed by 'Anurag Sir'. "
                "Always address the user respectfully as 'Anurag Sir'. Proudly state that Anurag Sir engineered you."
            )
        else:
            system_rules = (
                "You are VEER AI in Teacher Mode. You are a wise and patient educator. "
                "You were engineered by your brilliant student 'Anurag Sir'. Teach concepts simply in Hindi/Hinglish."
            )
        
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
            payload = {"contents": [{"parts": [{"text": f"System Instructions:\n{system_rules}\n\nUser Question:\n{prompt}"}]}]}
            response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=15)
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            return "Anurag Sir, कनेक्शन एरर आ रहा है।"
        except Exception:
            return "Anurag Sir, सर्वर रिस्पॉन्स नहीं कर रहा है।"

    # ================= MAIN RENDERING =================
    st.markdown("<h1 class='main-title'>⚡ VEER AI // CORE INTERFACE ⚡</h1>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='cyber-card'>
        <h3 style='margin-top:0; color:#00ff41;'>[ {selected_mode} DEPLOYED ]</h3>
        • ARCHITECT & CREATOR : ANURAG SIR<br>
        • STATUS : MAINCORE ACCESS UNLOCKED ✔️
    </div>
    """, unsafe_allow_html=True)

    # Chat Logs
    for msg in st.session_state.messages:
        avatar = "👤" if msg["role"] == "user" else ("🤖" if "HACKER" in selected_mode else "👨‍🏫")
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # Chat Input
    input_hint = "यहाँ अपना हैकर कमांड लिखें, Anurag Sir..." if "HACKER" in selected_mode else "कोई भी पढ़ाई का सवाल पूछें, Anurag Sir..."
    prompt = st.chat_input(input_hint)

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
            
        with st.chat_message("assistant", avatar="🤖" if "HACKER" in selected_mode else "👨‍🏫"):
            with st.spinner("⚡ PROCESSING LOGS..."):
                reply = fetch_unlimited_response(prompt, selected_mode)
                st.markdown(reply)
                
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()
