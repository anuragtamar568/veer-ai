import streamlit as st
import google.generativeai as genai

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="VEER AI X",
    page_icon="⚡",
    layout="wide"
)

# =========================
# THEME
# =========================

st.markdown("""
<style>

.stApp{
    background:
    radial-gradient(circle at top left,#0f0f0f,#050505,#000000);
}

/* Sidebar */

section[data-testid="stSidebar"]{
    background:#050505;
    border-right:1px solid #00ff88;
}

/* Title */

.glow-title{
    text-align:center;
    font-size:60px;
    font-weight:bold;
    color:#00ff88;

    text-shadow:
        0 0 5px #00ff88,
        0 0 10px #00ff88,
        0 0 20px #00ff88,
        0 0 40px #00ff88;

    animation:glow 2s infinite alternate;
}

@keyframes glow{
    from{
        text-shadow:
            0 0 10px #00ff88,
            0 0 20px #00ff88;
    }

    to{
        text-shadow:
            0 0 20px #00ff88,
            0 0 40px #00ff88,
            0 0 80px #00ff88;
    }
}

/* Shining Text */

.shine{
    background:linear-gradient(
        90deg,
        #00ff88,
        #ffffff,
        #00ff88
    );

    background-size:200% auto;
    color:transparent;
    -webkit-background-clip:text;

    animation:shine 3s linear infinite;
}

@keyframes shine{
    to{
        background-position:200% center;
    }
}

/* Chat */

[data-testid="stChatMessage"]{
    background:#0d1117;
    border:1px solid #00ff88;
    border-radius:15px;
    padding:10px;
    box-shadow:
        0 0 15px rgba(0,255,136,.2);
}

/* Input */

.stChatInputContainer{
    border:2px solid #00ff88;
    border-radius:15px;
    box-shadow:
        0 0 20px rgba(0,255,136,.4);
}

/* Button */

.stButton button{
    background:#00ff88 !important;
    color:black !important;
    font-weight:bold !important;
    border:none !important;
}

/* Text */

p,span,div{
    color:#e5ffe5 !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# GEMINI
# =========================

genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# =========================
# MEMORY
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# SIDEBAR
# =========================

st.sidebar.title("⚡ VEER AI X")

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# =========================
# HEADER
# =========================

st.markdown("""
<h1 class="glow-title">
⚡ VEER AI X ⚡
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<div class="shine"
style="
text-align:center;
font-size:18px;
margin-bottom:20px;">
> SYSTEM ONLINE | GEMINI CONNECTED | VEER AI ACTIVE
</div>
""", unsafe_allow_html=True)

# =========================
# CHAT HISTORY
# =========================

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# CHAT INPUT
# =========================

prompt = st.chat_input(
    "Ask Anything..."
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

    try:

        conversation = ""

        for m in st.session_state.messages:
            conversation += (
                f"{m['role']}: "
                f"{m['content']}\n"
            )

     final_prompt = f"""
You are VEER AI X.

Rules:

- Your name is VEER AI X.
- Never say you are Google Gemini.
- Understand Hindi, English and Hinglish.
- Reply in the same language used by the user.
- If user writes Hindi, answer in Hindi.
- If user writes English, answer in English.
- If user writes Hinglish, answer in Hinglish.
- Remember previous messages in the conversation.
- Be friendly and intelligent.
- Give detailed answers when needed.
- Short answers for simple questions.
- Act like a premium AI assistant.

Conversation:

{conversation}

Current User Message:
{prompt}
"""
        }
    )
