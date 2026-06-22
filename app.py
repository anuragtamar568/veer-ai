import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text

# पेज कॉन्फ़िगरेशन (यह सबसे ऊपर होना चाहिए)
st.set_page_config(page_title="VEER AI", page_icon="💻", layout="centered")

# 1. बैकग्राउंड को फुल स्क्रीन इमेज बनाने और टेक्स्ट लेटर्स को डिज़ाइनर लुक देने के लिए CSS
def local_css():
    st.markdown("""
    <style>
    /* पूरे ऐप के बैकग्राउंड को इमेज के ऊपर सेट करना */
    [data-testid="stAppViewContainer"] {
        background-color: transparent !important;
    }
    
    /* बैकग्राउंड इमेज को फिक्स और फुल-स्क्रीन करने के लिए */
    .bg-img-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        overflow: hidden;
    }
    .bg-img-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        filter: brightness(0.4) contrast(1.1); /* इमेज को थोड़ा डार्क किया ताकि टेक्स्ट चमके */
    }
    
    /* VEER AI - डिज़ाइनर नियॉन टेक्स्ट लेटर्स */
    h1 {
        color: #6bf2ff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        font-weight: 300 !important;
        text-transform: uppercase;
        letter-spacing: 5px;
        text-shadow: 0 0 10px rgba(107, 242, 255, 0.8), 0 0 25px rgba(107, 242, 255, 0.5);
        margin-bottom: 5px !important;
    }
    
    /* सब-हेडिंग्स (Specialist Workstation) स्टाइल */
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

    /* चैट बॉक्स को पारदर्शी और नियॉन बॉर्डर वाला बनाना */
    div[data-testid="stChatMessage"] {
        background-color: rgba(8, 20, 30, 0.8) !important;
        border: 2px solid #00d2ff;
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.4);
        margin-bottom: 15px;
        padding: 15px !important;
    }

    /* नॉर्मल टेक्स्ट का कलर */
    p, span, div, label {
        color: #ffffff !important;
        font-family: 'Segoe UI', sans-serif !important;
    }
    
    /* चैट इनपुट कंटेनर स्टाइल */
    .stChatInputContainer {
        background-color: rgba(5, 10, 15, 0.95) !important;
        border: 2px solid #00d2ff !important;
        border-radius: 8px !important;
    }
    
    .stChatInputContainer textarea {
        color: #ffffff !important;
    }

    /* वॉयस कमांड टेक्स्ट */
    .voice-label {
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold;
        margin-top: 15px;
    }

    /* माइक बटन का हैकर स्टाइल */
    button {
        background-color: #050a10 !important;
        border: 1px solid #00d2ff !important;
        color: #00d2ff !important;
        border-radius: 4px !important;
    }
    
    button:hover {
        background-color: #00d2ff !important;
        color: black !important;
        box-shadow: 0 0 10px #00d2ff;
    }

    /* स्क्रॉलबार छिपाना */
    ::-webkit-scrollbar {
        width: 0px;
        background: transparent;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# HTML और st.image के कॉम्बिनेशन से बैकग्राउंड में 3D साइबर लैपटॉप इन्जेक्ट करना
st.markdown(
    f'<div class="bg-img-container"><img src="http://googleusercontent.com/image_generation_content/259"></div>',
    unsafe_allow_html=True
)

# हेडर (बिल्कुल डिज़ाइनर लेआउट)
st.title("VEER AI")
st.markdown("<div class='developer-text'>SPECIALIST WORKSTATION</div>", unsafe_allow_html=True)
st.markdown("<div class='developer-text'>DEVELOPER: ANURAG // SECURE CONNECTION</div>", unsafe_allow_html=True)
st.write("---")

# API Configuration
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # चैट हिस्ट्री स्क्रीन पर लोड करना
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # वॉयस इनपुट सेक्शन
    st.markdown("<div class='voice-label'>🎙️ VOICE COMMAND // INTERACT:</div>", unsafe_allow_html=True)
    voice_input = speech_to_text(
        start_prompt="START RECORDING",
        stop_prompt="STOP RECORDING",
        language='hi',
        key='speech'
    )

    text_input = st.chat_input("ENTER COMMAND...")
    prompt = voice_input if voice_input else text_input

    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown("`ANALYZING COMMAND...`")
            
            try:
                model = genai.GenerativeModel(
                    "gemini-2.5-flash",
                    system_instruction=(
                        "तुम्हारा नाम 'वीर' है। तुम एक अत्यंत उन्नत और सुरक्षित हैकर एआई हो जिसे सिर्फ 'अनुराग' ने विकसित किया है। "
                        "तुम अनुराग के प्रति पूरी तरह वफादार हो। तुम्हारी भाषा टेक्निकल, सीक्रेट, कूल और थोड़ी रहस्यमयी होनी चाहिए। "
                        "जब भी कोई पूछे, हमेशा गर्व से बताना कि तुम्हारे क्रिएटर और बॉस अनुराग हैं।"
                    )
                )
                response = model.generate_content(prompt)
                
                placeholder.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
            except Exception as e:
                placeholder.markdown(f"❌ `SYSTEM ERROR: {str(e)}`")

else:
    st.error("⚠️ CRITICAL: GEMINI_API_KEY NOT FOUND.")
