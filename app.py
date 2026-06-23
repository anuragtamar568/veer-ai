import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
from PIL import Image

# 1. सिंपल और क्लीन थीम सेटिंग
st.set_page_config(page_title="VEER AI", page_icon="🤖", layout="centered")

# वॉइस इंजन (नेचुरल हिंदी स्पीच)
def speak_natural(text):
    clean_text = text.replace('"', '').replace("'", "").replace("\n", " ")
    js = f"<script>window.speechSynthesis.cancel(); var msg = new SpeechSynthesisUtterance('{clean_text}'); msg.lang = 'hi-IN'; window.speechSynthesis.speak(msg);</script>"
    components.html(js, height=0)

# API की चेकिंग
if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"].strip():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key नहीं मिली। कृपया Streamlit Secrets में GEMINI_API_KEY जोड़ें।")
    st.stop()

# चैट हिस्ट्री के लिए मेमोरी
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🤖 वीर AI असिस्टेंट")

# चैट क्लियर करने का बटन
if st.button("🗑️ क्लियर चैट"):
    st.session_state.chat_history = []
    st.rerun()

# --- इनपुट सेक्शन (कैमरा या गैलरी) ---
st.write("### 👁️ वीर की आँख")
input_mode = st.radio("इनपुट का तरीका चुनें:", ["📷 लाइव कैमरा", "📁 फोटो अपलोड करें"])
active_image = None

if input_mode == "📷 लाइव कैमरा":
    cam_shot = st.camera_input("कैमरे के सामने ऑब्जेक्ट लाएं और फोटो खींचें सर:")
    if cam_shot:
        active_image = Image.open(cam_shot)
else:
    uploaded_image = st.file_uploader("गैलरी से फोटो चुनें...", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        active_image = Image.open(uploaded_image)

# --- चैट इनपुट बॉक्स ---
text_input = st.chat_input("अनुराग सर, यहाँ अपना सवाल लिखें...")

# पहले की बातचीत स्क्रीन पर दिखाना
for chat in st.session_state.chat_history:
    if "role" in chat and "content" in chat:
        with st.chat_message(chat["role"]):
            st.write(chat["content"])

# जेमिनी रिस्पॉन्स कोर लॉजिक
if text_input:
    # यूजर का सवाल जोड़ें
    st.session_state.chat_history.append({"role": "user", "content": text_input})
    with st.chat_message("user"):
        st.write(text_input)

    # वीर का जवाब
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
                
                # हिस्ट्री सेव करें और बोलें
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                speak_natural(reply)
                
            except Exception as e:
                st.write("क्षма करें अनुराग सर, सर्वर से रिस्पॉन्स नहीं मिल पाया। कृपया दोबारा कोशिश करें।")
