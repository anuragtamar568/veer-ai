import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="VEER AI",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#0f172a,#1e1b4b,#111827);
}

[data-testid="stHeader"]{
    background: transparent;
}

h1{
    text-align:center;
    color:white;
    font-size:3.2rem;
}

.block-container{
    padding-top:2rem;
}

.stChatMessage{
    border-radius:20px;
    padding:12px;
    background:rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border:1px solid rgba(255,255,255,0.1);
    margin-bottom:12px;
}

[data-testid="stSidebar"]{
    background:#0b1120;
}

.stButton button{
    width:100%;
    border-radius:12px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ---------------- API SETUP ----------------

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("⚠️ GEMINI_API_KEY नहीं मिली")
    st.stop()

# ---------------- MODEL ----------------

model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------- SESSION ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("⚙️ VEER AI")

    st.markdown("---")

    st.markdown("""
    ### Features

    ✅ Hindi AI  
    ✅ Smart Replies  
    ✅ Voice Output  
    ✅ Gemini 2.5 Flash  
    """)

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------- TITLE ----------------

st.title("🤖 VEER AI")

st.caption("Your Personal Hindi AI Assistant")

# ---------------- VOICE ----------------

def speak(text):

    text = (
        text.replace("'", "")
        .replace('"', '')
        .replace("\n", " ")
    )

    js = f"""
    <script>

    window.speechSynthesis.cancel();

    let msg = new SpeechSynthesisUtterance(`{text}`);
    msg.lang='hi-IN';
    msg.rate=1;
    msg.pitch=1;

    window.speechSynthesis.speak(msg);

    </script>
    """

    components.html(js, height=0)

# ---------------- SHOW HISTORY ----------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- USER INPUT ----------------

prompt = st.chat_input("अनुराग सर, कुछ पूछिए...")

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("VEER सोच रहा है..."):

            try:

                system_prompt = """
                तुम VEER नाम के एक intelligent AI assistant हो।

                नियम:
                - हमेशा हिंदी में उत्तर दो।
                - जवाब स्मार्ट, स्पष्ट और मददगार होने चाहिए।
                - यदि यूज़र अंग्रेज़ी में पूछे, तब भी हिंदी में उत्तर दो।
                """

                response = model.generate_content(
                    f"{system_prompt}\n\nUser: {prompt}"
                )

                reply = response.text

            except Exception as e:

                reply = f"❌ Error: {e}"

            st.markdown(reply)

            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

            speak(reply)
