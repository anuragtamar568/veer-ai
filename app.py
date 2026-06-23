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

# ================= CYBERPUNK & HACKER BACKGROUND CSS =================
st.markdown("""
<style>
/* हैकर / रोबोट वाली बैकग्राउंड इमेज और डार्क ओवरले */
.stApp {
    background: linear-gradient(rgba(0, 20, 0, 0.85), rgba(0, 0, 0, 0.95)), 
                url('https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1920') no-repeat center center fixed;
    background-size: cover;
}
header {
    visibility: hidden;
}
.main-title {
    text-align: center;
    font-size: 60px;
    font-weight: 900;
    color: #00ff41;
    text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41, 0 0 40px #00ff41;
}
/* Sidebar Fix */
[data-testid="stSidebar"] {
    background: rgba(0, 0, 0, 0.9) !important;
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
    padding: 15px 10px;
    margin-bottom: 20px;
    text-align: center;
    box-shadow: 0 0 15px rgba(0, 255, 65, 0.3);
}
.cyber-logo-img {
    border-radius: 50%;
    border: 2px solid #00ff41;
    box-shadow: 0 0 15px #00ff41;
    margin-bottom: 10px;
}
/* Cards */
.cyber-card {
    background: rgba(0, 15, 0, 0.75);
    border: 1px solid #00ff41;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 15px;
    box-shadow: 0 0 12px rgba(0, 255, 65, 0.4);
    backdrop-filter: blur(5px);
}
/* Chat Boxes */
.stChatMessage {
    background: rgba(0, 10, 0, 0.8) !important;
    border: 1px solid #00ff41 !important;
    border-radius: 18px !important;
    box-shadow: 0 0 8px rgba(0, 255, 65, 0.3) !important;
    margin-bottom: 10px;
    backdrop-filter: blur(3px);
}
/* Input Box Fix */
[data-testid="stChatInput"] {
    border: 1px solid #00ff41 !important;
    border-radius: 15px !important;
    box-shadow: 0 0 15px #00ff41 !important;
    background-color: black !important;
}
/* Metrics */
[data-testid="metric-container"] {
    background: rgba(0, 20, 0, 0.8);
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

    # साइडबार में शानदार लाइव एनिमेटेड हैकर/रोबोट गिफ (GIF) इमेज
    st.markdown("""
    <div class="cyber-logo-card">
        <img class="cyber-logo-img" src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3Z0cmNvdWp6M214b29pYTdqM29scXFlZnN4ZXFpZWh0ZXN5MmswOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Y3bme762LLXbg4Mme6/giphy.gif" width="120" height="120">
        <h3 style="margin:0; letter-spacing: 2px;">V E E R</h3>
        <span style="font-size:11px; opacity:0.8;">HACKER MODE v3.5</span>
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
## 🟢 SYSTEM STATUS : SECURE<br>
👤 USER : ANURAG SIR (CHIEF ARCHITECT)<br>
🧠 AI ENGINE : GEMINI PRO INFRASTRUCTURE<br>
🛡 FIREWALL : MAXIMUM PRIVACY<br>
⚡ MODE : HACKER INTELLIGENCE RENDERED
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("💬 Messages", len(st.session_state.messages))
with c2:
    st.metric("🧠 AI Core", "LIVE")
with c3:
    st.metric("⚡ Status", "CONNECTED")

st.markdown("---")

# ================= CHAT HISTORY DISPLAY =================
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
        with st.spinner("⚡ DECRYPTING QUANTUM DATA..."):
            try:
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
