import streamlit as st
import streamlit.components.v1 as components

# Page configuration (Yahan sidebar ko disabled rakha hai)
st.set_page_config(
    page_title="VEER AI - Gateway",
    page_icon="👁️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS se Streamlit ka default header aur menu chipana
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp {background-color: #05050a;}
    </style>
""", unsafe_allow_html=True)

# Session state login track karne ke liye
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- DYNAMIC 3D EYE GRAPHIC (HTML/CSS) ---
def render_eye(is_open):
    eye_status_class = "open" if is_open else "closed"
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                background-color: #05050a;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 280px;
                margin: 0;
                overflow: hidden;
            }}
            .eye-container {{
                position: relative;
                width: 220px;
                height: 220px;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            /* Futuristic Cyber Glow */
            .radar-glow {{
                position: absolute;
                width: 100%;
                height: 100%;
                border-radius: 50%;
                border: 2px dashed #00f2ff;
                animation: rotate 10s linear infinite;
                box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
            }}
            .eye {{
                position: relative;
                width: 160px;
                height: 100px;
                background: #000;
                border-radius: 50%;
                border: 3px solid #00f2ff;
                overflow: hidden;
                box-shadow: 0 0 30px rgba(0, 242, 255, 0.5);
                transition: all 0.8s ease-in-out;
            }}
            /* Eye State Logic */
            .eye.closed {{
                height: 4px;
                box-shadow: 0 0 15px #ff0055;
                border-color: #ff0055;
            }}
            .iris {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-30%, -50%);
                width: 65px;
                height: 65px;
                background: radial-gradient(circle, #00f2ff 10%, #0055ff 60%, #000022 90%);
                border-radius: 50%;
                border: 2px solid #00f2ff;
                box-shadow: 0 0 20px #00f2ff;
                animation: look around 4s infinite ease-in-out;
            }}
            .pupil {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 25px;
                height: 25px;
                background: #000;
                border-radius: 50%;
                box-shadow: inset 0 0 10px rgba(0,242,255,0.8);
            }}
            @keyframes rotate {{ 100% {{ transform: rotate(360deg); }} }}
        </style>
    </head>
    <body>
        <div class="eye-container">
            <div class="radar-glow"></div>
            <div class="eye {eye_status_class}">
                <div class="iris">
                    <div class="pupil"></div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    components.html(html_code, height=290)

# --- APP INTERFACE ---

if not st.session_state.
