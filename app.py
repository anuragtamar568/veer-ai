import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="VEER AI CYBER CORE",
    page_icon="💻",
    layout="wide"
)

# ================= GEMINI =================

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

    # अगर यह model काम न करे तो अपना working model डालें
    model = genai.GenerativeModel("gemini-2.5-flash")

except Exception as e:
    st.error(f"Gemini Error: {e}")
    st.stop()

# ================= SESSION =================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "voice" not in st.session_state:
    st.session_state.voice = True

# ================= HACKER CSS =================

st.markdown("""
<style>

.stApp{
    background:
    radial-gradient(circle at top,#002200,#000000 60%);
}

/* Hide Header */
header{visibility:hidden;}

/* Main Title */

.hacker-title{

    text-align:center;
    font-size:70px;
    font-weight:900;

    color:#00ff41;

    text-shadow:
    0 0 10px #00ff41,
    0 0 20px #00ff41,
    0 0 40px #00ff41,
    0 0 80px #00ff41;

    overflow:hidden;
    white-space:nowrap;

    border-right:4px solid #00ff41;

    width:100%;

    animation: blink .7s infinite;
}

@keyframes blink{
50%{
border-color:transparent;
}
}

/* Sidebar */

[data-testid="stSidebar"]{

    background:#010101;

    border-right:2px solid #00ff41;
}

[data-testid="stSidebar"] *{
    color:#00ff41 !important;
}

/* Chat */

.stChatMessage{

    background:rgba(0,255,65,.05);

    border:1px solid #00ff41;

    border-radius:20px;

    box-shadow:
    0 0 10px #00ff41,
    inset 0 0 15px rgba(0,255,65,.2);

    color:#00ff41;
}

/* Input */

[data-testid="stChatInput"]{

    border:1px solid #00ff41;

    border-radius:15px;

    box-shadow:0 0 20px #00ff41;
}

/* Buttons */

.stButton button{

    width:100%;

    background:black;

    color:#00ff41;

    border:1px solid #00ff41;

    border-radius:15px;

    box-shadow:0 0 10px #00ff41;

    font-weight:bold;
}

.stButton button:hover{

    background:#00ff41;

    color:black;

    box-shadow:
    0 0 20px #00ff41,
    0 0 40px #00ff41;
}

/* Metric Cards */

[data-testid="metric-container"]{

    background:rgba(0,0,0,.5);

    border:1px solid #00ff41;

    padding:15px;

    border-radius:15px;

    box-shadow:0 0 10px #00ff41;
}

/* Text */

p,span,div,label,h1,h2,h3{
    color:#00ff41 !important;
    font-family:Consolas, monospace !important;
}

/* Glass */

.glass{

    background:rgba(0,255,65,.04);

    border:1px solid #00ff41;

    border-radius:20px;

    padding:25px;

    box-shadow:0 0 20px rgba(0,255,65,.3);
}

</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================

with st.sidebar:

    st.markdown("# 💻 VEER AI")

    st.success("🟢 SYSTEM ONLINE")

    mode = st.selectbox(
        "🧠 AI MODE",
        [
            "VEER",
            "JARVIS",
            "TEACHER",
            "CODER"
        ]
    )

    st.session_state.voice = st.toggle(
        "🔊 VOICE REPLY",
        value=st.session_state.voice
    )

    st.markdown("---")

    st.markdown("""
    ### ⚡ MODULES

    🤖 Smart Chat

    💻 Coding

    📚 Learning

    🌐 Research

    🔐 Cyber Security
    """)

    if st.button("🗑 NEW CHAT"):
        st.session_state.messages = []
        st.rerun()

    chat_text = ""

    for m in st.session_state.messages:
        chat_text += f"{m['role']} : {m['content']}\n\n"

    st.download_button(
        "📥 DOWNLOAD CHAT",
        chat_text,
        "veer_chat.txt"
    )

# ================= TITLE =================

st.markdown("""
<h1 class='hacker-title'>
⚡ VEER AI // CYBER CORE ⚡
</h1>
""", unsafe_allow_html=True)

# ================= DASHBOARD =================

st.markdown("""
<div class='glass'>

## 🟢 SYSTEM STATUS : ONLINE

👤 USER : ANURAG SIR

🧠 AI ENGINE : GEMINI

🛡 SECURITY : ACTIVE

⚡ MODE : CYBER INTELLIGENCE

</div>
""", unsafe_allow_html=True)

st.markdown("### 📊 SYSTEM DASHBOARD")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("💬 CHATS", len(st.session_state.messages))

with c2:
    st.metric("🧠 MODE", mode)

with c3:
    st.metric(
        "🔊 VOICE",
        "ON" if st.session_state.voice else "OFF"
    )

with c4:
    st.metric("⚡ STATUS", "ONLINE")

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

    window.speechSynthesis.speak(msg);

    </script>
    """

    components.html(js, height=0)

# ================= HISTORY =================

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================= CHAT =================

prompt = st.chat_input(
    ">>> ENTER COMMAND..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    if mode == "JARVIS":

        personality = """
        You are JARVIS.
        Talk in futuristic style.
        Always call user Anurag Sir.
        """

    elif mode == "TEACHER":

        personality = """
        You are an expert teacher.
        Explain simply.
        Always call user Anurag Sir.
        """

    elif mode == "CODER":

        personality = """
        You are a senior software engineer.
        Give professional coding answers.
        Always call user Anurag Sir.
        """

    else:

        personality = """
        You are VEER AI.

        User name is Anurag Sir.

        Always call user Anurag Sir.

        Always answer in Hindi.

        If asked who created you,
        answer:

        "अनुराग सर, मुझे आपने बनाया है।"
        """

    with st.chat_message("assistant"):

        with st.spinner("⚡ ACCESSING CYBER CORE..."):

            try:

                response = model.generate_content(
                    f"{personality}\n\nUser:{prompt}"
                )

                reply = response.text

            except Exception as e:

                if "429" in str(e):
                    reply = """
🚫 API LIMIT EXCEEDED

Free Gemini quota खत्म हो गई है।

कृपया थोड़ी देर बाद पुनः प्रयास करें।
"""
                else:
                    reply = f"❌ ERROR : {e}"

            st.markdown(reply)

            st.session_state.messages.append(
                {
                    "role":"assistant",
                    "content":reply
                }
            )

            speak(reply)
