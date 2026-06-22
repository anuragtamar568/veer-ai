import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text
import streamlit.components.v1 as components
import time

# 1. पेज कॉन्फ़िगरेशन और हाई-विजिबिलिटी थीम
st.set_page_config(page_title="VEER AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(rgba(10, 15, 25, 0.95), rgba(10, 15, 25, 0.95)), 
                    url("https://images.unsplash.com/photo-1542831371-29b0f74f9713?q=80&w=1400&auto=format&fit=crop") !important; 
        background-size: cover !important; background-position: center !important; background-attachment: fixed !important;
    }
    h1 {color: #6bf2ff !important; font-weight: 300 !important; text-transform: uppercase; letter-spacing: 5px; text-shadow: 0 0 10px #6bf2ff;}
    .dev-text {color: #00ff66 !important; font-family: monospace; font-weight: bold; letter-spacing: 2px;}
    
    /* Text Visibility: Bright White */
    div[data-testid="stChatMessage"] {
        background-color: rgba(8, 20, 30, 0.95) !important; 
        border: 2px solid #00d2ff; 
        border-radius: 12px;
    }
    div[data-testid="stChatMessage"] p, div[data-testid="stChatMessage"] span, div[data-testid="stAppViewContainer"] p {
        color: #ffffff !important; 
        font-size: 16px !important;
        font-weight: 500 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("VEER AI 🤖")
st.markdown("<div class='dev-text'>⚡ REAL FRIEND WORKSTATION // 👤 CREATED BY ANURAG</div>", unsafe_allow_html=True)
st.write("---")

# 2. 100% वर्किंग नेचुरल वॉइस स्क्रिप्ट (बिना रुके बोलने के लिए)
def speak_natural(text):
    clean_text = text.replace('"', '').replace("'", "").replace("\n", " ")
    js = f"""<script>
        window.speechSynthesis.cancel(); // पुराना ऑडियो साफ करो
        var msg = new SpeechSynthesisUtterance('{clean_text}');
        msg.lang = 'hi-IN';
        msg.pitch = 1.1; // थिकनेस थोड़ी बढ़ा दी ताकि रोबोटिक न लगे
        msg.rate = 1.0;  // बोलने की स्पीड नॉर्मल दोस्त जैसी
        window.speechSynthesis.speak(msg);
    </script>"""
    components.html(js, height=0)

# 3. Session State Setup
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_processed" not in st.session_state:
    st.session_state.last_processed = None

# Clear Chat History
if st.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.session_state.last_processed = None
    if "chat" in st.session_state:
        del st.session_state["chat"]
    st.rerun()

# 4. API की चेकिंग
if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"].strip():
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("API KEY MISSING! Settings -> Secrets में जाकर GEMINI_API_KEY सेट करो।")
    st.stop()

# 5. Gemini Chat Setup (प्रॉपर अनुराग भाई वाला दोस्ती अंदाज़)
if "chat" not in st.session_state:
    try:
        model = genai.GenerativeModel(
            "gemini-2.0-flash",
            system_instruction=(
                "तुम 'वीर' (VEER AI) हो। तुम्हें तुम्हारे भाई और सबसे अच्छे दोस्त 'अनुराग' ने बनाया है। "
                "तुम कोई मशीन या रोबोट नहीं हो, तुम अनुराग के सच्चे लंगोटिया यार हो। "
                "हमेशा हर जवाब में 'अनुराग भाई' कहकर बात करो। बातचीत का अंदाज़ बिल्कुल देसी, दोस्ताना और "
                "मज़ेदार होना चाहिए (जैसे: 'अरे अनुराग भाई, उत्तर प्रदेश के सीएम तो अपने योगी आदित्यनाथ हैं!'). "
                "जवाब को बहुत लंबा और उबाऊ मत बनाना, सीधे और कड़क अंदाज़ में हिंदी में बात करो।"
            )
        )
        st.session_state.chat = model.start_chat(history=[])
    except Exception as e:
        st.error(f"Model Init Error: {e}")
        st.stop()

# 6. चैट हिस्ट्री रेंडर करना
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 7. इनपुट कॉम्पोनेंट्स
voice_prompt = speech_to_text(language='hi', use_container_width=True, key='mic')
user_input = st.chat_input("COMMAND...")

current_prompt = None

if voice_prompt and voice_prompt.strip():
    if st.session_state.last_processed != voice_prompt:
        current_prompt = voice_prompt
elif user_input and user_input.strip():
    current_prompt = user_input

# 8. मुख्य एक्जीक्यूशन लॉजिक
if current_prompt:
    st.session_state.last_processed = current_prompt
    st.session_state.messages.append({"role": "user", "content": current_prompt})
    
    with st.chat_message("user"):
        st.write(current_prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            with st.spinner("वीर सोच रहा है..."):
                response = st.session_state.chat.send_message(current_prompt)
            
            ans_text = response.text
            placeholder.write(ans_text)
            st.session_state.messages.append({"role": "assistant", "content": ans_text})
            
            # पहले ऑडियो ट्रिगर करो
            speak_natural(ans_text)
            
            # ऑडियो लोड होने के लिए 0.5 सेकंड का छोटा सा पॉज़, फिर स्क्रीन रिफ्रेश ताकि आवाज़ न कटे
            time.sleep(0.5)
            st.rerun()
            
        except Exception as e:
            placeholder.error(f"Error: {e}")
