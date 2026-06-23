import streamlit as st
import requests

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="VEER AI // CYBER CORE",
    page_icon="💻",
    layout="wide"
)

# ================= AI ENGINE LOGIC (WITH SECURE OPENAI API) =================
def fetch_unlimited_response(prompt):
    # अनुराग सर के लिए एआई टोन सेट करना
    system_rules = "You are VEER AI. User name is Anurag Sir. Always answer accurately. Always answer in Hindi. Always call the user 'Anurag Sir'. Be smart, professional, and act as a highly advanced cyber core intelligence."
    
    try:
        # 🔒 st.secrets से की (Key) को सुरक्षित तरीके से लोड करना
        api_key = st.secrets["OPENAI_API_KEY"]
        
        # OpenAI Chat Completions End Point
        url = "https://api.openai.com/v1/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # OpenAI के स्टैंडर्ड फॉर्मेट में पेलोड
        payload = {
            "model": "gpt-4o-mini",  # आप अपनी पसंद का मॉडल (जैसे gpt-4o) यहाँ बदल सकते हैं
            "messages": [
                {"role": "system", "content": system_rules},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            ai_reply = data['choices'][0]['message']['content']
            return ai_reply.strip()
        else:
            return f"Anurag Sir, API एरर कोड {response.status_code} रिसीव हुआ है। कृपया बैकएंड कॉन्फ़िगरेशन या बिलिंग जांचें।"
            
    except KeyError:
        return "Anurag Sir, 'OPENAI_API_KEY' आपकी secrets.toml फ़ाइल में नहीं मिली। कृपया फ़ाइल स्ट्रक्चर चेक करें।"
    except Exception:
        pass
        
    # ================= FAILSAFE MODE =================
    prompt_clean = prompt.lower()
    if "kedarnath" in prompt_clean or "केदारनाथ" in prompt:
        return "Anurag Sir, केदारनाथ भारत के उत्तराखंड राज्य के रुद्रप्रयाग जिले में स्थित एक बेहद पवित्र और प्रसिद्ध तीर्थस्थल है।"
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
    st.success("🔒 VAULT KEY SECURED & HIDDEN")

    st.markdown("""
    <div class="cyber-logo-card">
        <img class="cyber-logo-img" src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3Z0cmNvdWp6M214b29pYTdqM29scXFlZnN4ZXFpZWh0ZXN5MmswOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Y3bme762LLXbg4Mme6/giphy.gif" width="120" height="120">
        <h3 style="margin:0; letter-spacing: 2px;">V E E R</h3>
        <span style="font-size:11px; opacity:0.8;">INFINITY CORE v6.0</span>
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
## 🟢 SYSTEM STATUS : VAULT ENCRYPTED (SAFE)<br>
👤 USER : ANURAG SIR (CHIEF ARCHITECT)<br>
🧠 AI ENGINE : ENCRYPTED PRIVATE GATEWAY (SECRETS ROUTED)<br>
🛡️ FIREWALL : ACTIVE // STEALTH MODE ONLINE
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1: st.metric("💬 Total Chats", len(st.session_state.messages))
with c2: st.metric("🧠 API Key Status", "HIDDEN IN VAULT 🔒")
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
        with st.spinner("⚡ PROCESSING THROUGH ENCRYPTED STREAM..."):
            reply = fetch_unlimited_response(prompt)
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
