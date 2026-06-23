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
    # अब यह AI आपके साथ बिल्कुल नॉर्मल, स्मार्ट और मददगार दोस्त की तरह बात करेगा
    system_rules = (
        "You are VEER AI, a helpful, intelligent, and friendly AI collaborator. "
        "The user's name is Anurag Sir. Always address him respectfully as 'Anurag Sir'. "
        "Answer naturally, with clear formatting and a helpful tone in Hindi (or Hinglish if appropriate). "
        "Do not show any hacker prank errors or fake system errors. Act as a real assistant."
    )
    
    try:
        # 🔒 Vault से सुरक्षित तरीके से की (Key) उठाना
        api_key = st.secrets["GEMINI_API_KEY"]
        
        # Gemini API End Point (gemini-2.5-flash मॉडल सबसे तेज़ और बेस्ट है)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Gemini का ऑफिशियल स्ट्रक्चर्ड पेलोड
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
            # Gemini के रिस्पॉन्स से टेक्स्ट को निकालना
            ai_reply = data['candidates'][0]['content']['parts'][0]['text']
            return ai_reply.strip()
        else:
            return f"Anurag Sir, कनेक्शन में थोड़ी दिक्कत आ रही है (Error Code: {response.status_code})। कृपया एक बार बैकएंड सेटिंग्स या API Key चेक कर लें।"
            
    except KeyError:
        return "Anurag Sir, बैकएंड में 'GEMINI_API_KEY' नहीं मिल पा रही है। कृपया अपनी secrets.toml फ़ाइल चेक करें।"
    except Exception:
        return "Anurag Sir, नेटवर्क थोड़ा स्लो लग रहा है। कृपया एक बार फिर कोशिश करें।"

# ================= SESSION STATE =================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================= CYBERPUNK CSS (HACKER VIBE ONLY) =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(rgba(0, 15, 0, 0.9), rgba(0, 0, 0, 0.95)), 
                url('https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1920') no-repeat center center fixed;
    background-size: cover;
}
header { visibility: hidden; }
.main-title {
    text-align: center;
    font-size: 50px;
    font-weight: 900;
    color: #00ff41;
    text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41;
    font-family: Consolas, monospace !important;
}
[data-testid="stSidebar"] {
    background: rgba(0, 0, 0, 0.95) !important;
    border-right: 2px solid #00ff41;
}
[data-testid="stSidebar"] * { color: #00ff41 !important; }
.cyber-logo-card {
    background: rgba(0, 255, 65, 0.05);
    border: 1px solid #00ff41;
    border-radius: 12px;
    padding: 15px 10px;
    text-align: center;
    box-shadow: 0 0 10px rgba(0, 255, 65, 0.2);
}
.cyber-logo-img { border-radius: 50%; border: 1px solid #00ff41; margin-bottom: 10px; }
.cyber-card {
    background: rgba(0, 10, 0, 0.8);
    border: 1px solid #00ff41;
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 15px;
}
.stChatMessage {
    background: rgba(0, 10, 0, 0.85) !important;
    border: 1px solid #00ff41 !important;
    border-radius: 12px !important;
    margin-bottom: 10px;
}
[data-testid="stChatInput"] {
    border: 1px solid #00ff41 !important;
    border-radius: 12px !important;
    background-color: black !important;
}
[data-testid="metric-container"] {
    background: rgba(0, 15, 0, 0.8);
    border: 1px solid #00ff41;
    border-radius: 12px;
}
.stButton button { width: 100%; background: black; color: #00ff41; border: 1px solid #00ff41; border-radius: 8px; }
.stButton button:hover { background: #00ff41; color: black; }
p, span, div, label, h1, h2, h3, h4, li { color: #00ff41 !important; font-family: Consolas, monospace !important; }
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("# ⚡ VEER AI")
    st.success("🔒 GEMINI SECURE ONLINE")

    st.markdown("""
    <div class="cyber-logo-card">
        <img class="cyber-logo-img" src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3Z0cmNvdWp6M214b29pYTdqM29scXFlZnN4ZXFpZWh0ZXN5MmswOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Y3bme762LLXbg4Mme6/giphy.gif" width="100" height="100">
        <h3 style="margin:0; letter-spacing: 2px;">V E E R</h3>
        <span style="font-size:11px; opacity:0.8;">GEMINI CORE v7.5</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🗑️ CLEAR CHAT"):
        st.session_state.messages = []
        st.rerun()

# ================= MAIN TITLE & DASHBOARD =================
st.markdown("<h1 class='main-title'>⚡ VEER AI // LIVE GATEWAY ⚡</h1>", unsafe_allow_html=True)
st.markdown("""
<div class='cyber-card'>
## 🟢 SYSTEM STATUS : ONLINE<br>
👤 USER : ANURAG SIR (CHIEF ARCHITECT)<br>
🧠 ENGINE : GOOGLE GEMINI INTELLIGENCE (REAL CHAT ACTIVE)
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1: st.metric("💬 Total Chats", len(st.session_state.messages))
with c2: st.metric("🛡️ Gateway Status", "AUTHENTICATED 🔒")

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
        with st.spinner("⚡ सोच रहा हूँ..."):
            reply = fetch_unlimited_response(prompt)
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
