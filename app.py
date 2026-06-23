import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="VEER AI",
    page_icon="🤖",
    layout="wide"
)

# ================= GEMINI =================

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-2.5-flash")
except Exception as e:
    st.error(f"Gemini Error: {e}")
    st.stop()

# ================= SESSION =================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "voice" not in st.session_state:
    st.session_state.voice = True

# ================= CSS =================

st.markdown("""
<style>

.stApp{
background: linear-gradient(-45deg,
#ff0080,#7928ca,#007cf0,#00dfd8,#ff4d4d);
background-size:400% 400%;
animation: gradient 15s ease infinite;
}

@keyframes gradient{
0%{background-position:0% 50%;}
50%{background-position:100% 50%;}
100%{background-position:0% 50%;}
}

header{
visibility:hidden;
}

.main-title{
text-align:center;
font-size:70px;
font-weight:900;
color:white;

text-shadow:
0 0 10px #00ffff,
0 0 20px #00ffff,
0 0 40px #00ffff,
0 0 80px #00ffff;
}

.subtitle{
text-align:center;
font-size:20px;
color:white;
text-shadow:0 0 10px white;
}

.stChatMessage{
background:rgba(255,255,255,.10);
backdrop-filter: blur(20px);
border:1px solid rgba(255,255,255,.2);
border-radius:25px;
padding:15px;
box-shadow:0 0 20px rgba(255,255,255,.2);
}

[data-testid="stSidebar"]{
background:rgba(0,0,0,.30);
backdrop-filter:blur(20px);
}

[data-testid="stSidebar"] *{
color:white !important;
}

.stButton button{
width:100%;
border:none;
border-radius:15px;
font-weight:bold;
color:white;
background:linear-gradient(90deg,#00ffff,#ff00ff);
box-shadow:0 0 15px cyan;
}

.stButton button:hover{
transform:scale(1.02);
transition:.3s;
}

p,span,div,label{
color:white !important;
}

</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================

with st.sidebar:

    st.title("🤖 VEER AI")

    mode = st.selectbox(
        "🧠 AI Mode",
        ["VEER", "Jarvis", "Teacher", "Coder"]
    )

    st.session_state.voice = st.toggle(
        "🔊 Voice Reply",
        value=st.session_state.voice
    )

    if st.button("🗑️ New Chat"):
        st.session_state.messages = []
        st.rerun()

    # Download Chat
    chat_text = ""

    for msg in st.session_state.messages:
        chat_text += f"{msg['role']}: {msg['content']}\n\n"

    st.download_button(
        "📥 Download Chat",
        chat_text,
        "veer_chat.txt"
    )

# ================= TITLE =================

st.markdown(
    "<h1 class='main-title'>🤖 VEER AI</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='subtitle'>Next Generation Enterprise Assistant</p>",
    unsafe_allow_html=True
)

# ================= VOICE =================

def speak(text):

    if not st.session_state.voice:
        return

    text = text.replace("\n", " ")
    text = text.replace("'", "")
    text = text.replace('"', "")

    js = f"""
    <script>
    window.speechSynthesis.cancel();

    let msg = new SpeechSynthesisUtterance(`{text}`);
    msg.lang='hi-IN';
    msg.rate=1;
    msg.pitch=1;

    window.speechSynthesis.speak(msg);
    </script>
    """

    components.html(js, height=0)

# ================= HISTORY =================

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================= CHAT =================

prompt = st.chat_input("अनुराग सर, कुछ पूछिए...")

if prompt:

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Personality

    if mode == "Jarvis":
        personality = """
        तुम JARVIS हो।
        futuristic style में जवाब दो।
        हमेशा User को 'अनुराग सर' कहो।
        """

    elif mode == "Teacher":
        personality = """
        तुम expert teacher हो।
        हर चीज सरल भाषा में समझाओ।
        हमेशा User को 'अनुराग सर' कहो।
        """

    elif mode == "Coder":
        personality = """
        तुम senior software engineer हो।
        coding answers professional दो।
        हमेशा User को 'अनुराग सर' कहो।
        """

    else:
        personality = """
        तुम VEER AI हो।

        नियम:
        - User का नाम अनुराग सर है।
        - हमेशा User को 'अनुराग सर' कहकर संबोधित करो।
        - हमेशा हिंदी में उत्तर दो।
        - अगर पूछा जाए 'तुम्हें किसने बनाया?'
          तो जवाब दो:
          'अनुराग सर, मुझे आपने बनाया और विकसित किया है।'
        """

    with st.chat_message("assistant"):

        with st.spinner("⚡ VEER सोच रहा है..."):

            try:

                response = model.generate_content(
                    f"{personality}\n\nUser: {prompt}"
                )

                reply = response.text

            except Exception as e:
                reply = f"❌ Error: {e}"

            st.markdown(reply)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": reply
                }
            )

            speak(reply)
