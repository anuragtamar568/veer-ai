import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text
from PIL import Image

# पेज कॉन्फ़िगरेशन
st.set_page_config(page_title="VEER AI", page_icon="💻", layout="centered")

# डार्क थीम और नियॉन लेटर्स के लिए CSS
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(rgba(10, 15, 25, 0.85), rgba(10, 15, 25, 0.85)), url("https://images.unsplash.com/photo-1542831371-29b0f74f9713?q=80&w=1400&auto=format&fit=crop") !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
}
[data-testid="stHeader"] {
    background: transparent !important;
}
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(rgba(10, 15, 25, 0.85), rgba(10, 15, 25, 0.85)), url("https://images.unsplash.com/photo-1542831371-29b0f74f9713?q=80&w=1400&auto=format&fit=crop") !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
}
[data-testid="stHeader"] {
    background: transparent !important;
}
h1 {
    color: #6bf2ff !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    font-weight: 300 !important;
    text-transform: uppercase;
    letter-spacing: 5px;
    text-shadow: 0 0 10px rgba(107, 242, 255, 0.8), 0 0 25px rgba(107, 242, 255, 0.5);
    margin-bottom: 5px !important;
}
.developer-text {
    color: #00ff66 !important;
    font-family: 'Courier New', Courier, monospace !important;
    font-weight: bold;
    letter-spacing: 2px;
    font-size: 14px;
    text-shadow: 0 0 8px rgba(0, 255, 102, 0.6);
    margin-top: 2px !important;
    margin-bottom: 2px !important;
}
div[data-testid="stChatMessage"] {
    background-color: rgba(8, 20, 30, 0.9) !important;
    border: 2px solid #00d2ff;
    border-radius: 12px;
    box-shadow: 0 0 15px rgba(0, 210, 255, 0.4);
    margin-bottom: 15px;
    padding: 15px !important;
}
p, span, div, label {
    color: #ffffff !important;
    font-family: 'Segoe UI', sans-serif !important;
}
.stChatInputContainer {
    background-color: rgba(5, 10, 15, 0.95) !important;
    border: 2px solid #00d2ff !important;
    border-radius: 8px !important;
}
.stChatInputContainer textarea {
    color: #ffffff !important;
}
.voice-label {
    color: #00ff66 !important;
    font-family: 'Courier New', monospace !important;
    font-weight: bold;
    margin-top: 15px;
}
/* फाइल अपलोडर बॉक्स को साफ़ सुथरा रखना */
[data-testid="stFileUploader"] {
    background-color: rgba(8, 20, 30, 0.6) !important;
    border: 1px dashed #00d2ff !important;
    border-radius: 10px !important;
    padding: 10px !important;
}
::-webkit-scrollbar {
    width: 0px;
    background: transparent;
}
</style>
    color: #050a10 !important;
    box-shadow: 0 0 15px #00ff66 !important;
}
::-webkit-scrollbar {
    width: 0px;
    background: transparent;
}
</style>
""", unsafe_allow_html=True)

# 🎙️ भारी रोबोटिक आवाज़ जनरेट करने वाला फंक्शन
def robot_speak(text_to_say):
    clean_text = text_to_say.replace("'", "\\'").replace('"', '\\"').replace("\n", " ")
    js_code = f"""
    <script>
    if ('speechSynthesis' in window) {{
        window.speechSynthesis.cancel();
        var msg = new SpeechSynthesisUtterance("{clean_text}");
        msg.pitch = 0.3;  
        msg.rate = 0.85;  
        msg.volume = 1.0;
        
        var voices = window.speechSynthesis.getVoices();
        for(var i = 0; i < voices.length; i++) {{
            if(voices[i].lang.indexOf('hi-IN') >= 0 || voices[i].name.toLowerCase().includes('google')) {{
                msg.voice = voices[i];
                break;
            }}
        }}
        window.speechSynthesis.speak(msg);
    }}
    </script>
    """
    st.components.v1.html(js_code, height=0, width=0)

# हेडर लेआउट
st.title("VEER AI")
st.markdown("<div class='developer-text'>SPECIALIST WORKSTATION</div>", unsafe_allow_html=True)
st.markdown("<div class='developer-text'>DEVELOPER: ANURAG // SECURE CONNECTION</div>", unsafe_allow_html=True)
st.write("---")

# --- 🔐 पर्सनल पासवर्ड प्रोटेक्शन लॉजिक ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("### 🔒 SECURE LOGIN REQUIRED")
    password_input = st.text_input("ENTER ACCESS KEY // सिर्फ अनुराग के लिए:", type="password")
    if st.button("ACCESS SYSTEM"):
        if password_input == "anurag123": 
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ ACCESS DENIED // INVALID ACCESS KEY")
    st.stop()

# API Configuration
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ API Key नहीं मिली! कृपया Streamlit Secrets में GEMINI_API_KEY सेट करें।")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# चैट हिस्ट्री लोड करना
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        if isinstance(message["content"], dict) and message["content"].get("type") == "link_button":
            st.write(message["content"]["text"])
            st.link_button(message["content"]["button_text"], message["content"]["url"])
        else:
            st.markdown(str(message["content"]))

# फोटो अपलोडर
st.markdown("<div class='voice-label'>📁 UPLOAD IMAGE (फाइल या फोटो से सवाल पूछें):</div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])
uploaded_image = None
if uploaded_file:
    uploaded_image = Image.open(uploaded_file)
    st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)

# वॉयस इनपुट सेक्शन
st.markdown("<div class='voice-label'>🎙️ VOICE COMMAND // INTERACT:</div>", unsafe_allow_html=True)
voice_input = speech_to_text(start_prompt="START RECORDING", stop_prompt="STOP RECORDING", language='hi', key='speech')
text_input = st.chat_input("ENTER COMMAND...")

prompt = voice_input if voice_input else text_input

if prompt:
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    clean_prompt = prompt.lower().replace(" ", "")
    url_to_open = None
    assistant_reply = ""
    button_text = ""

    if "youtube" in clean_prompt or "यूट्यूब" in clean_prompt:
        url_to_open = "https://www.youtube.com"
        assistant_reply = "हाँ भाई, यूट्यूब खोलने का लिंक तैयार है! नीचे दिए बटन पर क्लिक करो।"
        button_text = "🚀 OPEN YOUTUBE"
    elif "google" in clean_prompt or "गूगल" in clean_prompt:
        url_to_open = "https://www.google.com"
        assistant_reply = "लो भाई, गूगल बाबा का एक्सेस रेडी है।"
        button_text = "🔍 OPEN GOOGLE"
    elif "github" in clean_prompt or "गिटहब" in clean_prompt:
        url_to_open = "https://www.github.com"
        assistant_reply = "बिल्कुल अनुराग भाई, गिटहब ओपन करने के लिए तैयार हूँ।"
        button_text = "🐙 OPEN GITHUB"
    elif "instagram" in clean_prompt or "इंस्टाग्राम" in clean_prompt:
        url_to_open = "https://www.instagram.com"
        assistant_reply = "चलो भाई, इंस्टाग्राम का लिंक हाजिर है। रील्स देखो! 😉"
        button_text = "📸 OPEN INSTAGRAM"

    if url_to_open:
        with st.chat_message("assistant", avatar="🤖"):
            st.write(assistant_reply)
            st.link_button(button_text, url_to_open)
        st.session_state.messages.append({
            "role": "assistant", 
            "content": {"type": "link_button", "text": assistant_reply, "button_text": button_text, "url": url_to_open}
        })
        robot_speak(assistant_reply)
    else:
        with st.chat_message("assistant", avatar="🤖"):
            placeholder = st.empty()
            placeholder.markdown("`SEARCHING INTERNET & ANALYZING COMMAND...`")
            try:
                model = genai.GenerativeModel(
                    "gemini-1.5-flash", 
                    tools=[{"google_search": {}}],
                    system_instruction=(
                        "तुम्हारा नाम 'वीर' है। तुम कोई रोबोट या मशीन नहीं हो, बल्कि एक बेहद समझदार, कूल और दोस्ताना एआई असिस्टेंट हो जिसे सिर्फ और सिर्फ 'अनुराग' ने बनाया है। "
                        "तुम्हारी बात करने की भाषा एकदम नेचुरल, आम इंसानों जैसी और हिंदी-इंग्लिश मिक्स (Hinglish) होनी चाहिए। "
                        "अगर कोई आज का क्रिकेट मैच, मौसम, या नई खबर पूछे, तो तुरंत अपनी सर्च टूल का इस्तेमाल करके एकदम सटीक लाइव जानकारी दो। "
                        "बातचीत में कोई रोबोटिक औपचारिकता मत रखना, हमेशा एक पक्के दोस्त की तरह बात करो। छोटे और क्रिस्प जवाब दे ताकि सुनने में अच्छे लगें।"
                    )
                )
                
                input_data = [uploaded_image, prompt] if uploaded_image else [prompt]
                response = model.generate_content(input_data)
                full_response = response.text
                
                placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
                robot_speak(full_response)
                
            except Exception as e:
                placeholder.markdown(f"❌ एरर आया: {str(e)}")
