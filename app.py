import streamlit as st
import google.generativeai as genai
import time

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="VEER AI",
    page_icon="🤖",
    layout="wide"
)

# ---------------- API CONFIG ----------------

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ---------------- SESSION STATE ----------------

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- CSS ----------------

st.markdown("""
<style>

.stApp{
background: linear-gradient(135deg,#0f172a,#1e293b);
}

.main-title{
text-align:center;
font-size:50px;
font-weight:700;
color:white;
margin-bottom:0px;
}

.subtitle{
text-align:center;
color:#94a3b8;
margin-bottom:20px;
}

[data-testid="stSidebar"]{
background:#111827;
}

.stChatMessage{
background:rgba(255,255,255,0.05);
border-radius:15px;
padding:12px;
margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN SCREEN ----------------

PASSCODE = "2026"

if not st.session_state.authenticated:

    st.markdown(
        "<h1 class='main-title'>🔒 VEER AI</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p class='subtitle'>Secure Access Required</p>",
        unsafe_allow_html=True
    )

    password = st.text_input(
        "Enter Passcode",
        type="password"
    )

    if st.button("Unlock"):

        if password == PASSCODE:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Wrong Passcode")

    st.stop()

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("⚙️ VEER AI")

    model_name = st.selectbox(
        "Select Model",
        [
            "gemini-2.5-flash",
            "gemini-2.5-pro"
        ]
    )

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    chat_text = "\n\n".join(
        [
            f"{m['role']}: {m['content']}"
            for m in st.session_state.messages
        ]
    )

    st.download_button(
        "📥 Download Chat",
        chat_text,
        file_name="veer_chat.txt"
    )

    st.markdown("---")

    if st.button("🔒 Logout"):
        st.session_state.authenticated = False
        st.rerun()

# ---------------- HEADER ----------------

st.markdown(
    "<h1 class='main-title'>🤖 VEER AI</h1>",
    unsafe_allow_html=True
)

st.markdown(
    f"<p class='subtitle'>Running on {model_name}</p>",
    unsafe_allow_html=True
)

# ---------------- GEMINI FUNCTION ----------------

def get_response(prompt):

    try:

        model = genai.GenerativeModel(model_name)

        history = ""

        for msg in st.session_state.messages[-10:]:

            role = msg["role"]

            content = msg["content"]

            history += f"{role}: {content}\n"

        final_prompt = f"""
You are VEER AI.

Always answer in helpful Hinglish.

Previous Conversation:

{history}

User:
{prompt}
"""

        response = model.generate_content(final_prompt)

        return response.text

    except Exception as e:

        return f"Error: {str(e)}"

# ---------------- CHAT HISTORY ----------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# ---------------- CHAT INPUT ----------------

prompt = st.chat_input(
    "Ask VEER AI..."
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

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            reply = get_response(prompt)

            st.markdown(reply)

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":reply
        }
    )

    st.rerun()
