import streamlit as st
import requests

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="VEER AI // CYBER CORE",
    page_icon="💻",
    layout="wide"
)

# ================= AI ENGINE LOGIC (LIVE GEMINI CHAT) =================
def fetch_unlimited_response(prompt):
    system_rules = (
        "You are VEER AI, a helpful, intelligent, and friendly AI collaborator. "
        "The user's name is Anurag Sir. Always address him respectfully as 'Anurag Sir'. "
        "Answer naturally, with clear formatting and a helpful tone in Hindi (or Hinglish if appropriate). "
        "Do not show any hacker prank errors or fake system errors. Act as a real assistant."
    )
    
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": f"System Instructions:\n{system_rules}\n\nUser Question:\n{prompt}"}
                    ]
                }
            ]
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            ai_reply = data['candidates'][0]['content']['parts'][0]['text']
            return ai_reply.strip()
        else:
            return f"Anurag Sir, कनेक्शन में थोड़ी दिक्कत आ रही है (Error Code: {response.status_code})।"
            
    except KeyError:
        return "Anurag Sir, बैकएंड में 'GEMINI_API_KEY' नहीं मिल पा रही है। कृपया अपनी secrets.toml फ़ाइल चेक करें।"
    except Exception:
        return "Anurag Sir, नेटवर्क थोड़ा स्लो लग रहा है। कृपया फिर से कोशिश करें।"

# ================= SESSION STATE =================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================= ADVANCED CYBERPUNK CSS (LIGHTING & BOXES) =================
st.markdown("""
<style>
/* Scanline Animation & Matrix Background */
.stApp {
    background: linear-gradient(rgba(0, 10, 0, 0.92), rgba(0, 0, 0, 0.97)), 
                url('https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1920') no-repeat center center fixed;
    background-size: cover;
}
header { visibility: hidden; }

/* Glowing Main Title */
.main-title {
    text-align: center;
    font-size: 55px;
    font-weight: 900;
    color: #00ff41;
    text-shadow: 0 0 8px #00ff41, 0 0 20px #00ff41, 0 0 30px #028a1e;
    font-family: 'Courier New', Consolas, monospace !important;
    margin-bottom: 25px;
}

/* Sidebar Custom Look */
[data-testid="stSidebar"] {
    background: rgba(0, 5, 0, 0.95) !important;
    border-right: 2px solid #00ff41;
    box-shadow: 5px 0 15px rgba(0, 255, 65, 0.2);
}
[data-testid="stSidebar"] * { color: #00ff41 !important; }

/* Cyber Boxes with Neon Lighting */
.cyber-logo-card {
    background: rgba(0, 255, 65, 0.03);
    border: 2px solid #00ff41;
    border-radius: 12px;
    padding: 20px 10px;
    text-align: center;
    box-shadow: 0 0 15px rgba(0, 255, 65, 0.2), inset 0 0 10px rgba(0, 255, 65, 0.1);
}
.cyber-logo-img { 
    border-radius: 50%; 
    border: 2px solid #00ff41; 
    box-shadow: 0 0 15px #00ff41; 
    margin-bottom: 10px; 
}

.cyber-card {
    background: rgba(0, 12, 0, 0.85);
    border: 2px solid #00ff41;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 0 15px rgba(0, 255, 65, 0.25), inset 0 0 15px rgba(0, 255, 65, 0.05);
}

/* Glowing Metrics Box */
[data-testid="metric-container"] {
    background: rgba(0, 8, 0, 0.9) !important;
    border: 1px solid #00ff41 !important;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 255, 65, 0.15);
    padding: 10px !important;
}

/* Chat Message Styling with Box Lighting */
.stChatMessage {
    background: rgba(0, 15, 0, 0.85) !important;
    border: 1px solid #00ff41 !important;
    border-radius: 10px !important;
    margin-bottom: 12px;
    box-shadow: 0 0 8px rgba(0, 255, 65, 0.1);
}

/* Glowing Input Box */
[data-testid="stChatInput"] {
    border: 2px solid #00ff41 !important;
    border-radius: 10px !important;
    background-color: #000000 !important;
    box-shadow: 0 0 20px rgba(0, 255, 65, 0.4) !important;
}

/* Glowing Custom Buttons */
.stButton button { 
    width: 100%; 
    background: #000000; 
    color: #00ff41; 
    border: 2px solid #00ff41; 
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 255, 65, 0.2);
    font-weight: bold;
    transition: all 0.3s ease;
}
.stButton button:hover { 
    background: #00ff41; 
    color: #000000; 
    box-shadow: 0 0 20px #00ff41;
}

/* Base Tech Typography */
p, span, div, label, h1, h2, h3, h4, li { 
    color: #00ff41 !important; 
    font-family: 'Courier New', Consolas, monospace !important; 
}
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("# ⚡ VEER AI")
    st.success("🔒 VAULT ONLINE // SECURE")

    st.markdown("""
    <div class="cyber-logo-card">
        <img class="cyber-logo-img" src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3Z0cmNvdWp6M214b29pYTdqM29scXFlZnN4ZXFpZWh0ZXN5MmswOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Y3bme762LLXbg4Mme6/giphy.gif" width="110" height="110">
        <h3 style="margin:0; letter-spacing: 3px;">V E E R</h3>
        <span style="font-size:11px; opacity:0.8;">CORE EDITION v8.0</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🗑️ CLEAR SYSTEM MEMORY"):
        st.session_state.messages = []
        st.rerun()

# ================= MAIN TITLE & DASHBOARD =================
st.markdown("<h1 class='main-title'>⚡ VEER AI // CYBER SYSTEM ⚡</h1>", unsafe_allow_html=True)

# Main Dashboard Status Box
st.markdown("""
<div class='cyber-card'>
    <h3 style='margin-top:0; color:#00ff41; text-shadow: 0 0 5px #00ff41;'>[ SYSTEM PARAMETERS ]</h3>
    • USER : ANURAG SIR (CHIEF ARCHITECT)<br>
    • ENGINE : GOOGLE GEMINI LIGHTNING CORE<br>
    • FIREWALL : ENCRYPTED SECURE LINK
</div>
""", unsafe_allow_html=True)

# Metrics Boxes
c1, c2 = st.columns(2)
with c1: st.metric("💬 Total Logs", len(st.session_state.messages))
with c2: st.metric("🛡️ Node Status", "STABLE // GLOW")

st.markdown("---")

# ================= CHAT HISTORY =================
for msg in st.session_state.messages:
    custom_avatar = "👤" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=custom_avatar):
        st.markdown(msg["content"])

# ================= CHAT INPUT & LOGIC =================
prompt = st.chat_input("यहाँ अपना सवाल लिखें, Anurag Sir...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("⚡ PROCESSING NODE DATA..."):
            reply = fetch_unlimited_response(prompt)
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
