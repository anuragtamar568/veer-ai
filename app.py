import streamlit as st
import google.generativeai as genai

# ================= PAGE =================

st.set_page_config(
    page_title="VEER AI // CYBER CORE",
    page_icon="💻",
    layout="wide"
)

# ================= GEMINI =================

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

    # अगर यह model आपके account में न चले
    # तो अपना working model name डालें
    model = genai.GenerativeModel("gemini-2.5-flash")

except Exception as e:
    st.error(f"Gemini Error: {e}")
    st.stop()

# ================= SESSION =================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ================= CSS =================

st.markdown("""
<style>

.stApp{
    background:
    radial-gradient(circle at top,#003300,#000000 70%);
}

header{
    visibility:hidden;
}

.main-title{
    text-align:center;
    font-size:65px;
    font-weight:900;

    color:#00ff41;

    text-shadow:
    0 0 10px #00ff41,
    0 0 20px #00ff41,
    0 0 40px #00ff41,
    0 0 80px #00ff41;
}

/* Sidebar */

[data-testid="stSidebar"]{
    background:#000000;
    border-right:2px solid #00ff41;
}

[data-testid="stSidebar"] *{
    color:#00ff41 !important;
}

/* Cards */

.cyber-card{

    background:rgba(0,255,65,.05);

    border:1px solid #00ff41;

    border-radius:18px;

    padding:18px;

    margin-bottom:15px;

    box-shadow:
    0 0 8px #00ff41,
    inset 0 0 8px rgba(0,255,65,.3);
}

/* Chat */

.stChatMessage{

    background:rgba(0,255,65,.04);

    border:1px solid #00ff41;

    border-radius:18px;

    box-shadow:
    0 0 8px #00ff41;
}

/* Input */

[data-testid="stChatInput"]{

    border:1px solid #00ff41;

    border-radius:15px;

    box-shadow:0 0 10px #00ff41;
}

/* Metrics */

[data-testid="metric-container"]{

    background:rgba(0,255,65,.05);

    border:1px solid #00ff41;

    border-radius:15px;

    box-shadow:0 0 10px #00ff41;
}

/* Buttons */

.stButton button{

    width:100%;

    background:black;

    color:#00ff41;

    border:1px solid #00ff41;

    border-radius:12px;

    box-shadow:0 0 10px #00ff41;
}

.stButton button:hover{
    background:#00ff41;
    color:black;
}

/* Text */

p,span,div,label,h1,h2,h3,h4{
    color:#00ff41 !important;
    font-family:Consolas, monospace !important;
}

</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================

with st.sidebar:

    st.markdown("# ⚡ VEER AI")

    st.success("🟢 SYSTEM ONLINE")

    st.markdown("""
    <div class="cyber-card">
        <h3>👤 Face Recognition</h3>
    </div>

    <div class="cyber-card">
        <h3>🤖 Smart Assistant</h3>
    </div>

    <div class="cyber-card">
        <h3>🛡️ Security Shield</h3>
    </div>

    <div class="cyber-card">
        <h3>🌐 Web Intelligence</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("🗑️ NEW CHAT"):
        st.session_state.messages = []
        st.rerun()

    chat_text = ""

    for m in st.session_state.messages:
        chat_text += f"{m['role']} : {m['content']}\n\n"

    st.download_button(
        "📥 DOWNLOAD CHAT",
        chat_text,
        file_name="veer_chat.txt"
    )

# ================= TITLE =================

st.markdown("""
<h1 class='main-title'>
⚡ VEER AI // CYBER CORE ⚡
</h1>
""", unsafe_allow_html=True)

# ================= DASHBOARD =================

st.markdown("""
<div class='cyber-card'>

## 🟢 SYSTEM STATUS : ONLINE

👤 USER : ANURAG SIR

🧠 AI ENGINE : GEMINI

🛡 SECURITY : ACTIVE

⚡ MODE : CYBER INTELLIGENCE

</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("💬 Messages", len(st.session_state.messages))

with c2:
    st.metric("🧠 AI", "ONLINE")

with c3:
    st.metric("⚡ Status", "ACTIVE")

# ================= HISTORY =================

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================= CHAT =================

prompt = st.chat_input(">>> ENTER COMMAND")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("⚡ ACCESSING CYBER CORE..."):

            try:

                system_prompt = f"""
                You are VEER AI.

                User name is Anurag Sir.

                Rules:
                - Always answer in Hindi.
                - Always call the user 'Anurag Sir'.
                - Be smart and professional.

                User: {prompt}
                """

                response = model.generate_content(system_prompt)

                reply = response.text

            except Exception as e:

                if "429" in str(e):
                    reply = """
🚫 API LIMIT EXCEEDED

Gemini free quota समाप्त हो गई है।

कृपया कुछ समय बाद पुनः प्रयास करें।
"""
                else:
                    reply = f"❌ Error: {e}"

            st.markdown(reply)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply
        }
    )
