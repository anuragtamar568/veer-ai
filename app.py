import streamlit as st

# ================= PAGE CONFIG ================= #

st.set_page_config(
    page_title="VEER AI // CYBER CORE",
    page_icon="💻",
    layout="wide"
)

# ================= HACKER CSS ================= #

st.markdown("""
<style>

/* Main Background */

.stApp{
    background:
    radial-gradient(circle at top,#012401,#000000 70%);
}

/* Hide Streamlit Header */

header{
    visibility:hidden;
}

/* Neon Title */

.cyber-title{

    text-align:center;
    font-size:70px;
    font-weight:900;

    color:#00ff41;

    text-shadow:
    0 0 10px #00ff41,
    0 0 20px #00ff41,
    0 0 40px #00ff41,
    0 0 80px #00ff41;

    border-right:4px solid #00ff41;

    overflow:hidden;
    white-space:nowrap;

    animation: blink .8s infinite;
}

@keyframes blink{
    50%{
        border-color:transparent;
    }
}

/* Sidebar */

[data-testid="stSidebar"]{
    background:#020202;
    border-right:2px solid #00ff41;
}

[data-testid="stSidebar"] *{
    color:#00ff41 !important;
}

/* Cards */

.cyber-card{

    background:rgba(0,255,65,.05);

    border:1px solid #00ff41;

    border-radius:20px;

    padding:20px;

    margin-bottom:20px;

    box-shadow:
    0 0 10px #00ff41,
    inset 0 0 15px rgba(0,255,65,.2);

    backdrop-filter: blur(15px);
}

/* Chat */

.stChatMessage{

    background:rgba(0,255,65,.05);

    border:1px solid #00ff41;

    border-radius:20px;

    box-shadow:
    0 0 10px #00ff41,
    inset 0 0 15px rgba(0,255,65,.2);
}

/* Buttons */

.stButton button{

    width:100%;

    background:black;

    color:#00ff41;

    border:1px solid #00ff41;

    border-radius:12px;

    font-weight:bold;

    box-shadow:0 0 10px #00ff41;
}

.stButton button:hover{

    background:#00ff41;

    color:black;

    box-shadow:
    0 0 20px #00ff41,
    0 0 40px #00ff41;
}

/* Metrics */

[data-testid="metric-container"]{

    background:rgba(0,255,65,.05);

    border:1px solid #00ff41;

    border-radius:15px;

    box-shadow:0 0 10px #00ff41;
}

/* Input */

[data-testid="stChatInput"]{

    border:1px solid #00ff41;

    border-radius:15px;

    box-shadow:0 0 15px #00ff41;
}

/* Text */

p,span,div,label,h1,h2,h3,h4{
    color:#00ff41 !important;
    font-family:Consolas, monospace !important;
}

</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR ================= #

with st.sidebar:

    st.markdown("# ⚡ VEER AI")

    st.success("🟢 SYSTEM ONLINE")

    st.markdown("""
    <div class="cyber-card">

    <h3>👤 facehi</h3>

    </div>

    <div class="cyber-card">

    <h3>🤖 smart_bot</h3>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    mode = st.selectbox(
        "🧠 AI MODE",
        [
            "VEER",
            "JARVIS",
            "TEACHER",
            "CODER"
        ]
    )

    st.toggle("🔊 VOICE REPLY", True)

    st.markdown("---")

    st.button("🗑 NEW CHAT")
    st.button("📥 DOWNLOAD CHAT")

# ================= TITLE ================= #

st.markdown("""
<h1 class='cyber-title'>
⚡ VEER AI // CYBER CORE ⚡
</h1>
""", unsafe_allow_html=True)

# ================= SYSTEM CARD ================= #

st.markdown("""
<div class='cyber-card'>

<h2>🟢 SYSTEM STATUS : ONLINE</h2>

<h3>👤 USER : ANURAG SIR</h3>

<h3>🧠 AI ENGINE : GEMINI</h3>

<h3>🛡 SECURITY : ACTIVE</h3>

<h3>⚡ MODE : CYBER INTELLIGENCE</h3>

</div>
""", unsafe_allow_html=True)

# ================= DASHBOARD ================= #

st.markdown("## 📊 SYSTEM DASHBOARD")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("💬 CHATS", "12")

with c2:
    st.metric("🧠 MODE", mode)

with c3:
    st.metric("🔊 VOICE", "ON")

with c4:
    st.metric("⚡ STATUS", "ONLINE")

# ================= FEATURE CARDS ================= #

a, b, c = st.columns(3)

with a:
    st.markdown("""
    <div class='cyber-card'>
    <h3>💻 CODING CORE</h3>
    <p>Advanced coding assistance.</p>
    </div>
    """, unsafe_allow_html=True)

with b:
    st.markdown("""
    <div class='cyber-card'>
    <h3>🌐 RESEARCH CORE</h3>
    <p>Internet knowledge & analysis.</p>
    </div>
    """, unsafe_allow_html=True)

with c:
    st.markdown("""
    <div class='cyber-card'>
    <h3>🔐 SECURITY CORE</h3>
    <p>Cyber intelligence module.</p>
    </div>
    """, unsafe_allow_html=True)

# ================= CHAT ================= #

st.markdown("## 💬 CYBER CHAT")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input(">>> ENTER COMMAND")

if prompt:

    st.session_state.messages.append({
        "role":"user",
        "content":prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    reply = f"⚡ Command Received: {prompt}"

    with st.chat_message("assistant"):
        st.write(reply)

    st.session_state.messages.append({
        "role":"assistant",
        "content":reply
    })
