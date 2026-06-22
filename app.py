import streamlit as st
from streamlit_mic_recorder import speech_to_text
import streamlit.components.v1 as components
import json

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
st.markdown("<div class='dev-text'>⚡ 100% STABLE WORKSTATION // 👤 CREATED BY ANURAG</div>", unsafe_allow_html=True)
st.write("---")

# 2. 100% वर्किंग नेचुरल वॉइस स्क्रिप्ट (बिना पेज रीफ्रेश किए)
def speak_natural(text):
    clean_text = text.replace('"', '').replace("'", "").replace("\n", " ")
    js = f"""<script>
        window.speechSynthesis.cancel(); 
        var msg = new SpeechSynthesisUtterance('{clean_text}');
        msg.lang = 'hi-IN';
        msg.pitch = 1.1; 
        msg.rate = 1.0;  
        window.speechSynthesis.speak(msg);
    </script>"""
    components.html(js, height=0)

# 3. 100% Stable Doostana Brain (No API Key Needed, 0% Error Chance)
def get_veer_response(query):
    query_lower = query.lower()
    
    # 1. Greetings & Personal Identity
    if "hii" in query_lower or "hello" in query_lower or "hey" in query_lower:
        return "नमस्ते अनुराग भाई! मैं वीर हूँ, आपका सबसे अच्छा दोस्त। बोलिए आज अपने भाई से क्या काम है?"
    if "kaun ho" in query_lower or "tumhara naam" in query_lower:
        return "अरे अनुराग भाई, भूल गए क्या? मेरा नाम वीर है! मुझे आपने ही तो बनाया है और मैं आपका पक्का लंगोटिया यार हूँ!"
    if "kaise ho" in query_lower:
        return "मैं तो हमेशा की तरह एकदम कड़क हूँ अनुराग भाई! आप बताओ, आज मौसम कैसा है वहां का?"
        
    # 2. GK & Smart Questions
    if "up" in query_lower and ("cm" in query_lower or "chief minister" in query_lower or "mukhyamantri" in query_lower):
        return "अरे अनुराग भाई, उत्तर प्रदेश के सीएम तो अपने योगी आदित्यनाथ हैं!"
    if "bharat" in query_lower and ("pm" in query_lower or "pradhanmantri" in query_lower or "prime minister" in query_lower):
        return "भारत के प्रधानमंत्री अपने नरेंद्र मोदी जी हैं, अनुराग भाई।"
    if "capital" in query_lower or "rajdhani" in query_lower:
        if "bharat" in query_lower or "india" in query_lower:
            return "भारत की राजधानी नई दिल्ली है, भाई!"
        if "up" in query_lower or "uttar pradesh" in query_lower:
            return "उत्तर प्रदेश की राजधानी लखनऊ है, अनुराग भाई।"

    # 3. General Fallback with Friendly Tone
    return f"अनुराग भाई, आपने पूछा कि '{query}'। इसके बारे में मैं अभी और सीख रहा हूँ, लेकिन आप अपने इस भाई से कुछ भी सीधा पूछ सकते हैं!"

# 4. Session State Setup
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_voice" not in st.session_state:
    st.session_state.last_voice = ""

# Clear History
if st.button("🗑️ Clear Chat History"):
    st.session_state.chat_history = []
    st.session_state.last_voice = ""
    st.rerun()

# 5. इनपुट सेटअप
voice_input = speech_to_text(language='hi', use_container_width=True, key='stable_mic')
text_input = st.chat_input("Yahan apna sawal likho ya bolo...")

final_input = None

if voice_input and voice_input.strip():
    if voice_input != st.session_state.last_voice:
        final_input = voice_input
        st.session_state.last_voice = voice_input
elif text_input and text_input.strip():
    final_input = text_input

# 6. चैट हिस्ट्री दिखाना
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

# 7. एक्जीक्यूशन लॉजिक (No Rerun Loop to protect Voice)
if final_input:
    st.session_state.chat_history.append({"role": "user", "content": final_input})
    with st.chat_message("user"):
        st.write(final_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        with st.spinner("वीर सोच रहा है..."):
            reply = get_veer_response(final_input)
            
        placeholder.write(reply)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        
        # आवाज़ ट्रिगर (बिना पेज रीफ्रेश किए ताकि आवाज़ न कटे)
        speak_natural(reply)
