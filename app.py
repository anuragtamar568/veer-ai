import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text
import streamlit.components.v1 as components
from PIL import Image
import time

# 1. पेज कॉन्फ़िगरेशन (यहाँ title को page_title कर दिया है, अब एरर नहीं आएगा)
st.set_page_config(page_title="VEER AI // VISION_OS", page_icon="👁️", layout="centered")

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
    
    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.05); opacity: 1; }
        100% { transform: scale(1); opacity: 0.8; }
    }
    
    /* Text Visibility: Bright White */
    div[data-testid="stChatMessage"] {
        background-color: rgba(5, 15, 10, 0.95) !important; 
        border: 2px solid #00ff66; 
        border-radius: 12px;
    }
    div[data-testid="stChatMessage"] p, div[data-testid="stChatMessage"] span, div[data-testid="stAppViewContainer"] p {
        color: #ffffff !important; 
        font-size: 16px !important;
        font-weight: 500 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. नेचुरल वॉइस इंजन
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

# 3. API की चेकिंग
if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"].strip():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API KEY MISSING! Streamlit Settings -> Secrets में GEMINI_API_KEY सेट करो सर।")
    st.stop()

# Session State Initialize
if "unlocked" not in st.session_state:
    st.session_state.unlocked = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_voice" not in st.session_state:
    st.session_state.last_voice = ""

# --- HACKER LOCK SCREEN ---
if not st.session_state.unlocked:
    st.markdown("<div class='lock-container'>", unsafe_allow_html=True)
    st.title("🛡️ VEER VISION_OS SECURITY")
    st.markdown("<div class='hacker-eye'>😑</div>", unsafe_allow_html=True)
    st.markdown("<div class='status-text'>🔒 SYSTEM STATUS: LOCKED // VISION_OFF</div>", unsafe_allow_html=True)
    
    if st.button("⚡ INITIALIZE BYPASS (ACCESS SYSTEM)"):
        with st.spinner("Activating Neural Optics... Bypassing Firewalls..."):
            time.sleep(1.5)
        st.session_state.unlocked = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- UNLOCKED WORKSTATION ---
else:
    if "welcomed" not in st.session_state:
        components.html("<script>var m = new SpeechSynthesisUtterance('सिस्टम अनलॉक हो गया है। वीर की आंखें अब खुली हैं। स्वागत है अनुराग सर।'); m.lang='hi-IN'; window.speechSynthesis.speak(m);</script>", height=0)
        st.session_state.welcomed = True

    st.title("VEER AI 🤖 👁️")
    st.markdown("<div class='dev-text'>👁️ STATUS: UNLOCKED // OPTICAL SENSORS ONLINE // USER: ANURAG SIR</div>", unsafe_allow_html=True)
    st.write("---")

    # Lock & Clear Buttons
    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("🔒 Lock System"):
            st.session_state.unlocked = False
            if "welcomed" in st.session_state: del st.session_state["welcomed"]
            st.rerun()
    with col1:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.session_state.last_voice = ""
            st.rerun()

    # --- 👀 EYE INPUT: IMAGE UPLOADER ---
    st.markdown("### 👁️ वीर की आँख (Upload Image/Photo to Show Him)")
    uploaded_image = st.file_uploader("Koi bhi photo ya screenshot upload karo jo tum VEER ko dikhana chahte ho...", type=["jpg", "jpeg", "png"])
    
    if uploaded_image:
        st.image(uploaded_image, caption="VEER is looking at this image...", width=300)

    # --- CHAT INPUTS ---
    voice_input = speech_to_text(language='hi', use_container_width=True, key='stable_mic')
    text_input = st.chat_input("Yahan apna sawal likho ya bolo...")

    final_input = None
    if voice_input and voice_input.strip() and voice_input != st.session_state.last_voice:
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
            try:
                with st.spinner("वीर देख रहा है और सोच रहा है..."):
                    sys_prompt = (
                        "तुम 'वीर' (VEER AI) हो, जिसे तुम्हारे मालिक 'अनुराग सर' ने बनाया है। "
                        "तुम अनुराग सर के प्रति पूरी तरह वफादार हो। हमेशा उन्हें 'अनुराग सर' या 'सर' कहकर संबोधित करो। "
                        "अगर कोई इमेज दी गई है, तो उसे ध्यान से देखो और अनुराग सर को उसका सटीक और देसी हिंदी में जवाब दो। "
                        "तुम्हारी भाषा दोस्ताना, आदरपूर्ण और कड़क होनी चाहिए।"
                    )
                    
                    if uploaded_image:
                        img = Image.open(uploaded_image)
                        model = genai.GenerativeModel("gemini-2.0-flash")
                        response = model.generate_content([sys_prompt, img, final_input])
                    else:
                        model = genai.GenerativeModel("gemini-2.0-flash")
                        response = model.generate_content([sys_prompt, final_input])
                    
                    reply = response.text
                    
                placeholder.write(reply)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                
                speak_natural(reply)
                
            except Exception as e:
                placeholder.error(f"System Error: {e}")
