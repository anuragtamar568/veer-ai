import streamlit as st
import streamlit.components.v1 as components
import random

# Page Configuration - Sidebar disabled, layout centered
st.set_page_config(
    page_title="VEER AI - Tactical Assistant",
    page_icon="👁️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 1. Hide Sidebar, Headers & Set Dynamic Hacker Colors (Green/Red based on status)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

theme_color = "#00ff66" if st.session_state.logged_in else "#ff0055" # Green=Online, Red=Locked

st.markdown(f"""
    <style>
        [data-testid="stSidebar"], [data-testid="stSidebarCollapseButton"] {{ display: none !important; }}
        #MainMenu {{visibility: hidden;}} footer {{visibility: hidden;}} header {{visibility: hidden;}}
        .stApp {{ background-color: #020205 !important; }}
        
        /* Unified Hacker Text Colors */
        h2, h3, p, span, label, div {{ color: {theme_color} !important; font-family: 'Courier New', Courier, monospace !important; }}
        
        /* Input & Button Styling (Matching Theme) */
        .stTextInput > div > div > input {{ background-color: #051a05 !important; color: {theme_color} !important; border: 1px solid {theme_color} !important; }}
        .stButton>button {{ background-color: #051a05 !important; color: {theme_color} !important; border: 1px solid {theme_color} !important; }}
        .stButton>button:hover {{ background-color: {theme_color} !important; color: black !important; }}
    </style>
""", unsafe_allow_html=True)

# 2. DYNAMIC EVIL EYE GRAPHIC (HTML/CSS) - Changes state on login
def render_eye(is_open):
    # If open, green glowing cyber eye; if closed, red secure line.
    status = "open" if is_open else "closed"
    eye_color = "#00ff66" if is_open else "#ff0055"
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ background-color: #020205; display: flex; justify-content: center; align-items: center; height: 180px; margin: 0; overflow: hidden; }}
            .eye-container {{ position: relative; width: 140px; height: 140px; display: flex; justify-content: center; align-items: center; }}
            .radar-glow {{ position: absolute; width: 100%; height: 100%; border-radius: 50%; border: 2px dashed {eye_color}; animation: rotate 10s linear infinite; box-shadow: 0 0 20px rgba({f"{eye_color[1:3]},{eye_color[3:5]},{eye_color[5:7]}"}, 0.2); }}
            
            /* Evil Eye Base */
            .eye {{ position: relative; width: 120px; height: 75px; background: #000; border-radius: 50%; border: 3px solid {eye_color}; overflow: hidden; box-shadow: 0 0 30px {eye_color}; transition: all 0.5s ease-in-out; }}
            
            /* Secure State (Closed) - Like image_1.png */
            .eye.closed {{ height: 4px; box-shadow: 0 0 15px #ff0055; border-color: #ff0055; }}
            
            /* Active State (Open) - Detailed Cyber Eye */
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

# --- APP MAIN INTERFACE ---

if not st.session_state.logged_in:
    # 3. Locked State: Closed Red Eye
    render_eye(is_open=False)
    st.markdown("<h2 style='text-align: center; color: #ff0055 !important;'>[ VEER A.I. SECURE SYSTEM ]</h2>", unsafe_allow_html=True)
    
    password = st.text_input("ENTER ACCESS KEY", type="password")
    
    if st.button("UNLOCK ASSISTANT"):
        if password == "veer123":
            st.session_state.logged_in = True
            st.session_state.ai_response_text = "" # Reset chat on login
            st.rerun()
        else:
            st.error("ACCESS DENIED: INTTRUSION DETECTED")

else:
    # 4. Unlocked State: Open Green Evil Eye
    render_eye(is_open=True)
    st.markdown("<h3 style='text-align: center; color: #00ff66 !important;'>🔓 VEER A.I. ASSISTANT ONLINE</h3>", unsafe_allow_html=True)
    
    st.write("---")
    query = st.text_input("⚡ Tell me your command, Master Anurag...", placeholder="Type here...")

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
