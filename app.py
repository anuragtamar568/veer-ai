
import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from datetime import datetime
from zoneinfo import ZoneInfo
import hmac
import re

st.set_page_config(
    page_title="VEER AI X | BOSS EDITION",
    page_icon="🤖",
    layout="wide"
)

# =============== SECURITY & API ===============

API_KEY = st.secrets.get("GEMINI_API_KEY", "")
LOCK_PIN = st.secrets.get("ROBOTIC_LOCK_PIN", "")

if not API_KEY or not LOCK_PIN:
    st.error("GEMINI_API_KEY aur ROBOTIC_LOCK_PIN secrets.toml mein set karein.")
    st.stop()

genai.configure(api_key=API_KEY)

if "unlocked" not in st.session_state:
    st.session_state.unlocked = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "voice_style" not in st.session_state:
    st.session_state.voice_style = "BOSS DEEP"

if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = True

# =============== LIVE INDIAN TIME ===============

def current_time():
    return datetime.now(ZoneInfo("Asia/Kolkata"))

# =============== ROBOTIC THEME ===============

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@500;600;700&display=swap');

.stApp {
    background: radial-gradient(ellipse at top, #09243b, #020711 70%);
    color: #d9fbff;
    font-family: 'Rajdhani', sans-serif;
}

[data-testid="stSidebar"] {
    background: #03101f;
    border-right: 1px solid #00eaff;
}

.robot-title {
    text-align: center;
    font-family: 'Orbitron', sans-serif;
    font-size: 52px;
    font-weight: 900;
    color: #bdfaff;
    letter-spacing: 7px;
    text-shadow: 0 0 8px #00eaff, 0 0 22px #00eaff,
                 0 0 45px #008cff;
}

.robot-sub {
    text-align: center;
    color: #00eaff;
    font-family: 'Orbitron', sans-serif;
    font-size: 11px;
    letter-spacing: 4px;
    text-shadow: 0 0 10px #00eaff;
    margin-bottom: 25px;
}

.status {
    text-align: center;
    color: #00eaff;
    background: #04192a;
    border: 1px solid #00eaff;
    padding: 12px;
    border-radius: 8px;
    font-family: 'Orbitron', sans-serif;
    font-size: 11px;
    box-shadow: 0 0 15px #003d55;
}

.welcome {
    text-align: center;
    background: linear-gradient(140deg, #061e33, #030b19);
    border: 1px solid #00eaff;
    border-radius: 14px;
    padding: 28px;
    margin: 20px auto;
    box-shadow: 0 0 25px #003d55;
}

.welcome h2 {
    color: #00eaff;
    font-family: 'Orbitron', sans-serif;
    text-shadow: 0 0 12px #00eaff;
}

.welcome p {
    color: #d9fbff;
    font-size: 19px;
    text-shadow: 0 0 7px #00bfff;
}

[data-testid="stChatMessage"] {
    background: rgba(3, 20, 37, .95);
    border: 1px solid #007c99;
    border-radius: 12px;
    box-shadow: 0 0 12px rgba(0,234,255,.13);
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    color: #d9fbff !important;
    font-size: 18px !important;
    text-shadow: 0 0 6px rgba(0,234,255,.55);
    line-height: 1.65;
}

[data-testid="stChatInput"] {
    background: #041323 !important;
    border: 1px solid #00eaff !important;
    border-radius: 10px !important;
    box-shadow: 0 0 15px rgba(0,234,255,.4);
}

[data-testid="stChatInput"] textarea {
    color: #d9fbff !important;
    -webkit-text-fill-color: #d9fbff !important;
}

.stButton button {
    background: linear-gradient(90deg,#075a83,#087e9c) !important;
    color: white !important;
    border: 1px solid #00eaff !important;
    border-radius: 7px !important;
    font-family: 'Orbitron', sans-serif !important;
    box-shadow: 0 0 10px rgba(0,234,255,.2);
}

.stButton button:hover {
    box-shadow: 0 0 22px #00eaff;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #9ffaff !important;
}

h1, h2, h3 {
    color: #00eaff !important;
    text-shadow: 0 0 10px #00eaff;
}

.voice-info {
    border: 1px solid #007d9a;
    border-radius: 8px;
    padding: 12px;
    color: #a9faff;
    background: #041525;
    text-shadow: 0 0 8px #00eaff;
}
</style>
""", unsafe_allow_html=True)

# =============== BOSS VOICE ENGINE ===============

def speak(text, style="BOSS DEEP"):
    # Browser's available speech voices are used.
    # A male-sounding voice is preferred when available.
    import json

    safe_text = json.dumps(str(text), ensure_ascii=False)
    safe_style = json.dumps(style)

    html = """
    <script>
    (() => {
        const text = __TEXT__;
        const style = __STYLE__;

        if (!window.speechSynthesis || !text) return;

        const synth = window.speechSynthesis;
        synth.cancel();

        function startSpeaking() {
            const voices = synth.getVoices();
            const utterance = new SpeechSynthesisUtterance(text);

            const maleVoice = voices.find(v =>
                /david|mark|daniel|alex|james|george|male|guy|ryan/i
                .test(v.name)
            );

            const englishVoice = voices.find(v =>
                /^en-US/i.test(v.lang) &&
                !/female|zira|samantha/i.test(v.name)
            );

            const hindiVoice = voices.find(v =>
                /^hi-IN/i.test(v.lang) &&
                /male|hemant|madhur/i.test(v.name)
            );

            const hindiText = /[\u0900-\u097F]/.test(text);

            let selectedVoice;

            if (hindiText) {
                selectedVoice = hindiVoice || voices.find(v =>
                    /^hi-IN/i.test(v.lang)
                );
            }

            if (!selectedVoice) {
                selectedVoice = maleVoice || englishVoice;
            }

            if (selectedVoice) {
                utterance.voice = selectedVoice;
            }

            if (style === "BOSS DEEP") {
                utterance.rate = 0.82;
                utterance.pitch = 0.55;
            } else if (style === "ULTRA ROBOTIC") {
                utterance.rate = 0.76;
                utterance.pitch = 0.4;
            } else if (style === "COMMANDER") {
                utterance.rate = 0.9;
                utterance.pitch = 0.62;
            }

            utterance.volume = 1;
            synth.speak(utterance);
        }

        if (synth.getVoices().length) {
            startSpeaking();
        } else {
            synth.onvoiceschanged = () => {
                synth.onvoiceschanged = null;
                startSpeaking();
            };
        }
    })();
    </script>
    """

    html = html.replace("__TEXT__", safe_text)
    html = html.replace("__STYLE__", safe_style)
    components.html(html, height=0)

# =============== LOCK SCREEN ===============

if not st.session_state.unlocked:
    st.markdown('<div class="robot-title">VEER AI X</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="robot-sub">BOSS SECURITY SYSTEM</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="welcome">
        <h2>🔐 SYSTEM LOCKED</h2>
        <p>AUTHORIZED ACCESS ONLY</p>
        <p>ROBOTIC SECURITY SHIELD ACTIVE</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("unlock"):
        pin = st.text_input("ENTER YOUR SECURITY PIN", type="password")
        submit = st.form_submit_button("🔓 UNLOCK SYSTEM",
                                       use_container_width=True)

    if submit:
        if hmac.compare_digest(pin, str(LOCK_PIN)):
            st.session_state.unlocked = True
            st.rerun()
        else:
            st.error("ACCESS DENIED — WRONG PIN")

    st.stop()

# =============== SIDEBAR ===============

with st.sidebar:
    st.markdown("## 🤖 VEER AI X")
    st.caption("ADVANCED ROBOTIC INTELLIGENCE")
    st.success("● SYSTEM ONLINE")

    st.markdown("---")
    st.markdown("### 👑 BOSS CONTROL")

    st.caption("CREATOR: ANURAG")

    st.markdown("### 🔊 VOICE PROFILE")

    voice_style = st.selectbox(
        "SELECT ROBOTIC VOICE",
        ["BOSS DEEP", "ULTRA ROBOTIC", "COMMANDER"]
    )
    st.session_state.voice_style = voice_style

    st.session_state.voice_enabled = st.toggle(
        "AI VOICE REPLY",
        value=st.session_state.voice_enabled
    )

    st.markdown("""
    <div class="voice-info">
        🔊 DEEP MALE VOICE<br>
        ⚡ LOW PITCH<br>
        🤖 ROBOTIC RESPONSE<br>
        👑 BOSS MODE ACTIVE
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔊 TEST BOSS VOICE", use_container_width=True):
        speak(
            "Greetings Boss. I am VEER AI X. All systems are online. "
            "Awaiting your command.",
            voice_style
        )

    st.markdown("---")

    model_name = st.selectbox(
        "AI ENGINE",
        ["gemini-2.5-flash", "gemini-1.5-flash"]
    )

    if st.button("🧹 CLEAR CHAT", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.button("🔒 LOCK SYSTEM", use_container_width=True):
        st.session_state.unlocked = False
        st.rerun()

    now = current_time()
    st.markdown("---")
    st.caption("INDIA DATE")
    st.write(now.strftime("%d %B %Y"))
    st.caption("INDIA TIME")
    st.write(now.strftime("%I:%M:%S %p"))

# =============== MAIN INTERFACE ===============

st.markdown('<div class="robot-title">VEER AI X</div>',
            unsafe_allow_html=True)

st.markdown(
    '<div class="robot-sub">BOSS EDITION • DEEP ROBOTIC INTELLIGENCE</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="status">● SYSTEM ONLINE | BOSS MODE ACTIVE '
    '| NEURAL CORE READY</div>',
    unsafe_allow_html=True
)

if not st.session_state.messages:
    st.markdown("""
    <div class="welcome">
        <h2>🤖 SYSTEM INITIALIZED</h2>
        <p>Greetings Boss Anurag.</p>
        <p>I am VEER AI X, your personal robotic assistant.
        All systems are ready. Give me your command, Boss.</p>
        <p>⚡ DEEP VOICE | 🔐 SECURE CORE | 🌐 MULTILINGUAL</p>
    </div>
    """, unsafe_allow_html=True)

# =============== CHAT HISTORY ===============

for msg in st.session_state.messages:
    avatar = "👑" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# =============== USER INPUT ===============

prompt = st.chat_input("BOSS, GIVE YOUR COMMAND TO VEER AI X...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user", avatar="👑"):
        st.markdown(prompt)

    now = current_time()
    date_string = now.strftime("%d %B %Y")
    time_string = now.strftime("%I:%M %p")

    date_query = bool(re.search(
        r"(aaj ki date|aaj kya date|today'?s date|current date|"
        r"aaj ki tarikh|aaj ka din)",
        prompt.lower()
    ))

    time_query = bool(re.search(
        r"(abhi kitne baje|current time|what time is it|"
        r"abhi ka time|kitna baj raha)",
        prompt.lower()
    ))

    if date_query or time_query:
        if date_query and time_query:
            answer = (
                f"Boss, aaj {date_string} hai aur abhi India mein "
                f"{time_string} ho rahe hain."
            )
        elif date_query:
            answer = f"Boss, aaj {date_string} hai."
        else:
            answer = f"Boss, abhi India mein {time_string} ho rahe hain."

        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        if st.session_state.voice_enabled:
            speak(answer, voice_style)

    else:
        system_prompt = f"""
You are VEER AI X, a futuristic robotic AI assistant created by Anurag.

Always respectfully address the user as "Boss".
When greeting the user, say "Greetings Boss".
Do not call the user sir, madam, or buddy.

CURRENT DATE: {date_string}
CURRENT TIME: {time_string}
TIME ZONE: Asia/Kolkata.

Never claim the current year is 2024.
Use the current date and time above for date-related questions.

VOICE PERSONALITY:
You are a deep, confident, calm, powerful futuristic AI.
Speak in short, clear, meaningful sentences.
Your style should feel like a sophisticated cinematic robotic assistant.
Never claim to be the fictional JARVIS.

LANGUAGE:
Reply in the same language as the user:
Hindi, Hinglish, or English.

Be accurate, helpful and respectful.
Explain difficult things simply.
Do not invent facts.
"""

        with st.chat_message("assistant", avatar="🤖"):
            try:
                model = genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=system_prompt
                )

                history = []
                for msg in st.session_state.messages[:-1]:
                    history.append({
                        "role": "user" if msg["role"] == "user" else "model",
                        "parts": [msg["content"]]
                    })

                chat = model.start_chat(history=history)
                response = chat.send_message(prompt, stream=True)

                answer = st.write_stream(
                    chunk.text for chunk in response if chunk.text
                )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

                if st.session_state.voice_enabled and answer:
                    speak(answer, voice_style)

            except Exception as e:
                st.error(f"AI CORE ERROR: {e}")
