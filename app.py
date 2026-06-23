import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="VEER AI",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#0f172a,#1e293b,#111827);
}

[data-testid="stHeader"]{
    background: transparent;
}

h1{
    text-align:center;
    color:#38bdf8;
    font-size:3.5rem;
    font-weight:bold;
}

.stMarkdown, p, span, div, label{
    color:white !important;
}

.stChatMessage{
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(10px);
    border:1px solid rgba(255,255,255,0.1);
    border-radius:20px;
    padding:15px;
    margin-bottom:10px;
}

[data-testid="stSidebar"]{
    background:#0b1120;
}

.stButton button{
    width:100%;
    border:none;
    border-radius:12px;
    background:linear-gradient(90deg,#06b6d4,#3b82f6);
    color:white;
    font-weight:bold;
    height:3em;
}

.stButton button:hover{
    transform: scale(1.02);
    transition:0.2s;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- GEMINI API ---------------- #

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("⚠️ GEMINI_API_KEY नहीं मिली")
    st.stop()

# ---------------- MODEL ---------------- #

model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.title("⚙️ VEER AI")

    st.markdown("---")

    st.markdown("""
### Features

✅ Hindi AI Assistant  
✅ Voice Response  
✅ Gemini 2.5 Flash  
✅ Smart Memory (Current Session)  
✅ Futuristic Theme
""")

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------- TITLE ---------------- #

st.title("🤖 VEER AI")

st.markdown(
    "<center><h4 style='color:#94a3b8;'>Your Personal Hindi AI Assistant</h4></center>",
    unsafe_allow_html=True
)

# ---------------- VOICE FUNCTION ---------------- #

def speak(text):

    clean = (
        text.replace("\n", " ")
        .replace("'", "")
        .replace('"', "")
    )

    js = f"""
    <script>

    window.speechSynthesis.cancel();

    let msg = new SpeechSynthesisUtterance(`{clean}`);
    msg.lang = 'hi-IN';
    msg.rate = 1;
    msg.pitch = 1;

    window.speechSynthesis.speak(msg);

    </script>
    """

    components.html(js, height=0)

# ---------------- SHOW CHAT ---------------- #

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- USER INPUT ---------------- #

prompt = st.chat_input("अनुराग सर, कुछ पूछिए...")

if prompt:

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("⚡ VEER सोच रहा है..."):

            try:

                system_prompt = """
तुम VEER नाम के एक Advanced AI Assistant हो।

नियम:

1. User का नाम 'अनुराग सर' है।
2. हमेशा User को 'अनुराग सर' कहकर संबोधित करो।
3. यदि User पूछे 'तुम्हें किसने बनाया?' तो जवाब दो:
   'अनुराग सर, मुझे आपने बनाया और विकसित किया है।'

4. हमेशा हिंदी में उत्तर दो।
5. जवाब स्मार्ट, स्पष्ट और दोस्ताना होने चाहिए।
6. यदि User अंग्रेज़ी में पूछे तब भी हिंदी में उत्तर दो।
7. अपने उत्तरों में सम्मान बनाए रखो।
"""

                response = model.generate_content(
                    f"{system_prompt}\n\nUser: {prompt}"
                )

                reply = response.text

            except Exception as e:
                reply = f"❌ Error: {str(e)}"

            st.markdown(reply)

            st.session_state.messages.append(
                {"role": "assistant", "content": reply}
            )

            speak(reply)
