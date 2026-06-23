import streamlit as st

st.set_page_config(
    page_title="VEER AI Enterprise",
    page_icon="🤖",
    layout="wide"
)

# ================= CSS =================

st.markdown("""
<style>

/* Animated Background */

.stApp{
    background: linear-gradient(
        -45deg,
        #0f172a,
        #7c3aed,
        #0891b2,
        #2563eb,
        #db2777,
        #16a34a
    );

    background-size: 600% 600%;
    animation: gradient 18s ease infinite;
}

@keyframes gradient{
    0%{background-position:0% 50%;}
    50%{background-position:100% 50%;}
    100%{background-position:0% 50%;}
}

/* Hide Streamlit Header */

header{
    visibility:hidden;
}

/* Main Title */

.main-title{
    text-align:center;
    font-size:70px;
    font-weight:900;

    background: linear-gradient(
        90deg,
        #00ffff,
        #ff00ff,
        #00ff99,
        #ffff00
    );

    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;

    text-shadow:
        0 0 10px #00ffff,
        0 0 20px #00ffff,
        0 0 40px #00ffff;
}

/* Subtitle */

.sub{
    text-align:center;
    color:white;
    font-size:20px;
    text-shadow:0 0 10px white;
}

/* Glass Card */

.glass{
    background:rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);

    border:1px solid rgba(255,255,255,.2);

    border-radius:25px;

    padding:30px;

    box-shadow:
        0 8px 32px rgba(0,0,0,.3),
        0 0 30px rgba(0,255,255,.2);
}

/* Sidebar */

[data-testid="stSidebar"]{
    background:rgba(0,0,0,.35);
    backdrop-filter: blur(25px);
}

/* Sidebar Text */

[data-testid="stSidebar"] *{
    color:white !important;
}

/* Buttons */

.stButton button{

    width:100%;
    height:55px;

    border:none;
    border-radius:18px;

    color:white;
    font-size:18px;
    font-weight:700;

    background: linear-gradient(
        90deg,
        #00ffff,
        #ff00ff
    );

    box-shadow:
        0 0 20px #00ffff;

    transition:0.3s;
}

.stButton button:hover{

    transform:translateY(-3px);

    box-shadow:
        0 0 35px #ff00ff;
}

/* Chat Messages */

.stChatMessage{

    background:rgba(255,255,255,0.08);

    border-radius:22px;

    border:1px solid rgba(255,255,255,.2);

    box-shadow:
        0 0 20px rgba(0,255,255,.2);

    color:white;
}

/* Input Box */

[data-testid="stChatInput"]{
    border-radius:20px;
    box-shadow:0 0 20px cyan;
}

/* General Text */

p, span, div, label{
    color:white !important;
}

</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================

with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/4712/4712109.png",
        width=120
    )

    st.title("VEER AI")

    st.markdown("---")

    mode = st.selectbox(
        "🧠 AI Mode",
        [
            "VEER",
            "Jarvis",
            "Teacher",
            "Coder"
        ]
    )

    voice = st.toggle("🔊 Voice Reply", True)

    st.button("🗑️ New Chat")

    st.button("📄 Download Chat")

    st.button("🚪 Logout")

# ================= MAIN =================

st.markdown(
    "<h1 class='main-title'>🤖 VEER AI</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='sub'>Next Generation Enterprise Assistant</p>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='glass'>
    <h2>✨ Welcome Anurag Sir</h2>

    <p>
    VEER AI is ready to assist you.
    Ask anything related to business, coding,
    education, research or automation.
    </p>
    </div>
    """,
    unsafe_allow_html=True
)

prompt = st.chat_input(
    "अनुराग सर, कुछ पूछिए..."
)

if prompt:

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        st.write(
            f"अनुराग सर, आपने पूछा: {prompt}"
        )
