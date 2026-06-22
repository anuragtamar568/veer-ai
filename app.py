import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text

# पेज कॉन्फ़िगरेशन
st.set_page_config(page_title="VEER AI", page_icon="💻", layout="centered")

# CSS - बैकग्राउंड, नियॉन टेक्स्ट और वॉयस रिकॉर्डर का फिक्स
def local_css():
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: transparent !important;
    }
    
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
        filter: brightness(0.35) contrast(1.1);
    }
    
    iframe[title="streamlit_mic_recorder.speech_to_text"] {
        background: transparent !important;
        background-color: transparent !important;
    }
    
    h1 {
        color: #6bf2ff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        font-weight: 300 !important;
        text-transform: uppercase;
        letter-spacing: 5px;
        text-shadow: 0 0 10px rgba(107, 242, 255, 0.8), 0 0 25px rgba(107, 242, 255, 0.5);
    }
    
    .developer-text {
        color: #00ff66 !important;
        font-family: 'Courier New', Courier, monospace !important;
        font-weight: bold;
        letter-spacing: 2px;
        font-size: 14px;
        text-shadow: 0 0 8px rgba(0, 255, 102, 0.6);
    }

    div[data-testid="stChatMessage"] {
        background-color: rgba(8, 20, 30, 0.85) !important;
        border: 2px solid #00d2ff;
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.4);
    }

    p, span, div, label {
        color: #ffffff !important;
    }
    
    .stChatInputContainer {
        background-color: rgba(5, 10, 15, 0.95) !important;
        border: 2px solid #00d2ff !important;
        border-radius: 8px !important;
    }
    
    .stChatInputContainer textarea {
        color: #ffffff !important;
    }

    button {
        background-color: #050a10 !important;
        border: 1px solid #00d2ff !important;
        color: #00d2ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# बैकग्राउंड इमेज
st.markdown(
    '<div class="bg-img-container"><img src="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1400&auto=format&fit=crop"></div>',
    unsafe_allow_html=True
)

# हेडर
st.title("VEER AI")
st.markdown("<div class='developer-text'>SPECIALIST WORKSTATION</div>", unsafe_allow_html=True)
st.markdown("<div class='developer-text'>DEVELOPER: ANURAG // SECURE CONNECTION</div>", unsafe_allow_html=True)
st.write("---")

# JavaScript से नई टैब खोलने का फंक्शन
def open_website(url):
    js = f"window.open('{url}', '_blank');"
    st.components.v1.html(f"<script>{js}</script>", height=0, width=0)

# API Configuration
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # वॉयस इनपुट
    st.markdown("<div style='font-family: monospace; font-weight: bold;'>🎙️ VOICE COMMAND // INTERACT:</div>", unsafe_allow_html=True)
    voice_input = speech_to_text(start_prompt="START RECORDING", stop_prompt="STOP RECORDING", language='hi', key='speech')

    text_input = st.chat_input("ENTER COMMAND...")
    prompt = voice_input if voice_input else text_input

    if prompt:
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # --- असिस्टेंट फीचर: कमांड चेक करना ---
        clean_prompt = prompt.lower()
        url_to_open = None
        assistant_reply = ""

        if "youtube" in clean_prompt or "यूट्यूब" in clean_prompt:
            url_to_open = "https://www.youtube.com"
            assistant_reply = "जी बॉस, आपके लिए यूट्यूब ओपन कर रहा हूँ।"
        elif "google" in clean_prompt or "गूगल" in clean_prompt:
            url_to_open = "https://www.google.com"
            assistant_reply = "कमांड एक्जीक्यूटेड! गूगल सर्च इंजन ओपन किया जा रहा है।"
        elif "github" in clean_prompt or "गिटहब" in clean_prompt:
            url_to_open = "https://www.github.com"
            assistant_reply = "बिल्कुल अनुराग, आपकी गिटहब रिपोजिटरी एक्सेस की जा रही है।"
        elif "facebook" in clean_prompt or "फेसबुक" in clean_prompt:
            url_to_open = "https://www.facebook.com"
            assistant_reply = "फेसबुक पोर्टल खोला जा रहा है, बॉस।"
        
        # अगर कोई मैचिंग कमांड मिली, तो सीधे एक्शन लें
        if url_to_open:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(assistant_reply)
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
            open_website(url_to_open)
        else:
            # अगर नॉर्मल बात है, तो Gemini AI से जवाब लें
            with st.chat_message("assistant", avatar="🤖"):
                placeholder = st.empty()
                placeholder.markdown("`ANALYZING COMMAND...`")
                
                try:
                    model = genai.GenerativeModel(
                        "gemini-2.5-flash",
                        system_instruction=(
                            "तुम्हारा नाम 'वीर' है। तुम एक अत्यंत उन्नत और सुरक्षित हैकर एआई असिस्टेंट हो जिसे सिर्फ 'अनुराग' ने विकसित किया है। "
                            "तुम अनुराग के प्रति पूरी तरह वفاदार हो। तुम्हारी भाषा टेक्निकल, सीक्रेट और कूल होनी चाहिए। "
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
