import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai

# 1. Page configuration
st.set_page_config(
    page_title="VEER AI - Gateway",
    page_icon="👁️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Gemini AI Configuration (Yahan apni API key daal sakte hain, ya direct chalane ke liye backup code hai)
# Tip: Streamlit secrets me GEMINI_API_KEY set karna sabse best hota hai
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    # Agar key nahi milti to user se input lene ka option de rahe hain backend me
    genai.configure(api_key="YOUR_GEMINI_API_KEY_HERE")

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
    st.markdown("<h3 style='text-align: center; color: #00ff66;'>🔓 SYSTEM ONLINE</h3>", unsafe_allow_html=True)
    
    st.write("---")
    query = st.text_input("🤖 Ask VEER AI anything...", placeholder="Type your question here...")
    
    if query:
        with st.spinner("VEER AI is thinking..."):
            try:
                # Gemini Model se response generate karna
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(query)
                ai_reply = response.text
            except Exception as e:
                ai_reply = "Sir, please make sure your Gemini API Key is configured correctly in Streamlit Secrets."

        # Response UI
        st.markdown(f"""
        <div style="background-color: #111122; padding: 15px; border-radius: 10px; border-left: 5px solid #00f2ff; margin-top: 15px;">
            <p style="color: #888; margin: 0;"><b>You:</b> {query}</p>
            <p style="color: #fff; margin-top: 10px;">🤖 <b>VEER AI:</b> {ai_reply}</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("---")
    if st.button("Lock System", type="secondary"):
        st.session_state.logged_in = False
        st.rerun()
