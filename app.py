import streamlit as st
import google.generativeai as genai

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="VEER AI // CYBER CORE",
    page_icon="💻",
    layout="wide"
)

# ================= GEMINI CONFIG =================
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # मॉडल इंस्ट्रक्शन बिल्कुल परफेक्ट सेट कर दी है
    model = genai.GenerativeModel(
        "gemini-2.5-flash",
        system_instruction=(
            "You are VEER AI. User name is Anurag Sir. "
            "Rules: Always answer accurately based on the user's question. "
            "Always answer in Hindi. Always call the user 'Anurag Sir'. "
            "Be smart, professional, witty, and cyber-intelligent."
        )
    )
except Exception as e:
    st.error(f"Gemini Configuration Error: {e}")
    st.stop()

# ================= SESSION STATE =================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================= CYBERPUNK CSS =================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #003300, #000000 70%);
}
header {
    visibility: hidden;
}
.main-title {
    text-align: center;
    font-size: 65px;
    font-weight: 900;
    color: #00ff41;
    text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41, 0 0 40px #00ff41;
}
/* Sidebar CSS Fix */
[data-testid="stSidebar"] {
    background: #000000;
    border-right: 2px solid #00ff41;
}
[data-testid="stSidebar"] p, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] span {
    color: #00ff41 !important;
}
/* Cyber Logo Card */
.cyber-logo-card {
    background: rgba(0, 255, 65, 0.05);
    border: 2px dashed #00ff41;
    border-radius: 18px;
    padding: 25px 10px;
    margin-bottom: 20px;
    text-align: center;
    box-shadow: 0 0 15px rgba(0, 255, 65, 0.3);
}
.cyber-logo-text {
    font-size: 65px;
    line-height: 1;
    margin-bottom: 10px;
}
/* Cards */
.cyber-card {
    background: rgba(0, 255, 65, 0.05);
    border: 1px solid #00ff41;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 15px;
    box-shadow: 0 0 8px #00ff41, inset 0 0 8px rgba(0, 255, 65, 0.3);
}
/* Chat Boxes */
.stChatMessage {
    background: rgba(0, 255, 65, 0.04) !important;
    border: 1px solid #00ff41 !important;
    border-radius: 18px !important;
    box-shadow: 0 0 8px #00ff41 !important;
    margin-bottom: 10px;
}
/* Input Box Fix */
[data-testid="stChatInput"] {
    border: 1px solid #00ff41 !important;
    border-radius: 15px !important;
    box-shadow: 0 0 10px #00ff41 !important;
    background-color: black !important;
}
/* Metrics */
[data-testid="metric-container"] {
    background: rgba(0, 255, 65, 0.05);
    border: 1px solid #00ff41;
    border-radius: 15px;
    box-shadow: 0 0 10px #00ff41;
}
/* Buttons */
.stButton button {
    width: 100%;
    background: black;
    color: #00ff41;
    border: 1px solid #00ff41;
    border-radius: 12px;
    box-shadow: 0 0 10px #00ff41;
}
.stButton button:hover {
    background: #00ff41;
    color: black;
}
/* Text Global Overrides */
p, span, div, label, h1, h2, h3, h4 {
    color: #00ff41 !important;
    font-family: Consolas, monospace !important;
}
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("# ⚡ VEER AI")
    st.success("🟢 CYBER CORE ONLINE")

    # एनिमेटेड रोबोट लोगो कार्ड
    st.markdown("""
    <div class="cyber-logo-card">
        <div class="cyber-logo-text">🤖</div>
        <h3 style="margin:0; letter-spacing: 2px;">V E E R</h3>
        <span style="font-size:11px; opacity:0.8;">LIVE CORE v2.5</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("🗑️ NEW CHAT"):
        st.session_state.messages = []
        st.rerun()

    chat_text = ""
    for m in st.session_state.messages:
        chat_text += f"{m['role'].upper()} : {m['content']}\n\n"

    st.download_button(
        "📥 DOWNLOAD CHAT",
        chat_text,
        file_name="veer_chat.txt"
    )

# ================= MAIN TITLE =================
st.markdown("""
<h1 class='main-title'>
⚡ VEER AI // CYBER CORE ⚡
</h1>
""", unsafe_allow_html=True)

# ================= DASHBOARD =================
st.markdown("""
<div class='cyber-card'>
## 🟢 SYSTEM STATUS : ONLINE<br>
👤 USER : ANURAG SIR<br>
🧠 AI ENGINE : GEMINI PRO<br>
🛡 SECURITY : ACTIVE<br>
⚡ MODE : CYBER INTELLIGENCE
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("💬 Messages", len(st.session_state.messages))
with c2:
    st.metric("🧠 AI Core", "LIVE")
with c3:
    st.metric("⚡ Status", "ACTIVE")

st.markdown("---")

# ================= CHAT HISTORY DISPLAY =================
# यहाँ avatar पैरामीटर जोड़कर टेक्स्ट लेबल्स को इमोजी में बदल दिया गया है
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
        with st.spinner("⚡ ACCESSING CYBER CORE..."):
            try:
                # सीधे लाइव जेमिनी इंजन से वास्तविक जवाब मंगाया जा रहा है
                response = model.generate_content(prompt)
                reply = response.text
            except Exception as e:
                if "429" in str(e) or "ResourceExhausted" in str(e):
                    reply = "Anurag Sir, मुख्य सर्वर ओवरलोड (API Limit Exceeded) हो गया है। कृपया कोर को रीस्टार्ट होने के लिए 1 मिनट का समय दें और पुनः प्रयास करें।"
                else:
                    reply = f"Anurag Sir, कनेक्शन में कुछ अस्थाई दिक्कत आई है। एरर कोड: {e}"
            
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
