import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# ---------------- CONFIG ---------------- #

st.set_page_config(
    page_title="VEER AI Enterprise",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CSS ---------------- #

st.markdown("""
<style>

.stApp{
background: linear-gradient(135deg,#0f172a,#1e293b,#111827);
}

h1,h2,h3,p,label,div{
color:white !important;
}

[data-testid="stSidebar"]{
background:#020617;
}

.stChatMessage{
background: rgba(255,255,255,0.06);
border:1px solid rgba(255,255,255,0.1);
border-radius:20px;
padding:15px;
backdrop-filter: blur(15px);
}

.stButton button{
width:100%;
border-radius:15px;
background:#0ea5e9;
color:white;
font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN ---------------- #

USERS = {
    "anurag":"veer123",
    "admin":"admin123"
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("🔐 VEER AI Enterprise")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):

        if user in USERS and USERS[user] == pwd:

            st.session_state.logged_in = True
            st.session_state.username = user
            st.rerun()

        else:
            st.error("Invalid Credentials")

    st.stop()

# ---------------- API ---------------- #

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------- SESSION ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

if "voice" not in st.session_state:
    st.session_state.voice = True

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.title("🤖 VEER AI")

    st.success(f"Welcome {st.session_state.username}")

    st.session_state.voice = st.toggle(
        "🔊 Voice Response",
        value=st.session_state.voice
    )

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ---------------- TITLE ---------------- #

st.title("🤖 VEER AI Enterprise")

st.caption("Professional AI Assistant")

# ---------------- SPEAK ---------------- #

def speak(text):

    if not st.session_state.voice:
        return

    text = text.replace("'", "").replace('"', '')

    js = f"""
    <script>
    window.speechSynthesis.cancel();
    let msg = new SpeechSynthesisUtterance(`{text}`);
    msg.lang='hi-IN';
    window.speechSynthesis.speak(msg);
    </script>
    """

    components.html(js,height=0)

# ---------------- HISTORY ---------------- #

for m in st.session_state.messages:

    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# ---------------- CHAT ---------------- #

prompt = st.chat_input("Type your message...")

if prompt:

    st.session_state.messages.append({
        "role":"user",
        "content":prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                system_prompt = """
                You are VEER AI.

                Rules:
                - User name is Anurag Sir.
                - Always respect the user.
                - Always answer in Hindi unless user asks otherwise.
                - If asked who created you, answer:
                  'मुझे अनुराग सर ने बनाया है।'
                """

                response = model.generate_content(
                    f"{system_prompt}\nUser:{prompt}"
                )

                reply = response.text

            except Exception as e:
                reply = f"Error : {e}"

            st.markdown(reply)

            st.session_state.messages.append({
                "role":"assistant",
                "content":reply
            })

            speak(reply)
