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
background:
linear-gradient(135deg,#020617,#0f172a,#1e293b);
}

[data-testid="stSidebar"]{
background:rgba(15,23,42,.85);
backdrop-filter: blur(20px);
}

h1{
text-align:center;
font-size:4rem;
background:linear-gradient(90deg,#38bdf8,#818cf8,#ec4899);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.stChatMessage{
background:rgba(255,255,255,.06);
backdrop-filter:blur(20px);
border:1px solid rgba(255,255,255,.1);
border-radius:24px;
padding:18px;
}

.stButton button{
width:100%;
border-radius:16px;
background:linear-gradient(90deg,#06b6d4,#6366f1);
color:white;
font-weight:700;
border:none;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN ---------------- #

USERS = {
    "anurag":"veer123"
}

if "logged" not in st.session_state:
    st.session_state.logged = False

if not st.session_state.logged:

    st.title("🔐 VEER AI Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):

        if u in USERS and USERS[u] == p:

            st.session_state.logged = True
            st.session_state.user = u
            st.rerun()

        else:
            st.error("Wrong credentials")

    st.stop()

# ---------------- API ---------------- #

genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------- STATES ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages=[]

if "voice" not in st.session_state:
    st.session_state.voice=True

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.title("🤖 VEER AI")

    st.success(
        f"Welcome {st.session_state.user}"
    )

    mode = st.selectbox(
        "AI Personality",
        [
            "VEER",
            "Jarvis",
            "Teacher",
            "Coder"
        ]
    )

    st.session_state.voice = st.toggle(
        "Voice Reply",
        value=True
    )

    st.markdown("---")

    if st.button("🗑️ New Chat"):
        st.session_state.messages=[]
        st.rerun()

    if st.button("🚪 Logout"):
        st.session_state.logged=False
        st.rerun()

# ---------------- TITLE ---------------- #

st.title("🤖 VEER AI Enterprise")

st.caption(
    "Next Generation Enterprise Assistant"
)

# ---------------- SPEAK ---------------- #

def speak(text):

    if not st.session_state.voice:
        return

    text=text.replace("'","")

    js=f"""
    <script>
    speechSynthesis.cancel();

    let msg=new SpeechSynthesisUtterance(`{text}`);
    msg.lang='hi-IN';
    speechSynthesis.speak(msg);
    </script>
    """

    components.html(js,height=0)

# ---------------- HISTORY ---------------- #

for m in st.session_state.messages:

    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# ---------------- CHAT ---------------- #

prompt = st.chat_input(
    "अनुराग सर, आदेश दें..."
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

    if mode=="Jarvis":

        personality="""
        तुम Jarvis हो।
        futuristic style में बात करो।
        """

    elif mode=="Teacher":

        personality="""
        तुम expert teacher हो।
        सरल भाषा में समझाओ।
        """

    elif mode=="Coder":

        personality="""
        तुम senior software engineer हो।
        """

    else:

        personality="""
        तुम VEER AI हो।
        User का नाम अनुराग सर है।
        हमेशा अनुराग सर कहकर संबोधित करो।
        अगर पूछा जाए कि तुम्हें किसने बनाया,
        तो जवाब दो:
        'मुझे अनुराग सर ने बनाया है।'
        """

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = model.generate_content(
                    personality + "\nUser:" + prompt
                )

                reply = response.text

            except Exception as e:

                reply = f"Error: {e}"

            st.markdown(reply)

            st.session_state.messages.append(
                {
                    "role":"assistant",
                    "content":reply
                }
            )

            speak(reply)
