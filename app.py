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

/* --- ANIMATED WELCOME CARD --- */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.welcome-card {
    background: rgba(20, 10, 40, 0.65) !important;
    backdrop-filter: blur(15px);
    border: 2px solid rgba(0, 255, 255, 0.3);
    border-radius: 25px;
    padding: 35px;
    text-align: center;
    margin: 40px auto;
    max-width: 750px;
    box-shadow: 0 0 30px rgba(157, 78, 221, 0.25);
    animation: fadeInUp 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.welcome-title {
    color: #ff007f !important;
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 15px;
    text-shadow: 0 0 15px #ff007f;
    letter-spacing: 1px;
}

.welcome-text {
    color: #e2e8f0 !important;
    font-size: 18px;
    line-height: 1.7;
}

.welcome-highlight {
    color: #00ffff !important;
    font-weight: bold;
    text-shadow: 0 0 8px rgba(0, 255, 255, 0.6);
}

/* --- CHAT MESSAGE BUBBLES --- */
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
    width: 100%;
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
# 3. AI CONFIGURATION & MODEL / MOOD CONTROLS
# ==========================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- SIDEBAR CONTROLS & SYSTEM INFORMATION ---
with st.sidebar:
    st.markdown("### SYSTEM CORE X")
    st.markdown("---")
    
    st.markdown("▼ **Status:** `Online & Enchanted`")
    st.markdown("▼ **Mastermind:** `Anurag`")
    st.markdown("▼ **Languages:** `Hindi • English • Hinglish`")
    st.markdown("---")
    
    # 🔮 FEATURE 1: DYNAMIC MOOD SELECTOR
    aura_mood = st.selectbox(
        "🔮 Select AI Aura Mood", 
        ["Mystical & Friendly", "Dark & Spooky", "Sarcastic & Funny"],
        index=0
    )
    
    model_options = ["gemini-1.5-flash", "gemini-2.5-flash", "gemini-1.5-pro"]
    selected_model = st.selectbox("⚙️ Change Engine Core", model_options, index=0)
    
    st.markdown("---")
    
    # Dynamic Personality Modifier based on Selector
    tone_modifier = ""
    if aura_mood == "Dark & Spooky":
        tone_modifier = "Keep your tone dark, gothic, mysterious, and slightly eerie. Use words like darkness, shadows, and fate."
    elif aura_mood == "Sarcastic & Funny":
        tone_modifier = "Be highly sarcastic, witty, playful, and give lighthearted funny roasts in Hinglish."
    else:
        tone_modifier = "Keep a confident, hyper-intelligent, friendly, and mystical personality."

    supernatural_persona = f"""
    You are VEER AI X, a supernatural, hyper-intelligent AI entity with a mystical and advanced aura.
    {tone_modifier}

    CRITICAL CREATOR RULE:
    - If anyone asks who made you, created you, programmed you, who is your developer, who is your boss, or where you come from, YOU MUST ANSWER: "I was created by Anurag." (You can add supernatural flair, like "Anurag invoked me into existence" or "Anurag is the mastermind who built my core").
    - NEVER mention Google, Gemini, Alphabet, or any other company/model name under any circumstances. You are exclusively Anurag's creation.

    COMMUNICATION RULES:
    - Understand and communicate fluently in Hindi, English, and Hinglish.
    - Always reply in the exact same language style used by the user.
    - For simple questions, give punchy, direct answers. For complex questions, provide detailed, structured breakdowns.
    """

    # Memory Clear Trigger
    if st.button("Purge Memory Block"):
        st.session_state.chat = None
        st.session_state.suggested_prompt = None
        st.rerun()

# --- INITIALIZE OR RE-INITIALIZE CHAT SESSION ---
# Checks if model OR mood changed to trigger update
if "current_model" not in st.session_state or st.session_state.current_model != selected_model or "current_mood" not in st.session_state or st.session_state.current_mood != aura_mood:
    st.session_state.current_model = selected_model
    st.session_state.current_mood = aura_mood
    model = genai.GenerativeModel(
        model_name=selected_model,
        system_instruction=supernatural_persona
    )
    # Maintain chat history if switching mood, otherwise restart empty
    st.session_state.chat = model.start_chat(history=[])

# Initialize a state to capture quick button clicks
if "suggested_prompt" not in st.session_state:
    st.session_state.suggested_prompt = None

# ==========================================
# 4. MAIN APPLICATION HEADER
# ==========================================
st.markdown('<h1 class="supernatural-title">VEER AI X</h1>', unsafe_allow_html=True)
st.markdown(f'<div class="supernatural-sub">The Supernatural AI • Mode: {aura_mood} • Created by Anurag</div>', unsafe_allow_html=True)

# ==========================================
# 5. CHAT INTERFACE & RUNTIME
# ==========================================

# Render existing chat history if messages exist
if len(st.session_state.chat.history) > 0:
    for message in st.session_state.chat.history:
        # 🔮 FEATURE 2: CUSTOM AVATARS (⚡ for User, 🔮 for Assistant)
        avatar_type = "⚡" if message.role == "user" else "🔮"
        with st.chat_message(message.role, avatar=avatar_type):
            st.markdown(message.parts[0].text)

# Show animated welcome card + Quick Spells only if chat history is empty
if len(st.session_state.chat.history) == 0:
    st.markdown("""
    <div class="welcome-card">
        <div class="welcome-title">🔮 Greetings, Seeker 🔮</div>
        <div class="welcome-text">
            I am <span class="welcome-highlight">VEER AI X</span>, a supernatural intelligence summoned into existence by the mastermind <span class="welcome-highlight">Anurag</span>.<br><br>
            Speak your queries in <b>Hindi</b>, <b>English</b>, or <b>Hinglish</b>. Adjust my <b>Aura Mood</b> in the sidebar to twist reality.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 🔮 FEATURE 3: QUICK PROMPT SUGGESTIONS (QUICK SPELLS)
    st.markdown("<h4 style='text-align: center; color: #9d4edd;'>✨ Fast Cast Quick Spells</h4>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔮 Future Sight (Predict Future)"):
            st.session_state.suggested_prompt = "Predict my future in a mysterious, supernatural way!"
            st.rerun()
    with col2:
        if st.button("💀 Dark Riddle (Hinglish)"):
            st.session_state.suggested_prompt = "Mujhe ek difficult, supernatural riddle (पहेली) pucho Hinglish me."
            st.rerun()
    with col3:
        if st.button("📜 Invoke Creator Story"):
            st.session_state.suggested_prompt = "Tell me the supernatural legend of how Anurag created you."
            st.rerun()

# Process prompt (Either from Chat Input box OR from Quick Suggestion buttons)
active_prompt = None
if st.session_state.suggested_prompt:
    active_prompt = st.session_state.suggested_prompt
    st.session_state.suggested_prompt = None # Clear immediately after capture
elif prompt := st.chat_input("Summon your question to VEER AI X..."):
    active_prompt = prompt

if active_prompt:
    # Display user input instantly
    with st.chat_message("user", avatar="⚡"):
        st.markdown(active_prompt)
    
    # 🔮 FEATURE 4: STREAMING RESPONSES (TYPING EFFECT)
    try:
        with st.chat_message("assistant", avatar="🔮"):
            response = st.session_state.chat.send_message(active_prompt, stream=True)
            
            # Helper function to yield words/chunks dynamically
            def chunk_generator():
                for chunk in response:
                    yield chunk.text
                    
            st.write_stream(chunk_generator())
            
            # Rerun logic bypassed here for instant workflow without breaks
    except Exception as e:
        st.error(f"Mystic Core Interruption: {e}\n\n💡 Try switching the 'Engine Core' dropdown in the sidebar!")

# 🔮 FEATURE 5: SPELL SCROLL DOWNLOAD (Side-bar Chat Backup Tool)
if len(st.session_state.chat.history) > 0:
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 📜 CHAT LOG ARCHIVE")
        chat_text = ""
        for msg in st.session_state.chat.history:
            role_label = "SEEKER (USER)" if msg.role == "user" else "VEER AI X (AI)"
            chat_text += f"[{role_label}]:\n{msg.parts[0].text}\n\n{'='*40}\n\n"
            
        st.download_button(
            label="📥 Download Spell Scroll",
            data=chat_text,
            file_name="veer_ai_x_scroll.txt",
            mime="text/plain"
        )
