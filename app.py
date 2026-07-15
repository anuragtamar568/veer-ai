import streamlit as st
import google.generativeai as genai

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="VEER AI",
    page_icon="⚡",
    layout="wide"
)

# =========================
# HACKER + AESTHETIC THEME
# =========================

st.markdown("""
<style>

.stApp{
    background: linear-gradient(
        135deg,
        #020617,
        #0f172a,
        #000000
    );
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
    font-weight:800;

    background:linear-gradient(
        90deg,
        #00ff88,
        #00ffff,
        #00ff88
    );

    background-size:200% auto;

    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;

    animation:shine 3s linear infinite;
}

@keyframes shine{
    to{
        background-position:200% center;
    }
}

/* Subtitle */
.subtitle{
    text-align:center;
    color:#00ff88;
    font-size:18px;
    margin-bottom:25px;

    text-shadow:
        0 0 10px #00ff88;
}

/* Chat */
[data-testid="stChatMessage"]{
    background:rgba(0,255,136,0.05);
    border:1px solid rgba(0,255,136,0.25);
    border-radius:18px;
    box-shadow:0 0 15px rgba(0,255,136,.12);
}

/* Input */
.stChatInputContainer{
    border:2px solid #00ff88;
    border-radius:20px;
}

/* Buttons */
.stButton button{
    background:#00ff88 !important;
    color:black !important;
    font-weight:bold !important;
}

/* Text */
p,span,div{
    color:#f8fafc !important;
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
<div class="subtitle">
🚀 Hindi • English • Hinglish • Smart AI
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

prompt = st.chat_input("Ask Anything...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
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
You are VEER AI.

Rules:
- Your name is VEER AI X.
- Never say you are Google Gemini.
- Understand Hindi, English and Hinglish.
- Reply in the same language used by the user.
- Remember previous messages in this chat.
- Be friendly and intelligent.
- Give detailed answers when needed.
- Keep short answers for simple questions.

Conversation:
{conversation}

Current User Message:
{prompt}
"""

        response = model.generate_content(
            final_prompt
        )

        reply = response.text

    except Exception as e:

        reply = f"Error: {e}"

    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply
        }
    )
