import streamlit as st
import random
import time

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="VEER AI // CYBER CORE",
    page_icon="💻",
    layout="wide"
)

# ================= SESSION STATE =================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================= MOCK CYBER BRAIN =================
def cyber_brain(prompt):
    # अनुराग सर के लिए स्पेशल लोकल इंटेलिजेंस डेटाबेस
    responses = [
        "आदेश का पालन कर दिया गया है, Anurag Sir। साइबर कोर पूरी तरह से सुरक्षित है।",
        "Anurag Sir, आपके दिए गए निर्देश को डिक्रिप्ट किया जा रहा है... एक्सेस ग्रैंटेड!",
        "Anurag Sir, मेनफ़्रेम डेटाबेस आपके नियंत्रण में है। अगला कमांड क्या है?",
        "सिस्टम पर कोई थ्रेट नहीं है, Anurag Sir। सिक्योरिटी शील्ड 100% एक्टिव है।",
        "Anurag Sir, आपके द्वारा इनपुट की गई कमांड को साइबर आर्किटेक्चर में प्रोसेस कर लिया गया है।",
        "VEER AI हमेशा आपकी सेवा में तत्पर है, Anurag Sir।"
    ]
    
    prompt_lower = prompt.lower()
    if "hello" in prompt_lower or "hi" in prompt_lower or "नमस्ते" in prompt:
        return "नमस्ते Anurag Sir! VEER AI साइबर कोर में आपका स्वागत है। मैं आपकी क्या सहायता कर सकता हूँ?"
    elif "status" in prompt_lower or "हाल" in prompt:
        return "Anurag Sir, सभी नोड्स ग्रीन हैं। सीपीयू लोड 12% है और नेटवर्क फायरवॉल पूरी तरह से एक्टिव है।"
    elif "नाम" in prompt or "who are you" in prompt_lower:
        return "मेरा नाम VEER AI है, Anurag Sir। मैं आपका पर्सनल साइबर-इंटेलिजेंस असिस्टेंट हूँ।"
        
    return random.choice(responses)

# ================= CYBERPUNK CSS =================
st.markdown("""
<style>
.stApp { background: radial-gradient(circle at top, #002200, #000000 75%); }
header { visibility: hidden; }
.main-title { text-align: center; font-size: 65px; font-weight: 900; color: #00ff41; text-shadow: 0 0 15px #00ff41; }
[data-testid="stSidebar"] { background: #000000; border-right: 2px solid #00ff41; }
[data-testid="stSidebar"] * { color: #00ff41 !important; }
.cyber-logo-card { background: rgba(0, 255, 65, 0.05); border: 2px dashed #00ff41; border-radius: 18px; padding: 25px 10px; text-align: center; }
.cyber-logo-text { font-size: 65px; }
.cyber-card { background: rgba(0, 255, 65, 0.05); border: 1px solid #00ff41; border-radius: 18px; padding: 18px; margin-bottom: 15px; }
.stChatMessage { background: rgba(0, 255, 65, 0.04) !important; border: 1px solid #00ff41 !important; border-radius: 18px !important; }
[data-testid="stChatInput"] { border: 1px solid #00ff41 !important; border-radius: 15px !important; background-color: black !important; }
[data-testid="metric-container"] { background: rgba(0, 255, 65, 0.05); border: 1px solid #00ff41; border-radius: 15px; }
.stButton button { width: 100%; background: black; color: #00ff41; border: 1px solid #00ff41; border-radius: 12px; }
.stButton button:hover { background: #00ff41; color: black; }
p, span, div, label, h1, h2, h3, h4 { color: #00ff41 !important; font-family: Consolas, monospace !important; }
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("# ⚡ VEER AI")
    st.success("🟢 LOCAL ENGINE ONLINE")
    st.markdown("""
    <div class="cyber-logo-card">
        <div class="cyber-logo-text">🤖</div>
        <h3 style="margin:0; letter-spacing: 2px;">V E E R</h3>
        <span style="font-size:11px; opacity:0.8;">OFFLINE CORE v3.0</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    if st.button("🗑️ NEW CHAT"):
        st.session_state.messages = []
        st.rerun()

# ================= MAIN UI =================
st.markdown("<h1 class='main-title'>⚡ VEER AI // CYBER CORE ⚡</h1>", unsafe_allow_html=True)
st.markdown("<div class='cyber-card'>## 🟢 SYSTEM STATUS : SECURE<br>👤 USER : ANURAG SIR<br>🧠 MODE : STANDALONE CYBER INTEL</div>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1: st.metric("💬 Messages", len(st.session_state.messages))
with c2: st.metric("🧠 Local Engine", "RUNNING")
with c3: st.metric("⚡ Latency", "0.01ms")

st.markdown("---")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

prompt = st.chat_input(">>> ENTER COMMAND")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("⚡ PROCESSING DATA LOCALLY..."):
            time.sleep(0.6)  # हैकर लुक देने के लिए आर्टिफिशियल डिले
            reply = cyber_brain(prompt)
            st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
