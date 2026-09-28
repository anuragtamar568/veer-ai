
import io
import json
import hashlib
import streamlit as st
import google.generativeai as genai
from PIL import Image

# =========================================================
# VEER AI X | JARVIS INSPIRED ROBOTIC AI
# =========================================================

st.set_page_config(
    page_title="VEER AI X | Robotic Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# 1. ROBOTIC THEME
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@400;500;600;700&display=swap');

:root {
    --cyan: #00eaff;
    --blue: #168bff;
    --deep: #030912;
    --line: rgba(0,234,255,.32);
}

.stApp {
    background:
        radial-gradient(ellipse at 50% -20%,
        rgba(0,110,160,.28), transparent 55%),
        linear-gradient(145deg,
        #02060d 0%, #061322 48%, #020711 100%);
    color: #dffaff;
}

header[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg, #04111f 0%, #020711 100%
    ) !important;
    border-right: 1px solid var(--line);
    box-shadow: 5px 0 28px rgba(0,234,255,.08);
}

h1, h2, h3, h4, p, label, span, div {
    font-family: 'Rajdhani', sans-serif;
}

.robot-title {
    font-family: 'Orbitron', sans-serif !important;
    text-align: center;
    font-weight: 900;
    font-size: clamp(32px, 5vw, 62px);
    letter-spacing: .13em;
    color: #dffcff;
    text-shadow:
        0 0 8px #00eaff,
        0 0 24px rgba(0,234,255,.7),
        0 0 48px rgba(22,139,255,.45);
    margin: 4px 0 0 0;
}

.robot-sub {
    font-family: 'Orbitron', sans-serif !important;
    text-align: center;
    color: #6eefff;
    letter-spacing: .18em;
    font-size: 11px;
    margin: 4px 0 20px 0;
}

.top-status {
    max-width: 760px;
    margin: 0 auto 22px auto;
    padding: 10px 16px;
    border: 1px solid var(--line);
    border-radius: 8px;
    background: linear-gradient(
        90deg,
        rgba(0,234,255,.04),
        rgba(0,110,255,.12),
        rgba(0,234,255,.04)
    );
    text-align: center;
    color: #9ff7ff;
    letter-spacing: .12em;
    font-family: 'Orbitron', sans-serif;
    font-size: 10px;
    box-shadow:
        inset 0 0 18px rgba(0,234,255,.05),
        0 0 20px rgba(0,234,255,.05);
}

.core-card {
    max-width: 850px;
    margin: 18px auto 26px auto;
    padding: 25px 24px;
    border: 1px solid rgba(0,234,255,.35);
    border-radius: 12px;
    background: linear-gradient(
        135deg,
        rgba(5,27,45,.92),
        rgba(3,10,22,.9)
    );
    box-shadow:
        inset 0 0 30px rgba(0,234,255,.035),
        0 0 28px rgba(0,145,255,.09);
    text-align: center;
    position: relative;
    overflow: hidden;
}

.core-card:before {
    content: "";
    position: absolute;
    left: 8%;
    right: 8%;
    top: 0;
    height: 1px;
    background: linear-gradient(
        90deg, transparent, #00eaff, transparent
    );
}

.core-heading {
    font-family: 'Orbitron', sans-serif;
    color: #00eaff;
    font-size: 20px;
    letter-spacing: .1em;
    text-shadow: 0 0 12px rgba(0,234,255,.5);
}

.core-copy {
    color: #c6eaf2;
    font-size: 18px;
    line-height: 1.5;
}

.core-chip {
    display: inline-block;
    margin: 6px 4px 0;
    padding: 5px 10px;
    border: 1px solid rgba(0,234,255,.3);
    border-radius: 4px;
    color: #86f5ff;
    font-family: 'Orbitron', sans-serif;
    font-size: 9px;
    letter-spacing: .08em;
    background: rgba(0,234,255,.05);
}

[data-testid="stChatMessage"] {
    background: rgba(4,19,34,.78) !important;
    border: 1px solid rgba(0,234,255,.2) !important;
    border-radius: 10px !important;
    box-shadow: 0 5px 22px rgba(0,0,0,.22);
    padding: 13px !important;
}

[data-testid="stChatMessage"]:hover {
    border-color: rgba(0,234,255,.55) !important;
    box-shadow: 0 0 20px rgba(0,234,255,.08);
}

.stChatInputContainer {
    border: 1px solid rgba(0,234,255,.55) !important;
    border-radius: 8px !important;
    background: rgba(2,12,24,.95) !important;
    box-shadow: 0 0 16px rgba(0,234,255,.09);
}

.stChatInputContainer textarea {
    color: #e6fcff !important;
}

.stButton button,
.stDownloadButton button {
    background: linear-gradient(
        100deg, #075a83, #087e9c
    ) !important;
    border: 1px solid #00dff5 !important;
    border-radius: 6px !important;
    color: #efffff !important;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 10px !important;
    letter-spacing: .06em;
    box-shadow: 0 0 12px rgba(0,234,255,.12);
}

.stButton button:hover,
.stDownloadButton button:hover {
    background: linear-gradient(
        100deg, #087e9c, #079eb8
    ) !important;
    box-shadow: 0 0 20px rgba(0,234,255,.3);
}

div[data-baseweb="select"] > div,
.stTextInput input {
    background: #071727 !important;
    border-color: rgba(0,234,255,.3) !important;
}

hr {
    border-color: rgba(0,234,255,.18) !important;
}

.small-label {
    color: #70cbd8;
    font-family: 'Orbitron', sans-serif;
    font-size: 10px;
    letter-spacing: .12em;
}

.voice-panel {
    border: 1px solid rgba(0,234,255,.24);
    border-radius: 7px;
    background: rgba(0,234,255,.035);
    padding: 9px 13px;
    color: #a9eaf2;
    font-size: 15px;
    margin: 10px 0;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# 2. JARVIS-INSPIRED VOICE SYSTEM
# =========================================================

def speak_text(text, voice_style="JARVIS Deep", language="Auto"):
    safe_text = json.dumps(str(text), ensure_ascii=False)
    safe_style = json.dumps(voice_style)
    safe_language = json.dumps(language)

    # Avoid Python f-string parsing of JavaScript braces.
    html = """
    <script>
    (() => {
        const text = __TEXT__;
        const style = __STYLE__;
        const language = __LANGUAGE__;

        if (!('speechSynthesis' in window) || !text) return;

        const synth = window.speechSynthesis;
        synth.cancel();

        const speak = () => {
            const voices = synth.getVoices();
            const u = new SpeechSynthesisUtterance(text);

            const langRegex =
                language === "Hindi" ? /^hi/i :
                language === "English" ? /^en/i : null;

            let candidates = langRegex
                ? voices.filter(v => langRegex.test(v.lang))
                : voices;

            if (!candidates.length) {
                candidates = voices;
            }

            const preferred =
                candidates.find(v =>
                    /Microsoft David|Google UK English Male|Daniel|Alex|Mark/i.test(v.name)
                )
                || candidates.find(v => /^en-US/i.test(v.lang))
                || candidates.find(v => /^en-IN/i.test(v.lang))
                || candidates.find(v => /^hi-IN/i.test(v.lang))
                || candidates[0];

            if (preferred) {
                u.voice = preferred;
            }

            if (style === "JARVIS Deep") {
                u.rate = 0.88;
                u.pitch = 0.62;
            }
            else if (style === "Robotic") {
                u.rate = 0.78;
                u.pitch = 0.48;
            }
            else if (style === "Calm AI") {
                u.rate = 0.92;
                u.pitch = 0.82;
            }
            else {
                u.rate = 1.0;
                u.pitch = 1.0;
            }

            u.volume = 1.0;
            synth.speak(u);
        };

        if (synth.getVoices().length) {
            speak();
        }
        else {
            synth.onvoiceschanged = () => {
                synth.onvoiceschanged = null;
                speak();
            };
        }
    })();
    </script>
    """

    html = html.replace("__TEXT__", safe_text)
    html = html.replace("__STYLE__", safe_style)
    html = html.replace("__LANGUAGE__", safe_language)

    st.components.v1.html(html, height=0)


# =========================================================
# 3. GEMINI AI CONFIGURATION
# =========================================================

api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.error(
        "GEMINI_API_KEY missing hai. "
        "Streamlit secrets mein API key add karein."
    )
    st.stop()

genai.configure(api_key=api_key)


# =========================================================
# 4. SIDEBAR CONTROL PANEL
# =========================================================

with st.sidebar:

    st.markdown("## 🤖 VEER AI X")

    st.markdown(
        '<div class="small-label">ROBOTIC INTELLIGENCE CORE</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("**SYSTEM STATUS**")
    st.success("ONLINE • ALL SYSTEMS READY")

    st.markdown("**CREATOR**")
    st.caption("ANURAG")

    st.markdown("**LANGUAGE MODULES**")
    st.caption("HINDI • ENGLISH • HINGLISH")

    st.divider()

    aura_mood = st.selectbox(
        "AI PERSONALITY",
        [
            "JARVIS Assistant",
            "Mystical & Friendly",
            "Dark & Spooky",
            "Sarcastic & Funny"
        ],
    )

    model_options = [
        "gemini-2.5-flash",
        "gemini-1.5-flash",
        "gemini-1.5-pro"
    ]

    selected_model = st.selectbox(
        "AI ENGINE",
        model_options,
        index=0
    )

    voice_enabled = st.toggle(
        "🔊 AI VOICE REPLY",
        value=True
    )

    voice_style = st.selectbox(
        "VOICE PROFILE",
        [
            "JARVIS Deep",
            "Robotic",
            "Calm AI",
            "Natural"
        ],
        index=0
    )

    voice_language = st.selectbox(
        "VOICE LANGUAGE",
        ["Auto", "Hindi", "English"],
        index=0
    )

    st.caption(
        "Actual voice Chrome/Windows ke installed voices par depend karti hai."
    )

    st.divider()

    if st.button(
        "🧹 CLEAR CHAT MEMORY",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.session_state.suggested_prompt = None
        st.session_state.last_voice_hash = None
        st.rerun()

    if st.button(
        "🔊 TEST AI VOICE",
        use_container_width=True
    ):
        speak_text(
            "Hello Anurag. VEER AI X systems are online. How may I assist you today?",
            voice_style,
            voice_language
        )

    st.divider()

    st.markdown("### 📡 CORE READOUT")

    st.caption(
        "VOICE MODULE: " +
        ("ACTIVE" if voice_enabled else "STANDBY")
    )

    st.caption("VISUAL INTERFACE: ONLINE")
    st.caption("MEMORY BUFFER: SESSION")


# =========================================================
# 5. SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "suggested_prompt" not in st.session_state:
    st.session_state.suggested_prompt = None

if "voice_input_counter" not in st.session_state:
    st.session_state.voice_input_counter = 0


# =========================================================
# 6. MAIN HEADER
# =========================================================

st.markdown(
    '<div class="robot-title">VEER AI X</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="robot-sub">'
    'ADVANCED ROBOTIC INTELLIGENCE • VOICE INTERFACE'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="top-status">'
    '● SYSTEM ONLINE &nbsp; | &nbsp; NEURAL CORE ACTIVE '
    '&nbsp; | &nbsp; CREATOR: ANURAG'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# 7. WELCOME SCREEN
# =========================================================

if not st.session_state.messages:

    st.markdown("""
    <div class="core-card">
        <div class="core-heading">🤖 SYSTEM INITIALIZED</div>

        <div class="core-copy">
            Greetings, Anurag. I am <b>VEER AI X</b>,
            your personal AI assistant.
            Voice interface and neural response core are ready.
            Ask a question in Hindi, English, or Hinglish.
        </div>

        <div style="margin-top:15px">
            <span class="core-chip">VOICE ENABLED</span>
            <span class="core-chip">MULTILINGUAL CORE</span>
            <span class="core-chip">IMAGE MODULE</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button(
            "🧠 Explain a topic",
            use_container_width=True
        ):
            st.session_state.suggested_prompt = (
                "Explain artificial intelligence in simple Hinglish."
            )
            st.rerun()

    with c2:
        if st.button(
            "⚙️ System capabilities",
            use_container_width=True
        ):
            st.session_state.suggested_prompt = (
                "Tell me your capabilities in a concise list."
            )
            st.rerun()

    with c3:
        if st.button(
            "🎨 Create futuristic art",
            use_container_width=True
        ):
            st.session_state.suggested_prompt = (
                "Create an image of a futuristic blue robotic AI assistant interface."
            )
            st.rerun()


# =========================================================
# 8. CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    avatar = (
        "⚡"
        if message["role"] == "user"
        else "🤖"
    )

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):
        st.markdown(message["content"])

        if message.get("image") is not None:
            st.image(
                message["image"],
                use_container_width=True
            )


# =========================================================
# 9. VOICE INPUT
# =========================================================

st.markdown(
    '<div class="voice-panel">'
    '🎙️ <b>VOICE INPUT MODULE</b> — Mic se Hindi, English '
    'ya Hinglish mein bolkar sawal poochhein.'
    '</div>',
    unsafe_allow_html=True
)

voice_audio = st.audio_input(
    "🎙️ Speak to VEER AI X",
    key=f"voice_input_{st.session_state.voice_input_counter}",
)

active_prompt = st.session_state.suggested_prompt
st.session_state.suggested_prompt = None

if voice_audio is not None:

    audio_bytes = voice_audio.getvalue()

    audio_hash = hashlib.sha256(
        audio_bytes
    ).hexdigest()

    if st.session_state.get("last_voice_hash") != audio_hash:

        st.session_state.last_voice_hash = audio_hash

        try:
            audio_part = {
                "mime_type": voice_audio.type or "audio/wav",
                "data": audio_bytes,
            }

            transcriber = genai.GenerativeModel(
                model_name=selected_model
            )

            transcription = transcriber.generate_content([
                "Understand the user's audio and return ONLY "
                "the spoken request as text. The speech may be "
                "Hindi, English, or Hinglish.",
                audio_part,
            ])

            spoken_text = (
                transcription.text or ""
            ).strip()

            if spoken_text:
                active_prompt = spoken_text
                st.session_state.voice_input_counter += 1

            else:
                st.warning(
                    "Awaaz samajh nahi aayi. Dobara try karein."
                )

        except Exception as exc:
            st.error(f"Voice input error: {exc}")


# =========================================================
# 10. TEXT INPUT
# =========================================================

if active_prompt is None:

    active_prompt = st.chat_input(
        "Type your command to VEER AI X..."
    )


# =========================================================
# 11. AI RESPONSE ENGINE
# =========================================================

if active_prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": active_prompt
    })

    with st.chat_message(
        "user",
        avatar="⚡"
    ):
        st.markdown(active_prompt)

    image_triggers = [
        "generate image",
        "create image",
        "create a photo",
        "draw",
        "visualize",
        "make an image",
        "image banao",
        "photo banao",
        "tasveer banao"
    ]

    prompt_lower = active_prompt.lower()

    is_image_request = any(
        word in prompt_lower
        for word in image_triggers
    )

    tone_modifier = {
        "JARVIS Assistant":
            "You are VEER AI X, a polished, concise, "
            "highly capable futuristic assistant inspired "
            "by cinematic AI assistants. Speak respectfully "
            "and clearly. Do not claim to be the fictional JARVIS.",

        "Mystical & Friendly":
            "Be friendly, confident, slightly mystical, and helpful.",

        "Dark & Spooky":
            "Use a mysterious, gothic, slightly eerie style "
            "while remaining helpful.",

        "Sarcastic & Funny":
            "Be witty, playful, and lightly sarcastic "
            "without being rude.",
    }[aura_mood]

    system_prompt = f"""
You are VEER AI X, an AI assistant created for Anurag.

{tone_modifier}

Communicate in the same language style as the user:
Hindi, English, or Hinglish.

Give accurate, useful, easy-to-understand answers.
Use steps when helpful.
Do not invent facts. If uncertain, say so.
"""


    # =====================================================
    # 12. IMAGE GENERATION
    # =====================================================

    if is_image_request:

        with st.chat_message(
            "assistant",
            avatar="🤖"
        ):

            try:
                st.markdown(
                    "**VISUAL CORE:** Image generation request received."
                )

                image_model_class = getattr(
                    genai,
                    "ImageGenerationModel",
                    None
                )

                if image_model_class is None:
                    raise RuntimeError(
                        "Installed google-generativeai SDK does not "
                        "expose ImageGenerationModel. A compatible "
                        "image-generation API/SDK is required."
                    )

                image_model = image_model_class(
                    "imagen-3.0-generate-002"
                )

                result = image_model.generate_images(
                    prompt=active_prompt,
                    number_of_images=1,
                    aspect_ratio="1:1",
                )

                image_bytes = (
                    result.images[0].image.image_bytes
                )

                generated_image = Image.open(
                    io.BytesIO(image_bytes)
                )

                confirmation = (
                    f"Visual core completed: {active_prompt}"
                )

                st.markdown(confirmation)

                st.image(
                    generated_image,
                    use_container_width=True
                )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": confirmation,
                    "image": generated_image,
                })

                if voice_enabled:
                    speak_text(
                        confirmation,
                        voice_style,
                        voice_language
                    )

            except Exception as exc:

                error_text = (
                    f"Image generation unavailable: {exc}"
                )

                st.error(error_text)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_text
                })


    # =====================================================
    # 13. NORMAL AI CHAT
    # =====================================================

    else:

        with st.chat_message(
            "assistant",
            avatar="🤖"
        ):

            try:
                model = genai.GenerativeModel(
                    model_name=selected_model,
                    system_instruction=system_prompt,
                )

                history = []

                for item in st.session_state.messages[:-1]:

                    history.append({
                        "role": (
                            "user"
                            if item["role"] == "user"
                            else "model"
                        ),
                        "parts": [item["content"]],
                    })

                chat = model.start_chat(
                    history=history
                )

                response = chat.send_message(
                    active_prompt,
                    stream=True
                )

                def stream_text():
                    for chunk in response:
                        if getattr(chunk, "text", None):
                            yield chunk.text

                full_response = st.write_stream(
                    stream_text()
                )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_response,
                })

                if voice_enabled and full_response:
                    speak_text(
                        full_response,
                        voice_style,
                        voice_language
                    )

            except Exception as exc:
                st.error(
                    f"AI core error: {exc}"
                )


# =========================================================
# 14. CHAT ARCHIVE
# =========================================================

if st.session_state.messages:

    with st.sidebar:

        st.divider()

        st.markdown("### 📜 CHAT ARCHIVE")

        archive = ""

        for item in st.session_state.messages:

            who = (
                "ANURAG"
                if item["role"] == "user"
                else "VEER AI X"
            )

            archive += (
                f"[{who}]\n"
                f"{item['content']}\n\n"
                f"{'-' * 36}\n\n"
            )

        st.download_button(
            "⬇ DOWNLOAD CHAT LOG",
            data=archive,
            file_name="veer_ai_x_chat.txt",
            mime="text/plain",
            use_container_width=True,
        )
