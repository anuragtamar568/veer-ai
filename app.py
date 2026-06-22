import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text
import streamlit.components.v1 as components

st.set_page_config(page_title="VEER AI", page_icon="💻", layout="centered")

def local_css():
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] {background: linear-gradient(rgba(10, 15, 25, 0.85), rgba(10, 15, 25, 0.85)), url("https://images.unsplash.com/photo-1542831371-29b0f74f9713?q=80&w=1400&auto=format&fit=crop") !important; background-size: cover !important; background-position: center !important; background-attachment: fixed !important;}
        h1 {color: #6bf2ff !important; font-family: 'Segoe UI', sans-serif !important; text-transform: uppercase; letter-spacing: 5px; text-shadow: 0 0 10px #6bf2ff;}
        .developer-text {color: #00ff66 !important; font-family: monospace; font-weight: bold; font-size: 14px;}
        div[data-testid="stChatMessage"] {background-color: rgba(8, 20, 30, 0.9) !important; border: 2px solid #00d2ff; border-radius: 12px;}
        div.stLinkButton > a {background-color: #050a10 !important; color: #00ff66 !important; border: 2px solid #00ff66 !important; border-radius: 6px !important;}
        </style>
    """, unsafe_allow_html=True)
local_css()

# बोलकर सुनाने वाला फंक्शन (Browser Speech API)
def play_audio(text):
    text = text.replace('"', '').replace("'", "")
    js = f"""
    <script>
        var msg = new SpeechSynthesisUtterance('{text}');
        msg.lang = 'hi-IN';
        msg.rate = 1.0;
        window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js, height=0)

st.title("VEER AI")
st.markdown("<div class='developer-text'>SPECIALIST WORKSTATION // ANURAG</div>", unsafe_allow_html=True)
st.write("---")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

prompt = st.chat_input("COMMAND...")

if prompt:
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()
        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt)
            placeholder.write(response.text)
            
            # ऑटो-प्ले करने की कोशिश (ब्राउज़र परमिशन के लिए)
            play_audio(response.text)
            
            # मैन्युअल लिसन बटन (अगर ऑटो-प्ले ब्लॉक हो जाए)
            if st.button("🔊 LISTEN AGAIN"):
                play_audio(response.text)
                
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Error!")
