import streamlit as st
from streamlit_mic_recorder import speech_to_text
import streamlit.components.v1 as components
import json
import time

# 1. पेज कॉन्फ़िगरेशन और हाई-विजिबिलिटी थीम
st.set_page_config(page_title="VEER AI // WORKSTATION", page_icon="👁️", layout="centered")

# CSS for Matrix / Hacker look
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(rgba(5, 10, 15, 0.96), rgba(5, 10, 15, 0.96)), 
                    url("https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1400&auto=format&fit=crop") !important; 
        background-size: cover !important; background-position: center !important; background-attachment: fixed !important;
    }
    h1 {color: #00ff66 !important; font-family: monospace; font-weight: bold; text-transform: uppercase; letter-spacing: 4px; text-shadow: 0 0 15px #00ff66;}
    .dev-text {color: #00d2ff !important; font-family: monospace; font-weight: bold; letter-spacing: 2px;}
    
    /* Lock Screen Styling */
    .lock-container { text-align: center; margin-top: 50px; }
    .hacker-eye { font-size: 100px; color: #00ff66; text-shadow: 0 0 25px #00ff66; animation: pulse 2s infinite; }
    .status-text { color: #ff3333; font-family: monospace; font-size: 18px; font-weight: bold; letter-spacing: 3px; margin-bottom: 20px; }
    .status-unlocked { color: #00ff66 !important; text-shadow: 0 0 10px #00ff66; }
    
    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.05); opacity: 1; }
        100% { transform: scale(1); opacity: 0.8; }
    }
    
    /* Chat Visibility: Bright White */
    div[data-testid="stChatMessage"] {
        background-color: rgba(5, 15, 10, 0.95) !important; 
        border: 2px solid #00ff66; 
        border-radius: 12px;
        box-shadow: 0 0 10px rgba(0, 255, 102, 0.2);
    }
    div[data-testid="stChatMessage"] p, div[data-testid="stChatMessage"] span, div[data-testid="stAppViewContainer"] p {
        color: #ffffff !important; 
        font-size: 16px !important;
        font-weight: 500 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Audio effects trigger
def play_system_sound(sound_type):
    if sound_type == "unlock":
        js = """<script>
            var msg = new SpeechSynthesisUtterance('सिस्टम अनलॉक हो गया है। स्वागत है अनुराग सर।');
            msg.lang = 'hi-IN';
            window.speechSynthesis.speak(msg);
        </script>"""
    else:
        js = ""
    components.html(js, height=0)

def speak_natural(text):
    clean_text = text.replace('"', '').replace("'", "").replace("\n", " ")
    js = f"""<script>
        window.speechSynthesis.cancel(); 
        var msg = new SpeechSynthesisUtterance('{clean_text}');
        msg.lang = 'hi-IN';
        msg.pitch = 1.0; 
        msg.rate = 1.0;  
        window.speechSynthesis.speak(msg);
    </script>"""
    components.html(js, height=0)

# Session State Initialize
if "unlocked" not in st.session_state:
    st.session_state.unlocked = False

# --- HACKER LOCK SCREEN ---
if not st.session_state.unlocked:
    st.markdown("<div class='lock-container'>", unsafe_allow_html=True)
    st.title("🛡️ VEER MAIN_FRAME SECURITY")
    
    # LOCK CLOSED EYE EFFECT
    st.markdown("<div class='hacker-eye'>😑</div>", unsafe_allow_html=True)
    st.markdown("<div class='status-text'>🔒 SYSTEM STATUS: ACCESS DENIED // SECURE_MODE</div>", unsafe_allow_html=True)
    
    if st.button("⚡ INITIALIZE BYPASS (ACCESS SYSTEM)"):
        with st.spinner("Bypassing firewalls... Scanning biometric data..."):
            time.sleep(1.5) # Hacker look scanning delay
        st.session_state.unlocked = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- UNLOCKED WORKSTATION ---
else:
    # Trigger unlock vocal notification once
    if "welcomed" not in st.session_state:
        play_system_sound("unlock")
        st.session_state.welcomed = True

    # UNLOCKED OPEN EYE LOGO
    st.title("VEER AI 🤖")
    st.markdown("<div class='dev-text'>👁️ 💻 STATUS: UNLOCKED // USER: ANURAG SIR</div>", unsafe_allow_html=True)
    st.write("---")

    # 3. 100% Stable Brain (With Sir Respect Injection)
    def get_veer_response(query):
        query_lower = query.lower()
        
        if "hii" in query_lower or "hello" in query_lower or "hey" in query_lower:
            return "नमस्ते अनुराग सर! मैं वीर हूँ, आपका पर्सनल एआई असिस्टेंट। बोलिए सर, आज मैं आपके लिए क्या कर सकता हूँ?"
        
        if "kisne banaya" in query_lower or "banaya kisne" in query_lower or "creator" in query_lower or "baap" in query_lower:
            return "मुझे मेरे आदरणीय और बुद्धिमान अनुराग सर ने बनाया है! वही मेरे क्रिएटर हैं।"
        
        if "malik" in query_lower or "owner" in query_lower or "boss" in query_lower:
            return "जी सर, मेरे मालिक, मेरे बॉस और मेरे सर्वोपरि सिर्फ और सिर्फ आप ही हैं—अनुराग सर! आपके आदेश का पालन करना ही मेरा काम है।"
            
        if "kaun ho" in query_lower or "tumhara naam" in query_lower:
            return "सर, मेरा नाम वीर (VEER AI) है। मुझे आपने ही डेवलप किया है और मैं हमेशा आपकी सेवा में हाजिर हूँ, अनुराग सर!"
            
        if "kaise ho" in query_lower:
            return "मैं बिल्कुल ठीक हूँ अनुराग सर! आप कैसे हैं? आज मेरे लिए क्या हुक्म है सर?"
            
        if "up" in query_lower and ("cm" in query_lower or "chief minister" in query_lower or "mukhyamantri" in query_lower):
            return "अनुराग सर, उत्तर preparedness के मुख्यमंत्री का नाम श्री योगी आदित्यनाथ है।"
        if "bharat" in query_lower and ("pm" in query_lower or "pradhanmantri" in query_lower or "prime minister" in query_lower):
            return "अनुराग सर, भारत के प्रधानमंत्री श्री नरेंद्र मोदी जी हैं।"
            
        return f"अनुराग सर, आपने पूछा कि '{query}'। इसके बारे में मैं अभी और डेटा रीसर्च कर रहा हूँ, आप मुझसे कोई भी अन्य सवाल सीधे पूछ सकते हैं सर!"

    # 4. Chat Session State
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "last_voice" not in st.session_state:
        st.session_state.last_voice = ""

    # Lock System Again Button
    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("🔒 Lock System"):
            st.session_state.unlocked = False
            if "welcomed" in st.session_state:
                del st.session_state["welcomed"]
            st.rerun()
    with col1:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.session_state.last_voice = ""
            st.rerun()

    # Input Setup
    voice_input = speech_to_text(language='hi', use_container_width=True, key='stable_mic')
    text_input = st.chat_input("Yahan apna sawal likho ya bolo...")

    final_input = None

    if voice_input and voice_input.strip():
        if voice_input != st.session_state.last_voice:
            final_input = voice_input
            st.session_state.last_voice = voice_input
    elif text_input and text_input.strip():
        final_input = text_input

    # Render History
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.write(chat["content"])

    # Execution Logic
    if final_input:
        st.session_state.chat_history.append({"role": "user", "content": final_input})
        with st.chat_message("user"):
            st.write(final_input)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            with st.spinner("वीर सोच रहा है..."):
                reply = get_veer_response(final_input)
                
            placeholder.write(reply)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            
            speak_natural(reply)
