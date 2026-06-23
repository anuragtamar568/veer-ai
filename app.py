import streamlit as st
import requests

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="VEER AI // CYBER CORE",
    page_icon="💻",
    layout="wide"
)

# ================= UNLIMITED FREE ENGINE LOGIC =================
def fetch_unlimited_response(prompt):
    # अनुराग सर के लिए एआई टोन सेट करना
    system_rules = "You are VEER AI. User name is Anurag Sir. Always answer accurately. Always answer in Hindi. Always call the user 'Anurag Sir'. Be smart and professional."
    full_query = f"{system_rules}\n\nUser Question: {prompt}"
    
    try:
        # Pollinations AI का बिल्कुल सही और फ्री पब्लिक API नेटवर्क एंडपॉइंट
        api_url = f"https://text.pollinations.ai/{requests.utils.quote(full_query)}"
        response = requests.get(api_url, timeout=12)
        
        if response.status_code == 200 and response.text.strip():
            return response.text.strip()
    except Exception:
        pass
        
    # ================= FAILSAFE MODE (LOCAL INTELLIGENCE) =================
    # अगर इंटरनेट या लाइव API डाउन हो तो यह बैकअप रिस्पॉन्स देगा
    prompt_clean = prompt.lower()
    if "kedarnath" in prompt_clean or "केदारनाथ" in prompt:
        return "Anurag Sir, केदारनाथ भारत के उत्तराखंड राज्य के रुद्रप्रयाग जिले में स्थित एक बेहद पवित्र और प्रसिद्ध तीर्थस्थल है। यह हिमालय की गोद में बसा भगवान शिव का बारहवां ज्योतिर्लिंग है।"
    elif "hello" in prompt_clean or "hi" in prompt_clean or "नमस्ते" in prompt:
        return "नमस्ते Anurag Sir! VEER AI नो-लिमिट साइबर कोर में आपका स्वागत है। आज आपका क्या आदेश है?"
    
    # डिफ़ॉल्ट साइबर थीम वाला एरर मैसेज (सिर्फ तब दिखेगा जब नेट पूरी तरह बंद हो)
    return f"Anurag Sir, कमांड रिसीव हो गई है। नेटवर्क फ़ायरवॉल की वजह से डेटा पैकेट डिक्रिप्ट हो रहा है, कृपया एक बार फिर कमांड एंटर करें या इंटरनेट कनेक्शन चेक करें।"

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
    st.success("🟢 UNLIMITED INFRASTRUCTURE")

    st.markdown("""
    <div class="cyber-logo-card">
        <img class="cyber-logo-img" src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3Z0cmNvdWp6M214b29pYTdqM29scXFlZnN4ZXFpZWh0ZXN5MmswOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Y3bme762LLXbg4Mme6/giphy.gif" width="120" height="120">
        <h3 style="margin:0; letter-spacing: 2px;">V E E R</h3>
        <span style="font-size:11px; opacity:0.8;">INFINITY CORE v5.0</span>
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
## 🟢 SYSTEM STATUS : UNLIMITED NO-LIMIT MODE<br>
👤 USER : ANURAG SIR (CHIEF ARCHITECT)<br>
🧠 AI ENGINE : FREE PUBLIC NETWORK BYPASS (NO API KEYS NEEDED)<br>
🛡️ FIREWALL : ACTIVE // INFINITE QUOTA BYPASSED
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1: st.metric("💬 Total Chats", len(st.session_state.messages))
with c2: st.metric("🧠 API Key Status", "BYPASSED (NONE)")
with c3: st.metric("⚡ Server Quota", "INFINITE")

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
        with st.spinner("⚡ ROUTING THROUGH UNLIMITED SERVERS..."):
            reply = fetch_unlimited_response(prompt)
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
