import streamlit as st
import streamlit.components.v1 as components

# Page Configuration
st.set_page_config(
    page_title="VEER AI - Core Nexus",
    page_icon="👁️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

theme_color = "#00ff66" if st.session_state.logged_in else "#ff0055"

# --- FUTURISTIC CYBERPUNK TERMINAL STYLES ---
st.markdown(f"""
    <style>
        [data-testid="stSidebar"], [data-testid="stSidebarCollapseButton"] {{ display: none !important; }}
        #MainMenu {{visibility: hidden;}} footer {{visibility: hidden;}} header {{visibility: hidden;}}
        .stApp {{ background: radial-gradient(circle at center, #0a120a 0%, #020205 100%) !important; }}
        
        /* Neon Glow Text & Elements */
        h2, h3, p, span, label, div {{ 
            color: {theme_color} !important; 
            font-family: 'Courier New', Courier, monospace !important;
            text-shadow: 0 0 10px {theme_color}44;
        }}
        
        /* Input Terminal Styling */
        .stTextInput > div > div > input {{ 
            background-color: #031403 !important; 
            color: #00ff66 !important; 
            border: 2px solid #00ff66 !important; 
            box-shadow: 0 0 15px #00ff6622;
            border-radius: 8px !important;
            font-size: 16px !important;
        }}
        
        /* Masterpiece Hacker Buttons */
        .stButton>button {{ 
            background: linear-gradient(135deg, #051a05 0%, #0a2e0a 100%) !important; 
            color: {theme_color} !important; 
            border: 2px solid {theme_color} !important;
            border-radius: 8px !important;
            box-shadow: 0 0 10px {theme_color}22;
            font-weight: bold !important;
            letter-spacing: 2px;
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{ 
            background: {theme_color} !important; 
            color: black !important; 
            box-shadow: 0 0 25px {theme_color};
            transform: scale(1.02);
        }}
    </style>
""", unsafe_allow_html=True)

# --- DYNAMIC EVIL EYE GRAPHIC ---
def render_eye(is_open):
    status = "open" if is_open else "closed"
    eye_color = "#00ff66" if is_open else "#ff0055"
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ background: transparent; display: flex; justify-content: center; align-items: center; height: 180px; margin: 0; overflow: hidden; }}
            .eye-container {{ position: relative; width: 140px; height: 140px; display: flex; justify-content: center; align-items: center; }}
            .radar-glow {{ position: absolute; width: 100%; height: 100%; border-radius: 50%; border: 2px dashed {eye_color}; animation: rotate 12s linear infinite; }}
            .eye {{ position: relative; width: 125px; height: 75px; background: #000; border-radius: 50%; border: 3px solid {eye_color}; overflow: hidden; box-shadow: 0 0 35px {eye_color}; transition: all 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275); }}
            .eye.closed {{ height: 4px; box-shadow: 0 0 20px #ff0055; border-color: #ff0055; }}
            .iris {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 48px; height: 48px; background: radial-gradient(circle, {eye_color} 20%, #0033aa 60%, #000011 100%); border-radius: 50%; border: 2px solid {eye_color}; box-shadow: 0 0 25px {eye_color}; }}
            .pupil {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 20px; height: 20px; background: #000; border-radius: 50%; }}
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

# --- SYSTEM MAIN ROUTINE ---
if not st.session_state.logged_in:
    render_eye(is_open=False)
    st.markdown("<h2 style='text-align: center;'>⚡ [ VEER CORE MATRIX: LOCKED ] ⚡</h2>", unsafe_allow_html=True)
    password = st.text_input("ENTER DECRYPTION KEY", type="password")
    if st.button("BYPASS FIREWALL"):
        if password == "veer123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("ACCESS DENIED: FIREWALL SAFEGUARD ACTIVE")
else:
    render_eye(is_open=True)
    st.markdown("<h3 style='text-align: center;'>⚡ VEER MULTILINGUAL NEXUS ONLINE</h3>", unsafe_
