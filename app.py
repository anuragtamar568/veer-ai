import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# ================= PAGE =================

st.set_page_config(
    page_title="VEER AI Enterprise",
    page_icon="🤖",
    layout="wide"
)

# ================= GEMINI =================

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")

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
    animation:gradient 15s ease infinite;
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
font-size:75px;
font-weight:900;
color:white;

text-shadow:
0 0 10px cyan,
0 0 20px cyan,
0 0 40px cyan,
0 0 80px cyan;
}

.glass{
background:rgba(255,255,255,.08);
backdrop-filter:blur(20px);
border:1px solid rgba(255,255,255,.2);
border-radius:25px;
padding:25px;
box-shadow:0 0 20px rgba(255,255,255,.2);
}

.stChatMessage{
background:rgba(255,255,255,.08);
backdrop-filter:blur(20px);
border-radius:25px;
border:1px solid rgba(255,255,255,.15);
}

[data-testid="stSidebar"]{
background:rgba(0,0,0,.35);
backdrop-filter:blur(25px);
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
}

p,span,div,label,h1,h2,h3{
color:white !important;
}

</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================

with st.sidebar:

    st.markdown("# 🤖 VEER AI")

    st.success("🟢 System Online")

    mode = st.selectbox(
        "🧠 AI Mode",
        [
            "VEER",
            "Jarvis",
            "Teacher",
            "Coder"
        ]
    )

    st.session_state.voice = st.toggle(
        "🔊 Voice Reply",
        value=st.session_state.voice
    )

    st.markdown("---")

    st.markdown("""
    ### 🚀 Features

    💬 Smart Chat  
    🧠 AI Personalities  
    🔊 Voice Assistant  
    📥 Chat Download  
    ⚡ Enterprise Ready  
    """)

    if st.button("🗑️ New Chat"):
        st.session_state.messages = []
        st.rerun()

    chat_text = ""

    for m in st.session_state.messages:
        chat_text += f"{m['role']} : {m['content']}\n\n"

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
"""
<div class='glass'>
<h2>🚀 Welcome Anurag Sir</h2>

VEER AI is ready to assist you with:

✔ Coding Assistance  
✔ Business Research  
✔ Education & Learning  
✔ Automation Ideas  
✔ General Knowledge  

</div>
""",
unsafe_allow_html=True
)

# ================= DASHBOARD =================

st.markdown("## 📊 Dashboard")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("💬 Messages", len(st.session_state.messages))

with c2:
    st.metric("🧠 Mode", mode)

with c3:
    st.metric(
        "🔊 Voice",
        "ON" if st.session_state.voice else "OFF"
    )

with c4:
    st.metric("⚡ Status", "ONLINE")

st.markdown("---")

# ================= QUICK CARDS =================

a, b, c = st.columns(3)

with a:
    st.info("💻 Coding Expert")

with b:
    st.info("📚 Learning Assistant")

with c:
    st.info("🌐 Research Assistant")

# ================= SPEAK =================

def speak(text):

    if not st.session_state.voice:
        return

    text = text.replace("'", "")
    text = text.replace('"', "")
    text = text.replace("\n", " ")

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
    "अनुराग सर, कुछ पूछिए..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # PERSONALITY

    if mode == "Jarvis":

        personality = """
        You are JARVIS.
        Speak in futuristic style.
        Always call user Anurag Sir.
        """

    elif mode == "Teacher":

        personality = """
        You are an expert teacher.
        Explain things simply.
        Always call user Anurag Sir.
        """

    elif mode == "Coder":

        personality = """
        You are a senior software engineer.
        Help with programming professionally.
        Always call user Anurag Sir.
        """

    else:

        personality = """
        You are VEER AI.

        User name is Anurag Sir.

        Always call user Anurag Sir.

        Always answer in Hindi.

        If user asks:
        "Who created you?"

        Reply:
        "अनुराग सर, मुझे आपने बनाया है।"
        """

    with st.chat_message("assistant"):

        with st.spinner("⚡ VEER सोच रहा है..."):

            try:

                response = model.generate_content(
                    f"{personality}\n\nUser:{prompt}"
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
