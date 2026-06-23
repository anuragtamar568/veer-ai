import streamlit as st
import requests

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="VEER AI // MULTI-CORE",
    page_icon="💻",
    layout="wide"
)

# ================= ADVANCED MODE TABS =================
# ऐप के सबसे ऊपर हैकर और टीचर मोड के टैब बनाए गए हैं
selected_mode = st.tabs(["🟢 HACKER MODE", "📚 TEACHER MODE"])

# ================= AI ENGINE LOGIC =================
def fetch_unlimited_response(prompt, mode):
    # एआई को यह पता है कि उसे अनुराग सर ने ही बनाया है
    if mode == "Hacker":
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
            ai_reply = data['candidates'][0]['content']['parts'][0]['text']
            return ai_reply.strip()
        else:
            return f"Anurag Sir, कनेक्शन में थोड़ी दिक्कत आ रही है (Error Code: {response.status_code})।"
            
    except KeyError:
        return "Anurag Sir, बैकएंड में 'GEMINI_API_KEY' नहीं मिल पा रही है। कृपया अपनी secrets.toml फ़ाइल चेक करें।"
    except Exception:
        return "Anurag Sir, नेटवर्क थोड़ा धीमा है। कृपया फिर से कोशिश करें।"

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

/* Tabs Styling */
div[data-testid="stTabs"] button {
    color: #00ff41 !important;
    font-size: 18px !important;
    font-weight: bold !important;
    font-family: 'Courier New', Consolas, monospace !important;
    border: 1px solid transparent !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    border: 1px solid #00ff41 !important;
    box-shadow: 0 0 10px rgba(0, 255, 65, 0.3);
    background: rgba(0, 255, 65, 0.05) !important;
}

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

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("# ⚡ VEER AI")
    st.success("🔒 MULTI-CORE PIPELINE ACTIVE")

    st.markdown("""
    <div class="cyber-logo-card">
        <img class="cyber-logo-img" src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3Z0cmNvdWp6M214b29pYTdqM29scXFlZnN4ZXFpZWh0ZXN5MmswOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Y3bme762LLXbg4Mme6/giphy.gif" width="110" height="110">
        <h3 style="margin:0; letter-spacing: 3px;">V E E R</h3>
        <span style="font-size:11px; opacity:0.8;">MULTI-CORE v9.0</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🗑️ CLEAR SYSTEM MEMORY"):
        st.session_state.messages = []
        st.rerun()

# ================= MAIN RENDERING =================
st.markdown("<h1 class='main-title'>⚡ VEER AI // CORE INTERFACE ⚡</h1>", unsafe_allow_html=True)

# 1. HACKER MODE TAB
with selected_mode[0]:
    st.markdown("""
    <div class='cyber-card'>
        <h3 style='margin-top:0; color:#00ff41;'>[ HACKER MODE PARAMETERS ]</h3>
        • USER : ANURAG SIR (CHIEF ARCHITECT)<br>
        • CREATOR : ANURAG SIR<br>
        • CORE : CYBER INTEL SYSTEM ACTIVE
    </div>
    """, unsafe_allow_html=True)
    
    # Chat History
    for msg in st.session_state.messages:
        avatar = "👤" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # Input Box for Hacker Mode
    prompt = st.chat_input("यहाँ अपना हैकर कमांड या सवाल लिखें, Anurag Sir...", key="hacker_input")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

# 2. TEACHER MODE TAB
with selected_mode[1]:
    st.markdown("""
    <div class='cyber-card'>
        <h3 style='margin-top:0; color:#00ff41;'>[ TEACHER MODE ACTIVE ]</h3>
        • ARCHITECT : ANURAG SIR<br>
        • MISSION : KNOWLEDGE & STUDY ASSISTANCE<br>
        • STATUS : READY TO TEACH
    </div>
    """, unsafe_allow_html=True)
    
    # Chat History
    for msg in st.session_state.messages:
        avatar = "👤" if msg["role"] == "user" else "👨‍🏫"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # Input Box for Teacher Mode
    prompt = st.chat_input("कोई भी पढ़ाई का सवाल पूछें, Anurag Sir...", key="teacher_input")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

# ================= API RESPONSE TRIGGER =================
# अगर नया मैसेज आया है तो आखिरी मैसेज का जवाब जेनरेट करें
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_prompt = st.session_state.messages[-1]["content"]
    
    # चेक करें कि यूजर इस वक्त किस टैब/मोड पर है
    # Streamlit में एक्टिव टैब का पता लगाने के लिए हम इनपुट की की (key) के हिसाब से मोड तय करेंगे
    current_mode = "Teacher" if st.as_穩定_internal_state if "teacher_input" in st.context else "Hacker"
    
    # असल में आसान तरीका है कि हम सेशन स्टेट या सिंपल कंडीशन से डिटेक्ट करें
    # यहाँ हम डिफ़ॉल्ट रूप से एक्टिव विजेट से मोड उठा लेंगे
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("⚡ PROCESSING DATA..."):
            reply = fetch_unlimited_response(last_prompt, mode=current_mode)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()
