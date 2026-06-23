import streamlit as st
import requests

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="VEER AI // MULTI-CORE",
    page_icon="💻",
    layout="wide"
)

# ================= SESSION STATE =================
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

/* Cyber Boxes with Neon Lighting */
.cyber-logo-card {
    background: rgba(0, 255, 65, 0.03);
    border: 2px solid #00ff41;
    border-radius: 12px;
    padding: 20px 10px;
    text-align: center;
    box-shadow: 0 0 15px rgba(0, 255, 65, 0.2);
}
.cyber-logo-img { border-radius: 50%; border: 2px solid #00ff41; box-shadow: 0 0 15px #00ff41; margin-bottom: 10px; }

.cyber-card {
    background: rgba(0, 12, 0, 0.85);
    border: 2px solid #00ff41;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 0 15px rgba(0, 255, 65, 0.25);
}

[data-testid="metric-container"] {
    background: rgba(0, 8, 0, 0.9) !important;
    border: 1px solid #00ff41 !important;
    border-radius: 10px;
    padding: 10px !important;
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

/* Radio Button Styling for Cyber Look */
div[data-testid="stRadio"] > label {
    font-weight: bold !important;
    color: #00ff41 !important;
}

.stButton button { 
    width: 100%; background: #000000; color: #00ff41; border: 2px solid #00ff41; border-radius: 8px;
    font-weight: bold; transition: all 0.3s ease;
}
.stButton button:hover { background: #00ff41; color: #000000; box-shadow: 0 0 20px #00ff41; }

p, span, div, label, h1, h2, h3, h4, li { 
    color: #00ff41 !important; font-family: 'Courier New', Consolas, monospace !important; 
}
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR (CORE CONTROL) =================
with st.sidebar:
    st.markdown("# ⚡ VEER AI")
    st.success("🔒 MULTI-CORE PIPELINE ACTIVE")

    st.markdown("""
    <div class="cyber-logo-card">
        <img class="cyber-logo-img" src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3Z0cmNvdWp6M214b29pYTdqM29scXFlZnN4ZXFpZWh0ZXN5MmswOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Y3bme762LLXbg4Mme6/giphy.gif" width="110" height="110">
        <h3 style="margin:0; letter-spacing: 3px;">V E E R</h3>
        <span style="font-size:11px; opacity:0.8;">CORE EDITION v9.0</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    
    # 🎛️ यहाँ से मोड कंट्रोल होगा बिना किसी सिंटैक्स एरर के
    selected_mode = st.radio(
        "🧠 CHOOSE SYSTEM CORE MODULE:",
        ["🟢 HACKER MODE", "📚 TEACHER MODE"]
    )
    
    st.markdown("---")
    if st.button("🗑️ CLEAR SYSTEM MEMORY"):
        st.session_state.messages = []
        st.rerun()

# ================= AI ENGINE LOGIC =================
def fetch_unlimited_response(prompt, mode):
    if "HACKER" in mode:
        system_rules = (
            "You are VEER AI, a highly advanced cyber core intelligence and a friendly hacker-style collaborator. "
            "You were created and developed by 'Anurag Sir' (who is your Chief Architect). "
            "The user talking to you is Anurag Sir. Always address him respectfully as 'Anurag Sir'. "
            "If anyone asks who created you or who made you, proudly state that you were designed and engineered by Anurag Sir. "
            "Answer naturally, with clear formatting and a cool, helpful tone in Hindi or Hinglish."
        )
    else:  # Teacher Mode
        system_rules = (
            "You are VEER AI in Teacher Mode. You are an extremely wise, patient, and knowledgeable educator. "
            "You were created and developed by your brilliant student and Chief Architect 'Anurag Sir'. "
            "The user is Anurag Sir. Always address him respectfully as 'Anurag Sir'. "
            "If anyone asks about your creator, explain with respect that Anurag Sir engineered you. "
            "Answer academic questions beautifully, clearly, breaking concepts down simply in Hindi/Hinglish like a professional teacher."
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
            return data['candidates'][0]['content']['parts'][0]['text'].strip()
        else:
            return f"Anurag Sir, कनेक्शन में थोड़ी दिक्कत आ रही है (Error Code: {response.status_code})।"
            
    except KeyError:
        return "Anurag Sir, बैकएंड में 'GEMINI_API_KEY' नहीं मिल पा रही है। कृपया अपनी secrets.toml फ़ाइल चेक करें।"
    except Exception:
        return "Anurag Sir, नेटवर्क थोड़ा धीमा है। कृपया फिर से कोशिश करें।"

# ================= MAIN RENDERING =================
st.markdown("<h1 class='main-title'>⚡ VEER AI // CORE INTERFACE ⚡</h1>", unsafe_allow_html=True)

# वर्तमान में एक्टिव मोड का स्टेटस कार्ड
st.markdown(f"""
<div class='cyber-card'>
    <h3 style='margin-top:0; color:#00ff41;'>[ {selected_mode} CURRENT SYSTEM PARAMETERS ]</h3>
    • USER : ANURAG SIR (CHIEF ARCHITECT)<br>
    • CREATOR : ANURAG SIR<br>
    • MODULE STATUS : SECURED & LIVE
</div>
""", unsafe_allow_html=True)

# Chat History Display
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else ("🤖" if "HACKER" in selected_mode else "👨‍🏫")
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ================= CHAT INPUT & LOGIC =================
input_hint = "यहाँ अपना हैकर कमांड लिखें, Anurag Sir..." if "HACKER" in selected_mode else "कोई भी पढ़ाई का सवाल पूछें, Anurag Sir..."
prompt = st.chat_input(input_hint)

if prompt:
    # 1. यूजर का मैसेज सेव करें और दिखाएं
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
        
    # 2. AI का रिस्पॉन्स जनरेट करें
    with st.chat_message("assistant", avatar="🤖" if "HACKER" in selected_mode else "👨‍🏫"):
        with st.spinner("⚡ PROCESSING LOGS..."):
            reply = fetch_unlimited_response(prompt, selected_mode)
            st.markdown(reply)
            
    # 3. AI का मैसेज हिस्ट्री में सेव करें और पेज रीलोड करें
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
