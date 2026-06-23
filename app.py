import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
from PIL import Image

# 1. ✨ CLEAN AND LIGHT PROFESSIONAL THEME
st.set_page_config(page_title="VEER AI // ASSISTANT", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    /* पूरी तरह से साफ सफेद बैकग्राउंड */
    .stApp {
        background-color: #ffffff !important;
    }
    h1 {
        color: #2c3e50 !important;
        text-align: center;
        font-family: sans-serif !important;
        font-weight: 700;
    }
    .stChatMessage {
        background-color: #f8f9fa !important;
        border: 1px solid #dee2e6 !important;
        border-radius: 10px !important;
        color: #000000 !important;
    }
    .stButton>button {
        background-color: #007bff !important;
        color: white !important;
        border: none !important;
        border-radius: 6px;
    }
    p, span, label {
        color: #2c3e50 !important;
    }
    </style>
""", unsafe_allow_html=True)

# वॉइस इंजन (नेचुरल हिंदी स्पीच)
def speak_natural(text):
    clean_text = text.replace('"', '').replace("'", "").replace("\n", " ")
    js = f"<script>window.speechSynthesis.cancel(); var msg = new SpeechSynthesisUtterance('{clean_text}'); msg.lang = 'hi-IN'; window.speechSynthesis.speak(msg);</script>"
    components.html(js, height=0)

# API कॉन्फ़िगरेशन Check
if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"].strip():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key नहीं मिली। कृपया Streamlit Cloud के Secrets में GEMINI_API_KEY जोड़ें।")
    st.stop()

# Session State की शुरुआत
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🤖 वीर AI असिस्टेंट")

# चैट क्लियर करने का बटन
if st.button("🗑️ क्लियर चैट"):
    st.session_state.chat_history = []
    st.rerun()

# --- कैमरा और फाइल इनपुट सेक्शन (सिर्फ ऑब्जेक्ट एनालिसिस के लिए) ---
st.write("### 👁️ वीर की आँख (ऑब्जेक्ट डिटेक्शन)")
input_mode = st.radio("इनपुट का तरीका चुनें:", ["📷 लाइव कैमरा", "📁 फोटो अपलोड करें"])
active_image = None

if input_mode == "📷 लाइव कैमरा":
    cam_shot = st.camera_input("कैमरे के सामने टारगेट ऑब्जेक्ट लाएं और कैप्चर करें सर:")
    if cam_shot:
        active_image = Image.open(cam_shot)
else:
    uploaded_image = st.file_uploader("गैलरी से फोटो चुनें...", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        active_image = Image.open(uploaded_image)

# --- चैट इनपुट बॉक्स ---
text_input = st.chat_input("अनुराग सर, यहाँ अपना सवाल लिखें...")

# पहले की चैट स्क्रीन पर दिखाना
for chat in st.session_state.chat_history:
    if "role" in chat and "content" in chat:
        with st.chat_message(chat["role"]):
            st.write(chat["content"])

# जेमिनी रिस्पॉन्स लॉजिक
if text_input:
    # यूजर का सवाल चैट में जोड़ें
    st.session_state.chat_history.append({"role": "user", "content": text_input})
    with st.chat_message("user"):
        st.write(text_input)

    # वीर (AI) का जवाब
    with st.chat_message("assistant"):
        with st.spinner("वीर सोच रहा है..."):
            try:
                model = genai.GenerativeModel("gemini-2.0-flash")
                sys_prompt = "तुम वीर (VEER AI) हो, जिसे तुम्हारे मालिक अनुराग सर ने बनाया है। हमेशा अनुराग सर को सम्मान देते हुए हिंदी में संक्षिप्त और सटीक जवाब दो।"
                
                if active_image:
                    response = model.generate_content([sys_prompt, active_image, text_input])
                else:
                    response = model.generate_content([sys_prompt, text_input])
                
                reply = response.text
                st.write(reply)
                
                # चैट हिस्ट्री अपडेट करें
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                
                # आवाज चालू करें
                speak_natural(reply)
                
            except Exception as e:
                st.write("क्षमा करें अनुराग सर, सर्वर से जुड़ने में कोई दिक्कत आई है।")
        msg.lang = 'hi-IN';
        msg.pitch = 0.9; /* थोड़ी भारी, रोबोटिक हैकर आवाज़ के लिए */
        msg.rate = 1.0;
        window.speechSynthesis.speak(msg);
    </script>"""
    components.html(js, height=0)

# 3. एडवांस फ़िंगरप्रिंट/फ़ेस मैचिंग एल्गोरिदम (Template Structural Tracking)
def verify_face(target_img, registered_path="master_kernel_face.png"):
    if not os.path.exists(registered_path):
        return False
    
    # मास्टर एडमिन का चेहरा लोड करना
    img1 = cv2.imread(registered_path, cv2.IMREAD_GRAYSCALE)
    
    # लाइव कैमरा फीड स्कैन करना
    file_bytes = np.asarray(bytearray(target_img.read()), dtype=np.uint8)
    img2 = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
    
    # ग्रिड साइजिंग स्टेबलाइजेशन
    img1 = cv2.resize(img1, (200, 200))
    img2 = cv2.resize(img2, (200, 200))
    
    # स्ट्रक्चरल मैचिंग
    res = cv2.matchTemplate(img2, img1, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)
    
    # 0.45 सिक्योरिटी थ्रेशोल्ड (केवल ओरिजिनल ओनर के लिए)
    return max_val > 0.45

# API कॉन्फ़िगरेशन
if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"].strip():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("[FATAL ERROR]: GEMINI_API_KEY IS CORRUPTED OR MISSING IN SECRETS.")
    st.stop()

# Session States initialization
if "unlocked" not in st.session_state:
    st.session_state.unlocked = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_voice" not in st.session_state:
    st.session_state.last_voice = ""

# --- 🛰️ SECURITY CORE / LOCK SCREEN INTERFACE ---
if not st.session_state.unlocked:
    st.markdown("<div class='lock-box'>", unsafe_allow_html=True)
    st.title("🥷 VEER_OS // BIOMETRIC LOCK")
    
    # रूट डायरेक्टरी में चेक करना कि क्या कोई एडमिन पहले से रजिस्टर है
    if not os.path.exists("master_kernel_face.png"):
        st.markdown("<div class='status-alert' style='color:#00d2ff !important;'>[SYSTEM NOTICE]: NO ROOT USER DETECTED. INITIALIZING FIRST TIME BIO-SETUP...</div>", unsafe_allow_html=True)
        reg_shot = st.camera_input("MASTER ADM, कैमरे के सामने आएं और अपना फेस रजिस्टर करें:")
        if reg_shot:
            img = Image.open(reg_shot)
            img.save("master_kernel_face.png")
            st.markdown("<div class='status-success'>[SUCCESS]: YOUR FACIAL VECTOR REGISTERED AS CORE ROOT USER! INJECTING KERNEL...</div>", unsafe_allow_html=True)
            time.sleep(1.5)
            st.rerun()
    else:
        st.markdown("<div class='status-alert'>⚠️ KERNEL STATUS: SECURE_LOCKED // ACCESS_RESTRICTED</div>", unsafe_allow_html=True)
        
        # लाइव ऑथेंटिकेशन गेटवे
        login_shot = st.camera_input("⌨️ RUNNING BIO-SCAN: अपना चेहरा स्कैन करें सर...")
        if login_shot:
            with st.spinner("Executing Facial Grid Matching... Injecting Exploit..."):
                is_match = verify_face(login_shot)
                time.sleep(1)
                
            if is_match:
                st.session_state.unlocked = True
                st.rerun()
            else:
                st.markdown("<div class='status-alert'>[X] ACCESS DENIED: UNKNOWN VECTOR DATA! YOU ARE NOT THE REGISTERED ROOT ADMIN.</div>", unsafe_allow_html=True)
                components.html("<script>var m = new SpeechSynthesisUtterance('वार्निंग। अनधिकृत एक्सेस। सिस्टम लॉक है।'); m.lang='hi-IN'; window.speechSynthesis.speak(m);</script>", height=0)
                
    st.markdown("</div>", unsafe_allow_html=True)

# --- 💻 UNLOCKED TERMINAL WORKSTATION (VEER MAINFRAME) ---
else:
    if "welcomed" not in st.session_state:
        components.html("<script>var m = new SpeechSynthesisUtterance('मेनफ्रेम डिक्रिप्टेड। वेलकम बैक, रूट एडमिन। वीर ओ एस एक्टिवेटेड।'); m.lang='hi-IN'; window.speechSynthesis.speak(m);</script>", height=0)
        st.session_state.welcomed = True

    st.title("VEER_OS // CONTROL_PANEL 🤖")
    st.markdown("<div class='kernel-text'>⚡ STATUS: MAIN_FRAME_UNLOCKED // USER: ROOT_ADMIN // ENCRYPTION: AES_256</div>", unsafe_allow_html=True)
    st.write("---")

    # टर्मिनल यूटिलिटी बटन्स
    col1, col2 = st.columns([7, 3])
    with col2:
        if st.button("🔒 Terminate Session (Lock)"):
            st.session_state.unlocked = False
            if "welcomed" in st.session_state: del st.session_state["welcomed"]
            st.rerun()
    with col1:
        if st.button("🗑️ Wipe Logs (Clear Chat)"):
            st.session_state.chat_history = []
            st.session_state.last_voice = ""
            st.rerun()

    # --- 👁️ LIVE OPTICAL OVERRIDE ---
    st.markdown("### 👁️ VEER CYBERNETIC EYE (Feed Live Target Data)")
    
    input_mode = st.radio("SELECT INPUT FEED TYPE:", ["🎥 LIVE CYBER CAM", "📁 INJECT IMAGE FILE"])
    
    active_image = None
    if input_mode == "🎥 LIVE CYBER CAM":
        cam_shot = st.camera_input("कैमरे के सामने टारगेट ऑब्जेक्ट लाएं और कैप्चर करें सर:")
        if cam_shot:
            active_image = Image.open(cam_shot)
    else:
        uploaded_image = st.file_uploader("अपलोड लोकल फ़ाइल...", type=["jpg", "jpeg", "png"])
        if uploaded_image:
            active_image = Image.open(uploaded_image)

    # --- TERMINAL CHAT INPUTS ---
    voice_input = speech_to_text(language='hi', use_container_width=True, key='stable_mic')
    text_input = st.chat_input("Enter command or prompt here root_admin@veer_os:~$ ")

    final_input = None
    if voice_input and voice_input.strip() and voice_input != st.session_state.last_voice:
        final_input = voice_input
        st.session_state.last_voice = voice_input
    elif text_input and text_input.strip():
        final_input = text_input

    # रेंडर टर्मिनल चैट हिस्ट्री
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.write(chat["content"])

    # एक्जीक्यूशन लॉजिक
    if final_input:
        st.session_state.chat_history.append({"role": "user", "content": f"root_admin:~$ {final_input}"})
        with st.chat_message("user"):
            st.write(f"root_admin:~$ {final_input}")

        with st.chat_message("assistant"):
            placeholder = st.empty()
            try:
                with st.spinner("VEER CORE PROCESSING..."):
                    sys_prompt = (
                        "तुम 'वीर' (VEER AI / VEER OS) हो—एक एलीट और खतरनाक हैकर वॉइस असिस्टेंट। "
                        "तुमने अपने क्रिएटर यानी 'रूट एडमिन' (या सर) के लिए यह मेनफ्रेम बनाया है। "
                        "हमेशा बात करते समय थोड़ा हैकर टोन, टेक्निकल शब्द और रोबोटिक गजब का रवैया रखो। "
                        "जवाब को क्रिस्प, कूल और देसी हिंदी मिक्स हैकिंग स्टाइल में दो और उन्हें हमेशा 'सर' या 'रूट एडमिन' कहो।"
                    )
                    
                    model = genai.GenerativeModel("gemini-2.0-flash")
                    if active_image:
                        response = model.generate_content([sys_prompt, active_image, final_input])
                    else:
                        response = model.generate_content([sys_prompt, final_input])
                    
                    reply = f"veer_os_core:~$ {response.text}"
                    
            except Exception as e:
                reply = f"veer_os_core:~$ कनेक्शन एरर सर, लेकिन आपका इनपुट लोड हो गया है: '{final_input}'"
                    
            placeholder.write(reply)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            speak_natural(response.text if 'response' in locals() else "सिस्टम लोड एरर सर")
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
            reply = f"अनुराग सर, सर्वर कनेक्ट करने में थोड़ा समय लग रहा है। आपने पूछा था: '{final_input}'"
                
        placeholder.write(reply)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        speak_natural(reply)
