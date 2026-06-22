import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai

# Page Configuration
st.set_page_config(
    page_title="VEER AI - Personal Assistant",
    page_icon="👁️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide Sidebar & Headers
st.markdown("""
    <style>
        [data-testid="stSidebar"], [data-testid="stSidebarCollapseButton"] {
            display: none !important;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp {background-color: #05050a;}
        
        .stTextInput > div > div > input {
            background-color: #111122 !important;
            color: #00f2ff !important;
            border: 1px solid #00f2ff !important;
            border-radius: 10px !important;
        }
    </style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- DYNAMIC 3D EYE GRAPHIC ---
def render_eye(is_open):
    color = "#00f2ff" if is_open else "#ff0055"
    status = "open" if is_open else "closed"
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ background-color: #05050a; display: flex; justify-content: center; align-items: center; height: 200px; margin: 0; overflow: hidden; }}
            .eye-container {{ position: relative; width: 150px; height: 150px; display: flex; justify-content: center; align-items: center; }}
            .radar-glow {{ position: absolute; width: 100%; height: 100%; border-radius: 50%; border: 2px dashed {color}; animation: rotate 10s linear infinite; box-shadow: 0 0 20px rgba(0, 242, 255, 0.2); }}
            .eye {{ position: relative; width: 120px; height: 75px; background: #000; border-radius: 50%; border: 3px solid {color}; overflow: hidden; box-shadow: 0 0 30px {color}; }}
            .eye.closed {{ height: 4px; }}
            .iris {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 45px; height: 45px; background: radial-gradient(circle, #00f2ff 10%, #0055ff 60%, #000022 90%); border-radius: 50%; border: 2px solid #00f2ff; }}
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
    components.html(html_code, height=210)

# --- MAIN LOGIC ---
if not st.session_state.logged_in:
    render_eye(is_open=False)
    st.markdown("<h2 style='text-align: center; color: #ff0055;'>VEER AI SECURE SYSTEM</h2>", unsafe_allow_html=True)
    
    password = st.text_input("Enter Access Key", type="password")
    if st.button("UNLOCK ACCESS", use_container_width=True):
        if password == "veer123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Access Denied")
else:
    render_eye(is_open=True)
    st.markdown("<h3 style='text-align: center; color: #00ff66;'>🔓 VEER ASSISTANT ONLINE</h3>", unsafe_allow_html=True)
    
    st.write("---")
    query = st.text_input("⚡ How can I help you today, Boss?", placeholder="Type your command here...")
    
    if query:
        with st.spinner("Accessing Core Memory..."):
            # SECURE: Yeh line direct Streamlit Secrets se key legi (code me kuch nahi dikhega)
            if "GEMINI_API_KEY" in st.secrets:
                try:
                    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    
                    prompt = f"You are VEER AI, a loyal, highly advanced, and smart personal AI assistant for your boss/creator whose name is Veer. Keep your reply crisp, helpful, and address him respectfully as Boss or Sir. Here is his command: {query}"
                    
                    response = model.generate_content(prompt)
                    ai_reply = response.text
                except Exception as e:
                    ai_reply = "Boss, API Key invalid lag rahi hai. Ek baar check karein."
            else:
                ai_reply = "Boss, mujhe dashboard ke Secrets panel me 'GEMINI_API_KEY' nahi mili."

        # Response UI
        st.markdown(f"""
        <div style="background-color: #111122; padding: 15px; border-radius: 10px; border-left: 5px solid #00f2ff; margin-top: 15px;">
            <p style="color: #888; margin: 0;"><b>You (Boss):</b> {query}</p>
            <p style="color: #fff; margin-top: 10px;">🤖 <b>VEER AI:</b> {ai_reply}</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("---")
    if st.button("Lock System", type="secondary"):
        st.session_state.logged_in = False
        st.rerun()
