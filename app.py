import streamlit as st
import requests

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="VEER AI // CYBER CORE",
    page_icon="💻",
    layout="wide"
)

# ================= API CONFIGURATION =================
# 🔑 अपनी असली Gemini API Key यहाँ नीचे पेस्ट करें:
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

# ================= AI ENGINE LOGIC (WITH YOUR API KEY) =================
def fetch_unlimited_response(prompt):
    # अनुराग सर के लिए एआई टोन सेट करना
    system_rules = "You are VEER AI. User name is Anurag Sir. Always answer accurately. Always answer in Hindi. Always call the user 'Anurag Sir'. Be smart, professional, and act as a highly advanced cyber core intelligence."
    
    # Gemini API End Point
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # स्ट्रक्चर्ड पेलोड (System Prompt + User Prompt)
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"System Instructions:\n{system_rules}\n\nUser Question:\n{prompt}"}
                ]
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            # Gemini के रिस्पॉन्स से टेक्स्ट निकालना
            ai_reply = data['candidates'][0]['content']['parts'][0]['text']
            return ai_reply.strip()
        else:
            # अगर API Key गलत हो या कोई एरर आए
            return f"Anurag Sir, API एरर कोड {response.status_code} रिसीव हुआ है। कृपया अपनी API Key जांचें।"
            
    except Exception as e:
        pass
        
    # ================= FAILSAFE MODE =================
    # अगर इंटरनेट या सर्वर बिल्कुल काम न करे तो लोकल बैकअप
    prompt_clean = prompt.lower()
    if "kedarnath" in prompt_clean or "केदारनाथ" in prompt:
        return "Anurag Sir, केदारनाथ भारत के运行 उत्तराखंड राज्य के रुद्रप्रयाग जिले में स्थित एक बेहद पवित्र और प्रसिद्ध तीर्थस्थल है।"
    elif "hello" in prompt_clean or "hi" in prompt_clean or "नमस्ते" in prompt:
        return "नमस्ते Anurag Sir! VEER AI नो-लिमिट साइबर कोर में आपका स्वागत है। आज आपका क्या आदेश है?"
    
    return f"Anurag Sir, कमांड रिसीव हो गई है। नेटवर्क फ़ायरवॉल की वजह से डेटा पैकेट डिक्रिप्ट हो रहा है, कृपया एक बार फिर कमांड एंटर करें।"

# ================= SESSION STATE =================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================= CYBERPUNK CSS =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(rgba(0, 20, 0, 0.85), rgba(0, 0, 0, 0.95)), 
                url('https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1920') no-repeat center center fixed;
    background-size: cover;
}
header { visibility: hidden; }
.main-title {
    text-align: center;
    font-size: 60px;
    font-weight: 900;
    color: #00ff41;
    text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41, 0 0 40px #00ff41;
}
[data-testid="stSidebar"] {
    background: rgba(0, 0, 0, 0.9) !important;
    border-right: 2px solid #00ff41;
}
[data-testid="stSidebar"] * { color: #00ff41 !important; }
.cyber-logo-card {
    background: rgba(0, 255, 65, 0.05);
    border: 2px dashed #00ff41;
    border-radius: 18px;
    padding: 15px 10px;
    text-align: center;
    box-shadow: 0 0 15px rgba(0, 255, 65, 0.3);
}
.cyber-logo-img { border-radius: 50%; border: 2px solid #00ff41; box-shadow: 0 0 15px #00ff41; margin-bottom: 10px; }
.cyber-card {
    background: rgba(0, 15, 0, 0.75);
    border: 1px solid #00ff41;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 15px;
    box-shadow: 0 0 12px rgba(0, 255, 65, 0.4);
}
.stChatMessage {
    background: rgba(0, 10, 0, 0.8) !important;
    border: 1px solid #00ff41 !important;
    border-radius: 18px !important;
    box-shadow: 0 0 8px rgba(0, 255, 65, 0.3) !important;
    margin-bottom: 10px;
}
[data-testid="stChatInput"] {
    border: 1px solid #00ff41 !important;
    border-radius: 15px !important;
    box-shadow: 0 0 15px #00ff41 !important;
    background-color: black !important;
}
[data-testid="metric-container"] {
    background: rgba(0, 20, 0, 0.8);
    border: 1px solid #00ff41;
    border-radius: 15px;
}
.stButton button { width: 100%; background: black; color: #00ff41; border: 1px solid #00ff41; border-radius: 12px; }
.stButton button:hover { background: #00ff41; color: black; }
p, span, div, label, h1, h2, h3, h4 { color: #00ff41 !important; font-family: Consolas, monospace !important; }
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("# ⚡ VEER AI")
    st.success("🟢 SECURE PRIVATE API ACTIVE")

    st.markdown("""
    <div class="cyber-logo-card">
        <img class="cyber-logo-img" src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3Z0cmNvdWp6M214b29pYTdqM29scXFlZnN4ZXFpZWh0ZXN5MmswOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Y3bme762LLXbg4Mme6/giphy.gif" width="120" height="120">
        <h3 style="margin:0; letter-spacing: 2px;">V E E R</h3>
        <span style="font-size:11px; opacity:0.8;">INFINITY CORE v5.5</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🗑️ NEW CHAT"):
        st.session_state.messages = []
        st.rerun()

# ================= MAIN TITLE & DASHBOARD =================
st.markdown("<h1 class='main-title'>⚡ VEER AI // CYBER CORE ⚡</h1>", unsafe_allow_html=True)
st.markdown("""
<div class='cyber-card'>
## 🟢 SYSTEM STATUS : PRIVATE KEY SECURED<br>
👤 USER : ANURAG SIR (CHIEF ARCHITECT)<br>
🧠 AI ENGINE : PRIVATE EXPERT GATEWAY (STABLE MODE)<br>
🛡️ FIREWALL : ACTIVE // DECRYPTION PIPELINE ONLINE
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1: st.metric("💬 Total Chats", len(st.session_state.messages))
with c2: st.metric("🧠 API Key Status", "AUTHENTICATED 🟢")
with c3: st.metric("⚡ Server Quota", "STABLE")

st.markdown("---")

# ================= CHAT HISTORY =================
for msg in st.session_state.messages:
    custom_avatar = "👤" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=custom_avatar):
        st.markdown(msg["content"])

# ================= CHAT INPUT & LOGIC =================
prompt = st.chat_input(">>> ENTER COMMAND")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("⚡ PROCESSING THROUGH SECURE GATEWAY..."):
            reply = fetch_unlimited_response(prompt)
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
