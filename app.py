import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text

# 1. हैकर लुक के लिए Custom CSS (Matrix Theme)
def local_css():
    st.markdown("""
    <style>
    /* पूरे ऐप का बैकग्राउंड */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.8)), 
                    url("http://googleusercontent.com/image_collection/image_retrieval/14003150927431358877");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* टेक्स्ट का कलर और फॉन्ट (Hacker Green) */
    h1, h2, h3, p, span, div {
        color: #00FF41 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    
    /* चैट बॉक्स को पारदर्शी (Transparent) बनाना */
    div[data-testid="stChatMessage"] {
        background-color: rgba(0, 30, 0, 0.6) !important;
        border: 1px solid #00FF41;
        border-radius: 10px;
    }

    /* इनपुट बॉक्स स्टाइल */
    .stChatInputContainer {
        background-color: black !important;
        border: 2px solid #00FF41 !important;
    }

    /* माइक बटन का स्टाइल */
    button {
        background-color: #0d0208 !important;
        border: 1px solid #00FF41 !important;
        color: #00FF41 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="वीर: हैकर एआई", page_icon="🕵️", layout="centered")
local_css()

# हेडर (यहाँ आपका नाम हमेशा स्क्रीन पर चमकेगा)
st.title("🕵️ वीर: टर्मिनल एक्सेस")
st.write("`[STATUS: ONLINE]` | `[DEVELOPER: ANURAG]`")
st.write("---")

# API Configuration
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # चैट हिस्ट्री दिखाना
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # वॉइस इनपुट
    st.write("🎙️ **वॉयस कमांड भेजें:**")
    voice_input = speech_to_text(start_prompt="🎤 लिसनिंग...", stop_prompt="🛑 स्टॉप", language='hi', key='speech')

    text_input = st.chat_input("कमांड टाइप करें...")
    prompt = voice_input if voice_input else text_input

    if prompt:
        with st.chat_message("user"):
            st.markdown(f"> {prompt}")
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown("`प्रोसैसिंग...`")
            
            try:
                # यहाँ इंस्ट्रक्शन को और पक्का कर दिया है
                model = genai.GenerativeModel(
                    "gemini-2.5-flash",
                    system_instruction="तुम्हारा नाम 'वीर' है। तुम एक प्रोफेशनल हैकर एआई हो जिसे सिर्फ और सिर्फ 'अनुराग' ने बनाया है। जब भी कोई पूछे कि तुम्हें किसने बनाया या तुम कौन हो, तो हमेशा गर्व से बताना कि तुम्हारे क्रिएटर और बॉस अनुराग हैं। तुम्हारी भाषा थोड़ी टेक्निकल, सीक्रेट और कूल होनी चाहिए।"
                )
                response = model.generate_content(prompt)
                placeholder.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                placeholder.markdown(f"❌ सिस्टम फेलियर: {str(e)}")
else:
    st.error("API Key Not Found.")
