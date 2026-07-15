import streamlit as st
import google.generativeai as genai

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="VEER AI Ultra",
    page_icon="🚀",
    layout="wide"
)

# ---------------- AESTHETIC THEME ----------------

st.markdown("""
<style>

/* Background */
.stApp{
    background: linear-gradient(
        135deg,
        #0f172a,
        #111827,
        #1e293b
    );
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background: rgba(15,23,42,0.95);
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Title */
.main-title{
    text-align:center;
    font-size:55px;
    font-weight:800;
    margin-top:10px;
    background: linear-gradient(
        90deg,
        #38bdf8,
        #8b5cf6,
        #ec4899
    );
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

/* Subtitle */
.sub-title{
    text-align:center;
    color:#cbd5e1;
    margin-bottom:25px;
}

/* Chat Messages */
[data-testid="stChatMessage"]{
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(18px);
    border-radius:18px;
    border:1px solid rgba(255,255,255,0.08);
    padding:12px;
}

/* Text */
p,span,div{
    color:#f8fafc !important;
}

/* Buttons */
.stButton button{
    width:100%;
    border:none;
    border-radius:12px;
    background: linear-gradient(
        90deg,
        #3b82f6,
        #8b5cf6
    );
    color:white;
    font-weight:bold;
}

/* Input */
.stChatInputContainer{
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
    border-radius:20px;
}

/* Scrollbar */
::-webkit-scrollbar{
    width:8px;
}
::-webkit-scrollbar-thumb{
    background:#8b5cf6;
    border-radius:20px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- GEMINI ----------------

genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# ---------------- SESSION ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SIDEBAR ----------------

st.sidebar.title("🚀 VEER AI Controls")

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# ---------------- HEADER ----------------

st.markdown(
    '<div class="main-title">✨ VEER AI Ultra</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Your Personal AI Assistant</div>',
    unsafe_allow_html=True
)

# ---------------- HISTORY ----------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- INPUT ----------------

prompt = st.chat_input(
    "Ask anything..."
)

if prompt:

    st.session_state.messages.append({
        "role":"user",
        "content":prompt
    })

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
You are VEER AI Ultra.

Rules:
- Never say you are Google Gemini.
- Always introduce yourself as VEER AI Ultra.
- Reply in Hindi if user uses Hindi.
- Reply in English if user uses English.
- Be helpful and intelligent.

Conversation:

{conversation}
"""

        response = model.generate_content(
            final_prompt
        )

        reply = response.text

    except Exception as e:

        reply = f"Error: {e}"

    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append({
        "role":"assistant",
        "content":reply
    })
