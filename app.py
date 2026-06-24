import streamlit as st
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="VEER AI",
    page_icon="🤖",
    layout="wide"
)

# ---------------- SESSION ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#0f172a,#1e293b);
}

.main-title{
    text-align:center;
    color:white;
    font-size:48px;
    font-weight:700;
    margin-bottom:5px;
}

.subtitle{
    text-align:center;
    color:#cbd5e1;
    margin-bottom:25px;
}

[data-testid="stSidebar"]{
    background:#111827;
}

.stChatMessage{
    background:rgba(255,255,255,0.08);
    border-radius:15px;
    padding:10px;
    margin-bottom:10px;
}

.stMarkdown,
.stMarkdown p,
.stChatMessage,
[data-testid="stChatMessageContent"],
[data-testid="stChatMessageContent"] p{
    color:white !important;
}

input{
    color:white !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    "<h1 class='main-title'>🤖 VEER AI</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='subtitle'>Running on Gemini 2.5 Flash</p>",
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.title("⚙️ VEER AI")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.info("Gemini 2.5 Flash")
    st.caption("Modern AI Assistant")

# ---------------- GEMINI FUNCTION ----------------
def get_gemini_response(prompt):

    api_key = st.secrets["GEMINI_API_KEY"]

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    try:

        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )

        if response.status_code == 200:

            data = response.json()

            return data["candidates"][0]["content"]["parts"][0]["text"]

        return f"API Error: {response.status_code}"

    except Exception as e:

        return f"Error: {str(e)}"

# ---------------- CHAT HISTORY ----------------
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------------- INPUT ----------------
prompt = st.chat_input("Ask VEER AI...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            reply = get_gemini_response(prompt)

            st.write(reply)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply
        }
    )

    st.rerun()
