import streamlit as st
import streamlit.components.v1 as components
import random

# Page Configuration
st.set_page_config(
    page_title="VEER AI - Tactical Assistant",
    page_icon="👁️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

theme_color = "#00ff66" if st.session_state.logged_in else "#ff0055"

# Custom Cyberpunk Styles
st.markdown(f"""
    <style>
        [data-testid="stSidebar"], [data-testid="stSidebarCollapseButton"] {{ display: none !important; }}
        #MainMenu {{visibility: hidden;}} footer {{visibility: hidden;}} header {{visibility: hidden;}}
        .stApp {{ background-color: #020205 !important; }}
        h2, h3, p, span, label, div {{ color: {theme_color} !important; font-family: 'Courier New', Courier, monospace !important; }}
        .stTextInput > div > div > input {{ background-color: #051a05 !important; color: {theme_color} !important; border: 1px solid {theme_color} !important; }}
        .stButton>button {{ background-color: #051a05 !important; color: {theme_color} !important; border: 1px solid {theme_color} !important; }}
        .stButton>button:hover {{ background-color: {theme_color} !important; color: black !important; }}
    </style>
""", unsafe_allow_html=True)

# DYNAMIC EVIL EYE GRAPHIC
def render_eye(is_open):
    status = "open" if is_open else "closed"
    eye_color = "#00ff66" if is_open else "#ff0055"
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ background-color: #020205; display: flex; justify-content: center; align-items: center; height: 180px; margin: 0; overflow: hidden; }}
            .eye-container {{ position: relative; width: 140px; height: 140px; display: flex; justify-content: center; align-items: center; }}
            .radar-glow {{ position: absolute; width: 100%; height: 100%; border-radius: 50%; border: 2px dashed {eye_color}; animation: rotate 10s linear infinite; }}
            .eye {{ position: relative; width: 120px; height: 75px; background: #000; border-radius: 50%; border: 3px solid {eye_color}; overflow: hidden; box-shadow: 0 0 30px {eye_color}; transition: all 0.5s ease-in-out; }}
            .eye.closed {{ height: 4px; box-shadow: 0 0 15px #ff0055; border-color: #ff0055; }}
            .iris {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 45px; height: 45px; background: radial-gradient(circle, {eye_color} 10%, #0055ff 60%, #000022 90%); border-radius: 50%; border: 2px solid {eye_color}; box-shadow: 0 0 20px {eye_color}; }}
            .pupil {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 18px; height: 18px; background: #000; border-radius: 50%; }}
            @keyframes rotate {{ 100% {{ transform: rotate(360deg); }} }}
        </style>
    </head>
    <body>
        <div class="eye-container">
            <div class="radar-glow"></div>
            <div class="eye {status}">
                <div class="iris"><div class="pupil"></div></div>
            </div>
        </div>
    </body>
    </html>
    """
    components.html(html_code, height=190)

# MAIN INTERFACE
if not st.session_state.logged_in:
    render_eye(is_open=False)
    st.markdown("<h2 style='text-align: center;'>[ VEER A.I. SECURE SYSTEM ]</h2>", unsafe_allow_html=True)
    password = st.text_input("ENTER ACCESS KEY", type="password")
    if st.button("UNLOCK ASSISTANT"):
        if password == "veer123":
            st.session_state.logged_in = True
            st.session_state.ai_response_text = ""
            st.rerun()
        else:
            st.error("ACCESS DENIED")
else:
    render_eye(is_open=True)
    st.markdown("<h3 style='text-align: center;'>🔓 VEER A.I. ASSISTANT ONLINE</h3>", unsafe_allow_html=True)
    st.write("---")
    
    query = st.text_input("⚡ Tell me your command, Master Anurag...", placeholder="Type here...")

    voice_js = """
    <script>
    function startListening() {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-US';
        recognition.start();
        recognition.onresult = function(event) {
            const speechToText = event.results[0][0].transcript;
            const inputEl = parent.document.querySelector('input[type="text"]');
            if(inputEl) {
                inputEl.value = speechToText;
                inputEl.dispatchEvent(new Event('input', { bubbles: true }));
                inputEl.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }
    }
    </script>
    <div style="display:flex; gap:10px;"><button onclick="startListening()" style="background:#051a05; color:#00ff66; border:1px solid #00ff66; padding:10px; border-radius:5px; cursor:pointer;">🎙️ Tap to Speak (Suno)</button></div>
    """
    components.html(voice_js, height=50)

    if query:
        user_input = query.lower().strip()
        
        if "hello" in user_input or "hii" in user_input or "hey" in user_input:
            responses = [
                "Arey, Hello Master Anurag! My systems are fully operational.",
                "Greetings Sir. Secure link is stable. How can VEER assist you today?",
                "Online and ready, Anurag Boss! Give me your command."
            ]
            reply = random.choice(responses)
        elif "who are you" in user_input or "naam" in user_input:
            reply = "I am VEER A.I., your personal tactical assistant. Anurag Sir designed my mainframe."
        elif "owner" in user_input or "creator" in user_input or "master" in user_input or "banaya" in user_input:
            reply = "Mera dimaag aur pure core ko Anurag Master ne banaya hai, aur main unke exclusive service ke liye online hoon!"
        elif "veer" in user_input or "naam" in user_input:
            reply = "Arey Boss, Veer mera hi code naam hai. Mera full name VEER A.I. hai."
        else:
            reply = f"Command '{query}' analyzed. Ready for execution, Master Anurag!"

        st.session_state.ai_response_text = reply

        st.markdown(f"""
        <div style="background-color: #051a05; padding: 15px; border-radius: 10px; border: 1px solid #00ff66; margin-top: 15px;">
            <p style="margin: 0; color: #888;"><b>[COMMAND]:</b> {query}</p>
            <p style="margin-top: 10px; color: #00ff66;">🤖 <b>[VEER AI]:</b> {st.session_state.ai_response_text}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.ai_response_text:
            # Enhanced Voice Script with Speech Synthesis Voice Queuing Fix
            tts_js = f"""
            <script>
                window.speechSynthesis.cancel();
                
                function speak() {{
                    const speech = new SpeechSynthesisUtterance("{st.session_state.ai_response_text}");
                    const voices = window.speechSynthesis.getVoices();
                    
                    // Priority: Find an Indian English/Hindi voice for natural Hinglish accent
                    let targetVoice = voices.find(v => v.lang.includes('en-IN') || v.lang.includes('hi-IN'));
                    if (!targetVoice) {{
                        targetVoice = voices.find(v => v.name.includes('Google') || v.name.includes('Natural'));
                    }}
                    
                    if (targetVoice) speech.voice = targetVoice;
                    
                    speech.rate = 1.0;  // Normal human conversational speed
                    speech.pitch = 1.0; // Clear, natural voice pitch
                    window.speechSynthesis.speak(speech);
                }}

                if (window.speechSynthesis.getVoices().length !== 0) {{
                    speak();
                }} else {{
                    window.speechSynthesis.onvoiceschanged = speak;
                }}
            </script>
            """
            components.html(tts_js, height=1)

    st.write("---")
    if st.button("TERMINATE SESSION"):
        st.session_state.logged_in = False
        st.session_state.ai_response_text = ""
        st.rerun()
