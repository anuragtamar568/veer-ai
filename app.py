import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
from PIL import Image

# PAGE CONFIG
st.set_page_config(
    page_title="VEER AI // PARALLEL WORLD",
    page_icon="🤖",
    layout="centered"
)

# SESSION STATE
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# DARK THEME
st.markdown("""
<style>
.stApp {
    background-color: #0e1117 !important;
}

h1 {
    color: #00d4ff !important;
    text-align: center;
    font-family: 'Courier New', monospace !important;
}

.stChatMessage {
    background-color: #1a1e26 !important;
    border: 1px solid #30363d !important;
    border-radius: 12px !important;
    color: white !important;
}

.stButton>button {
    background-color: #00d4ff !important;
    color: black !important;
    font-weight: bold;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# VOICE ENGINE
def speak_natural(text):
    clean_text = (
        text.replace('"', '')
        .replace("'", "")
        .replace("\n", " ")
    )

    js = f"""
    <script>
    window.speechSynthesis.cancel();
    var msg = new SpeechSynthesisUtterance('{clean_text}');
    msg.lang = 'hi-IN';
    window.speechSynthesis.speak(msg);
    </script>
    """

    components.html(js, height=0)

# GEMINI API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key नहीं मिली।")
    st.stop()

st.title("🤖 VEER PERSONAL AI")

# CLEAR CHAT
if st.button("🗑️ क्लियर चैट"):
    st.session_state.chat_history = []
    st.rerun()

# IMAGE INPUT MODE
active_image = None

input_mode = st.radio(
    "इमेज इनपुट मोड चुनें",
    ["📷 लाइव कैमरा", "🖼️ फोटो अपलोड"]
)

if input_mode == "📷 लाइव कैमरा":
    cam_shot = st.camera_input("कैमरा चालू करें:")

    if cam_shot:
        active_image = Image.open(cam_shot)

else:
    uploaded_image = st.file_uploader(
        "फोटो चुनें...",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_image:
        active_image = Image.open(uploaded_image)

# SHOW CHAT HISTORY
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

# USER INPUT
text_input = st.chat_input("अनुराग सर, आदेश दें...")

if text_input:

    st.session_state.chat_history.append(
        {"role": "user", "content": text_input}
    )

    with st.chat_message("user"):
        st.write(text_input)

    with st.chat_message("assistant"):

        with st.spinner("प्रोसेसिंग..."):

            try:
                model = genai.GenerativeModel("gemini-1.5-flash")

                sys_prompt = """
                तुम वीर हो, अनुराग सर के AI असिस्टेंट।
                हमेशा स्मार्ट और डार्क स्टाइल में हिंदी में जवाब दो।
                """

                if active_image:
                    response = model.generate_content(
                        [sys_prompt, active_image, text_input]
                    )
                else:
                    response = model.generate_content(
                        [sys_prompt, text_input]
                    )

                reply = response.text

                st.write(reply)

                st.session_state.chat_history.append(
                    {"role": "assistant", "content": reply}
                )

                speak_natural(reply)

            except Exception as e:
                st.error(f"Error: {e}")
