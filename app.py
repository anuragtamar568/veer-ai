import streamlit as st
import streamlit.components.v1 as components
import random

# Page Configuration
st.set_page_config(
    page_title="VEER AI - Hacker Terminal",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- MATRIX HACKER BACKGROUND ---
hacker_ui = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background: black; font-family: 'Courier New', Courier, monospace; }
        canvas { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1; opacity: 0.35; }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>
    <script>
        const canvas = document.getElementById('matrix');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        const katakana = 'ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        const alphabet = katakana.split('');
        const fontSize = 16;
        const columns = canvas.width / fontSize;
        const rainDrops = [];
        for (let x = 0; x < columns; x++) { rainDrops[x] = 1; }
        const draw = () => {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#0F0';
            ctx.font = fontSize + 'px monospace';
            for (let i = 0; i < rainDrops.length; i++) {
                const text = alphabet[Math.floor(Math.random() * alphabet.length)];
                ctx.fillText(text, i * fontSize, rainDrops[i] * fontSize);
                if (rainDrops[i] * fontSize > canvas.height && Math.random() > 0.975) { rainDrops[i] = 0; }
                rainDrops[i]++;
            }
        };
        setInterval(draw, 30);
    </script>
</body>
</html>
"""
components.html(hacker_ui, height=1, scrolling=False)

# Custom Cyberpunk Styles
st.markdown("""
    <style>
        [data-testid="stSidebar"], [data-testid="stSidebarCollapseButton"] { display: none !important; }
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
        .stApp { background-color: #020205 !important; }
        h2, h3, p, span, label { color: #00ff66 !important; font-family: 'Courier New', Courier, monospace !important; }
        .stTextInput > div > div > input { background-color: #051a05 !important; color: #00ff66 !important; border: 1px solid #00ff66 !important; font-family: 'Courier New', Courier, monospace !important; }
        .stButton>button { background-color: #051a05 !important; color: #00ff66 !important; border: 1px solid #00ff66 !important; }
        .stButton>button:hover { background-color: #00ff66 !important; color: black !important; }
    </style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "ai_response_text" not in st.session_state:
    st.session_state.ai_response_text = ""

# --- LOGIN ---
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center;'>[ VEER MAINMAINFRAME ACCESS ]</h2>", unsafe_allow_html=True)
    password = st.text_input("ENTER ACCESS ENCRYPTION KEY", type="password")
    if st.button("EXECUTE BYPASS"):
        if password == "veer123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("ACCESS DENIED")
else:
    st.markdown("<h2 style='text-align: center;'>💻 VEER CYBER SYSTEM ONLINE</h2>", unsafe_allow_html=True)
    query = st.text_input("⌨️ Terminal Command:", placeholder="Type here, Boss...")

    # Voice Input JS
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
        
        # Natural Human-Like Responses with Creator Recognition
        if "hello" in user_input or "hii" in user_input or "hey" in user_input:
            responses = [
                "Arey, Hello Boss! VEER A.I. is fully active. Sab mast chal raha hai, tell me your command.",
                "Greetings Sir! Mainframe secure hai. Aaj kya faddna hai, batao?",
                "Yo Boss! Systems are 100 percent online. Ready for your orders."
            ]
            st.session_state.ai_response_text = random.choice(responses)
            
        elif "who are you" in user_input or "naam" in user_input:
            st.session_state.ai_response_text = "I am VEER A.I., your personal tactical assistant. Mujhe Anurag ne banaya hai exclusive aapke liye, Boss!"
            
        elif "owner" in user_input or "boss" in user_input or "creator" in user_input or "banaya" in user_input:
            st.session_state.ai_response_text = "Mera dimaag aur ye poora mainframe system Anurag ne design kiya hai, aur mera commander sirf aap hain—Veer Sir!"
            
        else:
            st.session_state.ai_response_text = f"Understood Boss. Command '{query}' is being executed. Give me a second!"

        # Display Output
        st.markdown(f"""
        <div style="background-color: #051a05; padding: 15px; border-radius: 10px; border: 1px solid #00ff66; margin-top: 15px;">
            <p style="margin: 0; color: #888;"><b>[COMMAND]:</b> {query}</p>
            <p style="margin-top: 10px; color: #00ff66;">🤖 <b>[VEER AI]:</b> {st.session_state.ai_response_text}</p>
        </div>
        """, unsafe_allow_html=True)

        # --- NATURAL VOICE SPEECHES CONTROL (JS) ---
        if st.session_state.ai_response_text:
            tts_js = f"""
            <script>
                window.speechSynthesis.cancel(); 
                const speech = new SpeechSynthesisUtterance("{st.session_state.ai_response_text}");
                
                const voices = window.speechSynthesis.getVoices();
                const naturalVoice = voices.find(v => v.name.includes('Natural') || v.name.includes('Google US English')) || voices[0];
                if (naturalVoice) speech.voice = naturalVoice;
                
                speech.lang = 'en-US';
                speech.rate = 1.05;  
                speech.pitch = 0.95; 
                
                window.speechSynthesis.speak(speech);
            </script>
            """
            components.html(tts_js, height=1)

    st.write("---")
    if st.button("TERMINATE SESSION"):
        st.session_state.logged_in = False
        st.session_state.ai_response_text = ""
        st.rerun()
