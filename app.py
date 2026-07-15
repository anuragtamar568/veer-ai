import streamlit as st
import google.generativeai as genai

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="VEER AI Pro",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CODER THEME ----------------
st.markdown("""
<style>
.stApp{
    background:#0d1117;
    color:#e6edf3;
}

h1{
    color:#00ff88 !important;
    text-align:center;
    text-shadow:0 0 10px #00ff88;
}

section[data-testid="stSidebar"]{
    background:#090c10;
}

[data-testid="stChatMessage"]{
    background:#161b22;
    border:1px solid #00ff88;
    border-radius:12px;
    padding:10px;
    margin-bottom:10px;
}

.stButton button{
    background:#00ff88;
    color:black;
    font-weight:bold;
}

p, div, span{
    color:#e6edf3 !important;
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

# ---------------- MEMORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SIDEBAR ----------------
st.sidebar.title("🚀 VEER AI Controls")

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# ---------------- TITLE ----------------
st.title("🤖 VEER AI Pro")

# ---------------- CHAT HISTORY ----------------
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- CHAT INPUT ----------------
prompt = st.chat_input("Ask anything...")

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

        chat_text = ""

        for m in st.session_state.messages:
            chat_text += (
                f"{m['role']}: "
                f"{m['content']}\n"
            )

        final_prompt = f"""
You are VEER AI Pro.

Rules:
- Never say you are Google Gemini.
- Say you are VEER AI Pro.
- Reply in Hindi if user writes Hindi.
- Reply in English if user writes English.
- Be friendly and intelligent.

Conversation:
{chat_text}
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
