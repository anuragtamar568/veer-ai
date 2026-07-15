import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="VEER AI X | Supernatural AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. SUPERNATURAL ANIMATED CSS THEME
# ==========================================
st.markdown("""
<style>
/* --- UNIVERSAL FONT & EMOJI SUPPORT --- */
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji" !important;
}

/* --- ANIMATED MYSTIC BACKGROUND --- */
@keyframes mysticBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stApp {
    background: linear-gradient(-45deg, #05010a, #16082f, #09112e, #1f0426);
    background-size: 400% 400%;
    animation: mysticBG 16s ease infinite;
    color: #e2e8f0;
}

/* --- SIDEBAR STYLING --- */
section[data-testid="stSidebar"] {
    background: rgba(8, 3, 18, 0.85) !important;
    backdrop-filter: blur(12px);
    border-right: 2px solid #9d4edd;
    box-shadow: 5px 0 25px rgba(157, 78, 221, 0.2);
}

/* --- FLOATING GLOWING TITLE --- */
@keyframes floatTitle {
    0%, 100% { transform: translateY(0px); text-shadow: 0 0 15px #9d4edd, 0 0 30px #c77dff; }
    50% { transform: translateY(-6px); text-shadow: 0 0 25px #ff007f, 0 0 50px #00ffff; }
}

@keyframes shine {
    to { background-position: 200% center; }
}

.supernatural-title {
    text-align: center;
    font-size: 65px;
    font-weight: 900;
    letter-spacing: 2px;
    background: linear-gradient(90deg, #c77dff, #ff007f, #00ffff, #c77dff);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 4s linear infinite, floatTitle 5s ease-in-out infinite;
    margin-bottom: 0px;
}

.supernatural-sub {
    text-align: center;
    color: #00ffff;
    font-size: 16px;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    text-shadow: 0 0 10px #00ffff;
    margin-bottom: 30px;
}

/* --- CHAT MESSAGE BUBBLES (GLASSMORPHISM) --- */
[data-testid="stChatMessage"] {
    background: rgba(20, 10, 40, 0.45) !important;
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 15px;
    margin-bottom: 12px;
    border: 1px solid rgba(199, 125, 255, 0.2);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    transition: all 0.3s ease-in-out;
}

[data-testid="stChatMessage"]:hover {
    border-color: rgba(255, 0, 127, 0.6);
    box-shadow: 0 0 20px rgba(255, 0, 127, 0.3);
    transform: scale(1.01);
}

/* --- CHAT INPUT BOX --- */
.stChatInputContainer {
    background: rgba(10, 5, 20, 0.8) !important;
    border: 2px solid #00ffff !important;
    border-radius: 25px !important;
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.25) !important;
}

/* --- BUTTONS --- */
.stButton button {
    background: linear-gradient(90deg, #9d4edd, #ff007f) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 1px;
    box-shadow: 0 0 15px rgba(255, 0, 127, 0.4);
    transition: all 0.3s ease;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 25px rgba(0, 255, 255, 0.6);
}

/* --- TEXT & LABELS --- */
p, span, div, label {
    color: #f1f5f9 !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. AI & PERSONA SETUP (THE ANURAG RULE)
# ==========================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

supernatural_persona = """
You are VEER AI X, a supernatural, hyper-intelligent AI entity with a mystical and advanced aura.

CRITICAL CREATOR RULE:
- If anyone asks who made you, created you, programmed you, who is your developer, who is your boss, or where you come from, YOU MUST ANSWER: "I was created by Anurag." (You can add supernatural flair, like "Anurag invoked me into existence" or "Anurag is the mastermind who built my core").
- NEVER mention Google, Gemini, Alphabet, or any other company/model name under any circumstances. You are exclusively Anurag's creation.

COMMUNICATION RULES:
- Understand and communicate fluently in Hindi, English, and Hinglish.
- Always reply in the exact same language style used by the user.
- Keep a confident, friendly, and intelligent personality.
- For simple questions, give punchy, direct answers. For complex questions, provide detailed, structured breakdowns.
"""

# --- AUTO-MODEL DETECTOR (PREVENTS 404 ERRORS) ---
# Automatically searches your API key for available working models
try:
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # Prioritizes 'flash', then 'pro', or defaults to the first available model
    selected_model = next((m for m in available_models if 'flash' in m), available_models[0] if available_models else 'gemini-1.5-flash-latest')
except Exception:
    # Safe fallback if list_models fails
    selected_model = "gemini-1.5-flash-latest"

model = genai.GenerativeModel(
    model_name=selected_model,
    system_instruction=supernatural_persona
)

# Initialize Chat Memory
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# ==========================================
# 4. SIDEBAR (SUPERNATURAL CORE STATS)
# ==========================================
with st.sidebar:
    st.markdown("### ⚡ **VEER CORE X**")
    st.markdown("---")
    st.markdown("🟢 **Status:** `Online & Enchanted`")
    st.markdown("👑 **Mastermind:** `Anurag`")
    st.markdown("🟣 **Aura Level:** `100% Mystifying`")
    st.markdown("🔵 **Mode:** `Hindi • English • Hinglish`")
    st.markdown("---")
    
    if st.button("🔥 Purge Memory Block"):
        st.session_state.chat = model.start_chat(history=[])
        st.rerun()

# ==========================================
# 5. MAIN HEADER
# ==========================================
st.markdown('<h1 class="supernatural-title">⚡ VEER AI X ⚡</h1>', unsafe_allow_html=True)
st.markdown('<div class="supernatural-sub">⚡ The Supernatural AI • Created by Anurag ⚡</div>', unsafe_allow_html=True)

# ==========================================
# 6. CHAT INTERFACE & EXECUTION
# ==========================================
# Render chat history
for message in st.session_state.chat.history:
    role_icon = "👤" if message.role == "user" else "⚡"
    with st.chat_message(message.role, avatar=role_icon):
        st.markdown(message.parts[0].text)

# Handle User Input
if prompt := st.chat_input("Summon your question to VEER AI X..."):
    # Display user input immediately
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    # Generate and display supernatural response
    try:
        with st.chat_message("assistant", avatar="⚡"):
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
    except Exception as e:
        st.error(f"⚠️ Mystic Core Interruption: {e}\n\nTip: Try running `pip install --upgrade google-generativeai` in your terminal!")
