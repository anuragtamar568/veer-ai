import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# 1. पेज कॉन्फ़िगरेशन
st.set_page_config(page_title="VEER AI", page_icon="💻", layout="centered")

# 2. थीम (CSS)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {background: linear-gradient(rgba(10, 15, 25, 0.85), rgba(10, 15, 25, 0.85)), url("https://images.unsplash.com/photo-1542831371-29b0f74f9713?q=80&w=1400&auto=format&fit=crop") !important; background-size: cover !important; background-attachment: fixed !important;}
    h1 {color: #6bf2ff !important; text-transform: uppercase; letter-spacing: 5px;}
    .developer-text {color: #00ff66 !important; font-family: monospace; font-weight: bold;}
    div[data-testid="stChatMessage"] {background-color: rgba(8, 20, 30, 0.9) !important; border: 2px solid #00d2ff; border-radius: 12px;}
    </style>
""", unsafe_allow_html=True)

# 3. वॉइस फंक्शन
def play_audio(text):
    clean_text = text.replace('"', '').replace("'", "")
    js = f"""
    <script>
        var msg = new SpeechSynthesisUtterance('{clean_text}');
        msg.lang = 'hi-IN';
        window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js, height=0)

# 4. ऐप सेटअप
st.title("VEER AI")
st.markdown("<div class='developer-text'>SPECIALIST WORKSTATION</div>", unsafe_allow_html=True)

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# हिस्ट्री
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# इनपुट
if prompt := st.chat_input("COMMAND..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt)
            placeholder.write(response.text)
            play_audio(response.text) # वीर बोलेगा
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("API Error! Please check your Gemini Key.")
