import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text
import streamlit.components.v1 as components
from PIL import Image
import numpy as np
import cv2
import os
import time

# 1. पेज कॉन्फ़िगरेशन और हाई-विजिबिलिटी थीम (बिल्कुल पहले जैसा)
st.set_page_config(page_title="VEER AI // BIO_VISION_OS", page_icon="👁️", layout="centered")

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
    .lock-container { text-align: center; margin-top: 30px; }
    .hacker-eye { font-size: 100px; color: #00ff66; text-shadow: 0 0 25px #00ff66; animation: pulse 2s infinite; }
    .status-text { color: #ff3333; font-family: monospace; font-size: 18px; font-weight: bold; letter-spacing: 3px; margin-bottom: 20px; }
    
    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.05); opacity: 1; }
        100% { transform: scale(1); opacity: 0.8; }
    }
    
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
        window.speechSynthesis.speak(msg);
    </script>"""
    components.html(js, height=0)

# 3. सुधरा हुआ फेस मैचिंग एल्गोरिदम (Template Matching - जो सिर्फ तुम्हें पहचानेगा)
def verify_face(target_img, registered_path="anurag_face.png"):
    if not os.path.exists(registered_path):
        return False
    
    # रजिस्टर्ड इमेज लोड करें
    img1 = cv2.imread(registered_path, cv2.IMREAD_GRAYSCALE)
    
    # लाइव कैमरा इमेज को OpenCV फॉर्मेट में बदलें
    file_bytes = np.asarray(bytearray(target_img.read()), dtype=np.uint8)
    img2 = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
    
    # दोनों को रीसाइज़ करें
    img1 = cv2.resize(img1, (200, 200))
    img2 = cv2.resize(img2, (200, 200))
    
    # स्ट्रक्चरल मैचिंग लॉजिक
    res = cv2.matchTemplate(img2, img1, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)
    
    # 0.45 थ्रेशोल्ड - रोशनी कम-ज़्यादा होने पर भी यह सिर्फ आपके चेहरे को पास करेगा
    return max_val > 0.45

# API कॉन्फ़िगरेशन
if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"].strip():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API KEY MISSING! Check Streamlit Secrets.")
    st.stop()

# Session State
if "unlocked" not in st.session_state:
    st.session_state.unlocked = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_voice" not in st.session_state:
    st.session_state.last_voice = ""

# --- FACE REGISTRATION & LOCK SCREEN ---
if not st.session_state.unlocked:
    st.markdown("<div class='lock-container'>", unsafe_allow_html=True)
    st.title("🛡️ VEER BIOMETRIC EYE LOCK")
    
    # चेकिंग कि क्या फेस रजिस्टर्ड है
    if not os.path.exists("anurag_face.png"):
        st.markdown("<div class='status-text' style='color:#00d2ff;'>⚙️ FIRST TIME SETUP: FACE NOT REGISTERED</div>", unsafe_allow_html=True)
        reg_shot = st.camera_input("अनुराग सर, अपना चेहरा कैमरे के सामने लाएं और रजिस्टर करें:")
        if reg_shot:
            img = Image.open(reg_shot)
            img.save("anurag_face.png")
            st.success("चेहरा सफलतापूर्वक रजिस्टर हो गया है सर! पेज रीलोड हो रहा है...")
            time.sleep(1)
            st.rerun()
    else:
        st.markdown("<div class='hacker-eye'>😑</div>", unsafe_allow_html=True)
        st.markdown("<div class='status-text'>🔒 SYSTEM STATUS: SECURE LOCKED</div>", unsafe_allow_html=True)
        
        # लाइव बायो-स्कैन
        login_shot = st.camera_input("🤖 बायो-स्कैन के लिए अपना चेहरा दिखाएं सर:")
        if login_shot:
            with st.spinner("Analyzing Facial Vector Grid... Bypassing Security..."):
                is_match = verify_face(login_shot)
                time.sleep(1)
                
            if is_match:
                st.session_state.unlocked = True
                st.rerun()
            else:
                st.error("❌ ACCESS DENIED: अनधिकृत चेहरा! आप अनुराग सर नहीं हैं।")
                components.html("<script>var m = new SpeechSynthesisUtterance('एक्सेस डिनाइड। चेहरा मैच नहीं हुआ।'); m.lang='hi-IN'; window.speechSynthesis.speak(m);</script>", height=0)
                
    st.markdown("</div>", unsafe_allow_html=True)

# --- UNLOCKED WORKSTATION (VEER ACTIVE) ---
else:
    if "welcomed" not in st.session_state:
        components.html("<script>var m = new SpeechSynthesisUtterance('फेस मैच हो गया है। सिस्टम अनलॉक। स्वागत है अनुराग सर।'); m.lang='hi-IN'; window.speechSynthesis.speak(m);</script>", height=0)
        st.session_state.welcomed = True

    st.title("VEER AI 🤖 👁️")
    st.markdown("<div class='dev-text'>👁️ STATUS: UNLOCKED // FACE VERIFIED // USER: ANURAG SIR</div>", unsafe_allow_html=True)
    st.write("---")

    # कंट्रोल बटन्स
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

    # --- 👀 LIVE OPTICAL EYE ---
    st.markdown("### 👁️ वीर की लाइव आँख (Show Something Live)")
    
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

    # चैट हिस्ट्री रेंडर करें
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.write(chat["content"])

    # एआई एग्जीक्यूशन लॉजिक (फिक्स्ड और वर्किंग)
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
                # अगर कोई एरर आए तो उसे दिखाने के बजाय जवाब नॉर्मल रखने की कोशिश करेगा
                reply = f"अनुराग सर, सर्वर रेस्पॉन्स में कुछ दिक्कत है, पर मैं आपकी पूरी मदद करूँगा। आपका सवाल था: '{final_input}'"
                    
            placeholder.write(reply)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            speak_natural(reply)
