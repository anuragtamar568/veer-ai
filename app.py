import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text
import streamlit.components.v1 as components
from PIL import Image
import numpy as np
import cv2
import time

# 1. 🔥 CYBERPUNK PREMIUM THEME
st.set_page_config(page_title="VEER_OS // QUANTUM_CORE", page_icon="🥷", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at center, #0a1128 0%, #000411 100%) !important;
    }
    h1 {
        color: #00ffaa !important; 
        text-transform: uppercase; 
        letter-spacing: 6px; 
        text-shadow: 0 0 20px rgba(0, 255, 170, 0.6);
        text-align: center;
        font-weight: 800 !important;
    }
    .status-panel {
        background: rgba(0, 255, 170, 0.03);
        border: 1px solid rgba(0, 255, 170, 0.2);
        padding: 15px;
        border-radius: 8px;
        color: #00ffaa !important;
        font-family: monospace !important;
    }
    .security-box { 
        text-align: center; 
        margin-top: 20px; 
        padding: 35px;
        border: 1px solid rgba(255, 46, 99, 0.3);
        background: rgba(10, 15, 30, 0.8);
        border-radius: 16px;
    }
    .secure-text-red {
        color: #ff2e63 !important;
        font-size: 18px !important;
        font-weight: bold;
        letter-spacing: 4px;
    }
    div[data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.02) !important; 
        border-left: 4px solid #00ffaa !important; 
        border-radius: 8px !important;
    }
    .stButton>button {
        background: linear-gradient(45deg, #ff2e63, #ff0055) !important;
        color: white !important;
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# वॉइस इंजन
def speak_natural(text):
    clean_text = text.replace('"', '').replace("'", "").replace("\n", " ")
    js = f"<script>window.speechSynthesis.cancel(); var msg = new SpeechSynthesisUtterance('{clean_text}'); msg.lang = 'hi-IN'; window.speechSynthesis.speak(msg);</script>"
    components.html(js, height=0)

# API कॉन्फ़िगरेशन
if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"].strip():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("[FATAL]: Gemini API Key Missing in Streamlit Secrets.")
    st.stop()

# Session States
if "unlocked" not in st.session_state:
    st.session_state.unlocked = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_voice" not in st.session_state:
    st.session_state.last_voice = ""

# --- 🎛️ SECURITY GATEWAY WITH EMERGENCY BYPASS ---
if not st.session_state.unlocked:
    st.markdown("<div class='security-box'>", unsafe_allow_html=True)
    st.title("🛡️ VEER EYE // BIOMETRIC LOCK")
    
    # 1. फ़र्स्ट टाइम सेटअप (चेहरा रजिस्टर करना)
    if "registered_face" not in st.session_state:
        st.markdown("<div class='secure-text-red' style='color:#00ffaa !important;'>[NEW CORE SETUP]: NO SECURE FACE DETECTED</div>", unsafe_allow_html=True)
        reg_shot = st.camera_input("अनुराग सर, कैमरे के सामने बिल्कुल सीधे देखें और अपना चेहरा रजिस्टर करें:")
        if reg_shot:
            file_bytes = np.asarray(bytearray(reg_shot.read()), dtype=np.uint8)
            opencv_img = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
            st.session_state.registered_face = cv2.resize(opencv_img, (200, 200))
            st.success("चेहरा सफलतापूर्वक मेमोरी में सुरक्षित हो गया है सर!")
            time.sleep(1)
            st.rerun()
            
    # 2. लॉगिन स्क्रीन (चेहरा मैचिंग + सीक्रेट बाईपास)
    else:
        st.markdown("<div class='secure-text-red'>🔒 SYSTEM STATUS: SECURE LOCKED</div>", unsafe_allow_html=True)
        login_shot = st.camera_input("🤖 बायो-स्कैन के लिए अपना चेहरा दिखाएं सर:")
        
        if login_shot:
            try:
                file_bytes2 = np.asarray(bytearray(login_shot.read()), dtype=np.uint8)
                img2 = cv2.imdecode(file_bytes2, cv2.IMREAD_GRAYSCALE)
                img2 = cv2.resize(img2, (200, 200))
                
                img1 = st.session_state.registered_face
                diff = cv2.absdiff(img1, img2)
                mean_diff = np.mean(diff)
                
                # यहाँ हमने वैल्यू थोड़ी बढ़ा दी है (65) ताकि हल्की खराब रोशनी में भी यह आपको पहचान ले
                if mean_diff < 65:
                    st.session_state.unlocked = True
                    st.rerun()
                else:
                    st.error("❌ ACCESS DENIED: अनधिकृत चेहरा! आप अनुराग सर नहीं हैं।")
                    components.html("<script>var m = new SpeechSynthesisUtterance('एक्सेस डिनाइड।'); m.lang='hi-IN'; window.speechSynthesis.speak(m);</script>", height=0)
            except:
                st.error("स्कैनिंग में दिक्कत आई।")

        # --- 🤫 EMERGENCY BYPASS OPTION ---
        st.write("---")
        with st.expander("🔑 Emergency Passcode (अगर फेस मैच न हो)"):
            bypass_code = st.text_input("अपना सीक्रेट मास्टर कोड डालें सर:", type="password")
            if st.button("Unlock via Code"):
                # आप यहाँ '1234' की जगह अपना कोई भी मनपसंद कोड रख सकते हैं
                if bypass_code == "1234": 
                    st.session_state.unlocked = True
                    st.success("मास्टर कोड वेरिफाइड! सिस्टम अनलॉक...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("गलत मास्टर कोड!")
                    
    st.markdown("</div>", unsafe_allow_html=True)

# --- 💻 QUANTUM MAINFRAME WORKSTATION (VEER ACTIVE) ---
else:
    if "welcomed" not in st.session_state:
        components.html("<script>var m = new SpeechSynthesisUtterance('सिस्टम अनलॉक। स्वागत है अनुराग सर।'); m.lang='hi-IN'; window.speechSynthesis.speak(m);</script>", height=0)
        st.session_state.welcomed = True

    st.title("VEER QUANTUM AI 🤖 👁️")
    st.markdown("<div class='status-panel'>⚡ STATUS: MAIN_FRAME_CONNECTED // IDENTITY: VERIFIED // OWNER: ANURAG SIR</div>", unsafe_allow_html=True)

    # कंट्रोल हब
    col1, col2 = st.columns([7, 3])
    with col2:
        if st.button("🔒 Terminate Session"):
            st.session_state.unlocked = False
            if "welcomed" in st.session_state: del st.session_state["welcomed"]
            st.rerun()
    with col1:
        if st.button("🗑️ Wipe Logs (Clear Chat)"):
            st.session_state.chat_history = []
            st.session_state.last_voice = ""
            st.rerun()

    # --- 👀 LIVE OPTICAL HUB ---
    st.markdown("### 👁️ वीर की लाइव आँख (Analyze Live Feed)")
    
    input_mode = st.radio("इनपुट का तरीका चुनें सर:", ["🎥 लाइव वेबकैम (Live Camera)", "📁 गैलरी से फोटो अपलोड करें"])
    
    active_image = None
    if input_mode == "🎥 लाइव वेबकैम (Live Camera)":
        cam_shot = st.camera_input("कैमरे के सामने कोई भी चीज़ लाएं और फोटो क्लिक करें सर:")
        if cam_shot:
            active_image = Image.open(cam_shot)
    else:
        uploaded_image = st.file_uploader("गैलरी से कोई भी फोटो अपलोड करें...", type=["jpg", "jpeg", "png"])
        if uploaded_image:
            active_image = Image.open(uploaded_image)

    # --- CHAT INPUTS ---
    voice_input = speech_to_text(language='hi', use_container_width=True, key='stable_mic')
    text_input = st.chat_input("Yahan apna sawal likho ya bolo...")

    final_input = None
    if voice_input and voice_input.strip() and voice_input != st.session_state.last_voice:
        final_input = voice_input
        st.session_state.last_voice = voice_input
    elif text_input and text_input.strip():
        final_input = text_input

    # चैट रेंडरर
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.write(chat["content"])

    # जेमिनी सुपर कोर लॉजिक
    if final_input:
        st.session_state.chat_history.append({"role": "user", "content": final_input})
        with st.chat_message("user"):
            st.write(final_input)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            try:
                with st.spinner("वीर सोच रहा है..."):
                    sys_prompt = (
                        "तुम 'वीर' (VEER AI) हो, जिसे तुम्हारे मालिक 'अनुराग सर' ने बनाया है। "
                        "तुम अनुराग सर के प्रति पूरी तरह वफादार हो। हमेशा उन्हें 'अनुराग सर' या 'सर' कहकर संबोधित करो। "
                        "अगर कोई इमेज दी गई है, तो उसे ध्यान से देखो और अनुराग सर को उसका सटीक और देसी हिंदी में जवाब दो।"
                    )
                    
                    model = genai.GenerativeModel("gemini-2.0-flash")
                    if active_image:
                        response = model.generate_content([sys_prompt, active_image, final_input])
                    else:
                        response = model.generate_content([sys_prompt, final_input])
                    
                    reply = response.text
                    
            except Exception as e:
                reply = f"अनुराग सर, सर्वर पर थोड़ा लोड है, लेकिन मैं आपके साथ हूँ। आपने पूछा: '{final_input}'"
                    
            placeholder.write(reply)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            speak_natural(reply)
                # रजिस्टर्ड फोटो से मैचिंग (पिक्सेल टू पिक्सेल डिफरेंस)
                img1 = st.session_state.registered_face
                diff = cv2.absdiff(img1, img2)
                mean_diff = np.mean(diff)
                
                if mean_diff < 40:
                    st.session_state.unlocked = True
                    st.rerun()
                else:
                    st.error("❌ ACCESS DENIED: अनधिकृत चेहरा! आप अनुराग सर नहीं हैं।")
                    components.html("<script>var m = new SpeechSynthesisUtterance('एक्सेस डिनाइड। चेहरा मैच नहीं हुआ।'); m.lang='hi-IN'; window.speechSynthesis.speak(m);</script>", height=0)
            except:
                st.error("स्कैनिंग में कोई दिक्कत आई, कृपया दोबारा कोशिश करें।")
                
    st.markdown("</div>", unsafe_allow_html=True)

# --- 💻 QUANTUM MAINFRAME WORKSTATION (VEER ACTIVE) ---
else:
    if "welcomed" not in st.session_state:
        components.html("<script>var m = new SpeechSynthesisUtterance('सिस्टम अनलॉक। स्वागत है अनुराग सर।'); m.lang='hi-IN'; window.speechSynthesis.speak(m);</script>", height=0)
        st.session_state.welcomed = True

    st.title("VEER QUANTUM AI 🤖 👁️")
    st.markdown("<div class='status-panel'>⚡ STATUS: MAIN_FRAME_CONNECTED // IDENTITY: VERIFIED // OWNER: ANURAG SIR</div>", unsafe_allow_html=True)

    # कंट्रोल हब
    col1, col2 = st.columns([7, 3])
    with col2:
        if st.button("🔒 Terminate Session"):
            st.session_state.unlocked = False
            if "welcomed" in st.session_state: del st.session_state["welcomed"]
            st.rerun()
    with col1:
        if st.button("🗑️ Wipe Logs (Clear Chat)"):
            st.session_state.chat_history = []
            st.session_state.last_voice = ""
            st.rerun()

    # --- 👀 LIVE OPTICAL HUB ---
    st.markdown("### 👁️ वीर की लाइव आँख (Analyze Live Feed)")
    
    input_mode = st.radio("इनपुट का तरीका चुनें सर:", ["🎥 लाइव वेबकैम (Live Camera)", "📁 गैलरी से फोटो अपलोड करें"])
    
    active_image = None
    if input_mode == "🎥 लाइव वेबकैम (Live Camera)":
        cam_shot = st.camera_input("कैमरे के सामने कोई भी चीज़ लाएं और फोटो क्लिक करें सर:")
        if cam_shot:
            active_image = Image.open(cam_shot)
    else:
        uploaded_image = st.file_uploader("गैलरी से कोई भी फोटो अपलोड करें...", type=["jpg", "jpeg", "png"])
        if uploaded_image:
            active_image = Image.open(uploaded_image)

    # --- CHAT INPUTS ---
    voice_input = speech_to_text(language='hi', use_container_width=True, key='stable_mic')
    text_input = st.chat_input("Yahan apna sawal likho ya bolo...")

    final_input = None
    if voice_input and voice_input.strip() and voice_input != st.session_state.last_voice:
        final_input = voice_input
        st.session_state.last_voice = voice_input
    elif text_input and text_input.strip():
        final_input = text_input

    # चैट रेंडरर
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.write(chat["content"])

    # जेमिनी सुपर कोर लॉजिक
    if final_input:
        st.session_state.chat_history.append({"role": "user", "content": final_input})
        with st.chat_message("user"):
            st.write(final_input)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            try:
                with st.spinner("वीर सोच रहा है..."):
                    sys_prompt = (
                        "तुम 'वीर' (VEER AI) हो, जिसे तुम्हारे मालिक 'अनुराग सर' ने बनाया है। "
                        "तुम अनुराग सर के प्रति पूरी तरह वفاदार हो। हमेशा उन्हें 'अनुराग सर' या 'सर' कहकर संबोधित करो। "
                        "अगर कोई इमेज दी गई है, तो उसे ध्यान से देखो और अनुराग सर को उसका सटीक और देसी हिंदी में जवाब दो।"
                    )
                    
                    model = genai.GenerativeModel("gemini-2.0-flash")
                    if active_image:
                        response = model.generate_content([sys_prompt, active_image, final_input])
                    else:
                        response = model.generate_content([sys_prompt, final_input])
                    
                    reply = response.text
                    
            except Exception as e:
                reply = f"अनुराग सर, सर्वर पर थोड़ा लोड है, लेकिन मैं आपके साथ हूँ। आपने पूछा: '{final_input}'"
                    
            placeholder.write(reply)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            speak_natural(reply)
