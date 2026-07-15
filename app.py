import streamlit as st
import requests
import PyPDF2
import json

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="VEER AI Pro",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main{
    background-color:#0f172a;
}

h1{
    text-align:center;
    color:#38bdf8;
}

.stChatMessage{
    border-radius:15px;
    padding:10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

# ---------------- LOGIN ----------------
def login_screen():

    st.markdown("<h1>🔐 VEER AI Access</h1>",
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        username = st.text_input("Username")
        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            if (
                username == "admin"
                and password == "veer123"
            ):
                st.session_state.authenticated = True
                st.rerun()

            else:
                st.error("Invalid Credentials")

# ---------------- GEMINI FUNCTION ----------------
def ask_gemini(prompt):

    api_key = st.secrets["GEMINI_API_KEY"]

    url = (
        "https://generativelanguage.googleapis.com"
        f"/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    )

    contents = []

    system_prompt = """
    You are VEER AI Pro.

    Rules:
    - Be intelligent.
    - Reply in Hindi or English according to user language.
    - Give accurate answers.
    - Be friendly.
    """

    contents.append({
        "role":"user",
        "parts":[{"text":system_prompt}]
    })

    # previous chat memory
    for msg in st.session_state.messages:

        role = (
            "user"
            if msg["role"] == "user"
            else "model"
        )

        contents.append({
            "role": role,
            "parts":[
                {"text": msg["content"]}
            ]
        })

    # add PDF knowledge
    if st.session_state.pdf_text:

        prompt = f"""
        PDF CONTENT:

        {st.session_state.pdf_text[:15000]}

        USER QUESTION:

        {prompt}
        """

    contents.append({
        "role":"user",
        "parts":[{"text":prompt}]
    })

    try:

        response = requests.post(
            url,
            headers={
                "Content-Type":
                "application/json"
            },
            json={
                "contents": contents
            },
            timeout=60
        )

        if response.status_code == 200:

            data = response.json()

            return data["candidates"][0] \
                ["content"]["parts"][0]["text"]

        return (
            f"API Error "
            f"{response.status_code}\n"
            f"{response.text}"
        )

    except Exception as e:
        return str(e)

# ---------------- MAIN APP ----------------
def main_app():

    st.sidebar.title("🚀 VEER AI Controls")

    # logout
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

    # clear chat
    if st.sidebar.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    # download chat
    chat_json = json.dumps(
        st.session_state.messages,
        indent=2
    )

    st.sidebar.download_button(
        "⬇ Download Chat",
        chat_json,
        "chat_history.json"
    )

    # PDF Upload
    uploaded_file = st.sidebar.file_uploader(
        "Upload PDF",
        type="pdf"
    )

    if uploaded_file:

        pdf_reader = PyPDF2.PdfReader(
            uploaded_file
        )

        text = ""

        for page in pdf_reader.pages:

            text += (
                page.extract_text()
                or ""
            )

        st.session_state.pdf_text = text

        st.sidebar.success(
            "PDF Loaded Successfully"
        )

    st.markdown(
        "<h1>🤖 VEER AI Pro</h1>",
        unsafe_allow_html=True
    )

    # display chat
    for msg in st.session_state.messages:

        with st.chat_message(
            msg["role"]
        ):
            st.markdown(
                msg["content"]
            )

    # user prompt
    if prompt := st.chat_input(
        "Ask anything..."
    ):

        st.session_state.messages.append({
            "role":"user",
            "content":prompt
        })

        with st.chat_message(
            "user"
        ):
            st.markdown(prompt)

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "Thinking..."
            ):

                reply = ask_gemini(
                    prompt
                )

                st.markdown(
                    reply
                )

                st.session_state.messages.append({
                    "role":"assistant",
                    "content":reply
                })

# ---------------- RUN ----------------
if st.session_state.authenticated:
    main_app()
else:
    login_screen()
