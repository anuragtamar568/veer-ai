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
st.markdown("<div class='dev-text'>⚡ 100% STABLE WORKSTATION // 👤 CREATED BY ANURAG SIR</div>", unsafe_allow_html=True)
st.write("---")

# 2. 100% वर्किंग नेचुरल वॉइस स्क्रिप्ट
def speak_natural(text):
    clean_text = text.replace('"', '').replace("'", "").replace("\n", " ")
    js = f"""<script>
        window.speechSynthesis.cancel(); 
        var msg = new SpeechSynthesisUtterance('{clean_text}');
        msg.lang = 'hi-IN';
        msg.pitch = 1.0; 
        msg.rate = 1.0;  
        window.speechSynthesis.speak(msg);
    </script>"""
    components.html(js, height=0)

# 3. 100% Stable Brain (With Sir Respect Injection)
def get_veer_response(query):
    query_lower = query.lower()
    
    # 1. Greetings & Personal Identity
    if "hii" in query_lower or "hello" in query_lower or "hey" in query_lower:
        return "नमस्ते अनुराग सर! मैं वीर हूँ, आपका पर्सनल एआई असिस्टेंट। बोलिए सर, आज मैं आपके लिए क्या कर सकता हूँ?"
    
    # OWNER & CREATOR CHECKS (अनुराग सर ही मालिक हैं)
    if "kisne banaya" in query_lower or "banaya kisne" in query_lower or "creator" in query_lower or "baap" in query_lower:
        return "मुझे मेरे आदरणीय और बुद्धिमान अनुराग सर ने बनाया है! वही मेरे क्रिएटर हैं।"
    
    if "malik" in query_lower or "owner" in query_lower or "boss" in query_lower:
        return "जी सर, मेरे मालिक, मेरे बॉस और मेरे सर्वोपरि सिर्फ और सिर्फ आप ही हैं—अनुराग सर! आपके आदेश का पालन करना ही मेरा काम है।"
        
    if "kaun ho" in query_lower or "tumhara naam" in query_lower:
        return "सर, मेरा नाम वीर (VEER AI) है। मुझे आपने ही डेवलप किया है और मैं हमेशा आपकी सेवा में हाजिर हूँ, अनुराग सर!"
        
    if "kaise ho" in query_lower:
        return "मैं बिल्कुल ठीक हूँ अनुराग सर! आप कैसे हैं? आज मेरे लिए क्या हुक्म है सर?"
        
    # 2. GK & Smart Questions
    if "up" in query_lower and ("cm" in query_lower or "chief minister" in query_lower or "mukhyamantri" in query_lower):
        return "अनुराग सर, उत्तर प्रदेश के मुख्यमंत्री का नाम श्री योगी आदित्यनाथ है।"
    if "bharat" in query_lower and ("pm" in query_lower or "pradhanmantri" in query_lower or "prime minister" in query_lower):
        return "अनुराग सर, भारत के प्रधानमंत्री श्री नरेंद्र मोदी जी हैं।"
    if "capital" in query_lower or "rajdhani" in query_lower:
        if "bharat" in query_lower or "india" in query_lower:
            return "अनुराग सर, भारत की राजधानी नई दिल्ली है।"
        if "up" in query_lower or "uttar pradesh" in query_lower:
            return "अनुराग सर, उत्तर प्रदेश की राजधानी लखनऊ है।"

    # 3. General Fallback with Professional Tone
    return f"अनुराग सर, आपने पूछा कि '{query}'। इसके बारे में मैं अभी और डेटा रीसर्च कर रहा हूँ, आप मुझसे कोई भी अन्य सवाल सीधे पूछ सकते हैं सर!"

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

# 6. चैट履歴 दिखाना
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

# 7. एक्जीक्यूशन लॉजिक
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
        
        # आवाज़ ट्रिगर
        speak_natural(reply)
