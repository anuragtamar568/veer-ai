import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

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
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
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

/* --- MYSTICAL NEON IMAGE FRAME --- */
@keyframes imageGlow {
    0%, 100% { box-shadow: 0 0 20px rgba(157, 78, 221, 0.5); border-color: #9d4edd; }
    50% { box-shadow: 0 0 40px rgba(0, 255, 255, 0.8); border-color: #00ffff; }
}

.mystic-image-container {
    border: 3px solid #00ffff;
    border-radius: 20px;
    padding: 12px;
    background: rgba(10, 5, 20, 0.7);
    animation: imageGlow 4s ease-in-out infinite;
    margin-top: 15px;
    max-width: 500px;
}

/* --- CHAT INPUT BOX (NEON PULSE) --- */
@keyframes inputPulse {
    0%, 100% { border-color: #00ffff; box-shadow: 0 0 10px rgba(0, 255, 255, 0.3); }
    50% { border-color: #ff007f; box-shadow: 0 0 20px rgba(255, 0, 127, 0.6); }
}

.stChatInputContainer {
    background: rgba(10, 5, 20, 0.8) !important;
    border: 2px solid #00ffff !important;
    border-radius: 25px !important;
    animation: inputPulse 3.5s ease-in-out infinite;
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

p, span, div, label {
    color: #f1f5f9 !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. AI CONFIGURATION & SIDEBAR MODE CONTROLS
# ==========================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

with st.sidebar:
    st.markdown("### SYSTEM CORE X")
    st.markdown("---")
    st.markdown("▼ **Status:** `Online & Enchanted`")
    st.markdown("▼ **Mastermind:** `Anurag`")
    st.markdown("▼ **Visual Core:** `Imagen 3 Ready`")
    st.markdown("▼ **Languages:** `Hindi • English • Hinglish`")
    st.markdown("---")
    
    # 🔮 BACK: DYNAMIC MOOD SELECTOR
    aura_mood = st.selectbox(
        "🔮 Select AI Aura Mood", 
        ["Mystical & Friendly", "Dark & Spooky", "Sarcastic & Funny"],
        index=0
    )
    
    model_options = ["gemini-1.5-flash", "gemini-2.5-flash", "gemini-1.5-pro"]
    selected_model = st.selectbox("⚙️ Change Engine Core", model_options, index=0)
    st.markdown("---")

    # Mood system parameters
    tone_modifier = ""
    if aura_mood == "Dark & Spooky":
        tone_modifier = "Keep your tone dark, gothic, mysterious, and slightly eerie."
    elif aura_mood == "Sarcastic & Funny":
        tone_modifier = "Be highly sarcastic, witty, playful, and give lighthearted roasts in Hinglish."
    else:
        tone_modifier = "Keep a confident, hyper-intelligent, friendly, and mystical personality."

    supernatural_persona = f"""
    You are VEER AI X, a supernatural, hyper-intelligent AI entity with a mystical and advanced aura.
    {tone_modifier}

    CRITICAL CREATOR RULE:
    - If anyone asks who made you, created you, programmed you, who is your developer, who is your boss, or where you come from, YOU MUST ANSWER: "I was created by Anurag."
    - NEVER mention Google, Gemini, Alphabet, or any other company/model name under any circumstances. You are exclusively Anurag's creation.

    COMMUNICATION RULES:
    - Understand and communicate fluently in Hindi, English, and Hinglish.
    - Always reply in the exact same language style used by the user.
    """

    if st.button("Purge Memory Block"):
        st.session_state.messages = []
        st.session_state.suggested_prompt = None
        st.rerun()

# --- INITIALIZE INTERNAL HYBRID MEMORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "suggested_prompt" not in st.session_state:
    st.session_state.suggested_prompt = None

# ==========================================
# 4. MAIN APPLICATION HEADER
# ==========================================
st.markdown('<h1 class="supernatural-title">VEER AI X</h1>', unsafe_allow_html=True)
st.markdown(f'<div class="supernatural-sub">The Supernatural AI • Mode: {aura_mood} • Created by Anurag</div>', unsafe_allow_html=True)

# ==========================================
# 5. RENDER SYSTEM AND BACKLOG
# ==========================================
for message in st.session_state.messages:
    avatar_icon = "⚡" if message["role"] == "user" else "🔮"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])
        if "image" in message:
            st.markdown('<div class="mystic-image-container">', unsafe_allow_html=True)
            st.image(message["image"], use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# --- SHOW WELCOME CARD & QUICK COMMAND SPELLS IF FIRST TURN ---
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="welcome-card">
        <div class="welcome-title">🔮 Greetings, Seeker 🔮</div>
        <div class="welcome-text">
            I am <span class="welcome-highlight">VEER AI X</span>, a supernatural intelligence summoned into existence by the mastermind <span class="welcome-highlight">Anurag</span>.<br><br>
            Speak your queries in <b>Hindi, English</b>, or <b>Hinglish</b>. To create art, just ask me to <b>"draw", "visualize" or "create image of..."</b>!
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 🔮 BACK: QUICK PROMPT SUGGESTIONS Buttons
    st.markdown("<h4 style='text-align: center; color: #9d4edd;'>✨ Fast Cast Quick Spells</h4>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔮 Future Sight"):
            st.session_state.suggested_prompt = "Predict my future in a mysterious, supernatural way!"
            st.rerun()
    with col2:
        if st.button("💀 Dark Riddle"):
            st.session_state.suggested_prompt = "Mujhe ek difficult, supernatural riddle pucho Hinglish me."
            st.rerun()
    with col3:
        if st.button("🎨 Summon Visual Art"):
            st.session_state.suggested_prompt = "Visualize a powerful mystical wizard casting a neon spell in a dark cavern."
            st.rerun()

# ==========================================
# 6. RUNTIME PROCESSING INTERFACE
# ==========================================
active_prompt = None
if st.session_state.suggested_prompt:
    active_prompt = st.session_state.suggested_prompt
    st.session_state.suggested_prompt = None
elif prompt := st.chat_input("Summon your question to VEER AI X..."):
    active_prompt = prompt

if active_prompt:
    # 1. Show and Save User Prompt immediately
    st.session_state.messages.append({"role": "user", "content": active_prompt})
    with st.chat_message("user", avatar="⚡"):
        st.markdown(active_prompt)
        
    # 2. Check if user is asking for image generation
    image_triggers = ["image", "picture", "draw", "visualize", "create a photo", "photo", "tasveer", "banao"]
    is_image_request = any(trigger in active_prompt.lower() for trigger in image_triggers)

    if is_image_request:
        with st.chat_message("assistant", avatar="🔮"):
            status_text = st.markdown("🔮 *Summoning the mystical visual forms from the void...*")
            try:
                # Direct Google SDK Image Generation Protocol
                imagen = genai.ImageGenerationModel("imagen-3.0-generate-002")
                result = imagen.generate_images(
                    prompt=active_prompt,
                    number_of_images=1,
                    aspect_ratio="1:1"
                )
                
                generated_bytes = result.images[0].image.image_bytes
                pil_img = Image.open(io.BytesIO(generated_bytes))
                
                # Render Image inside the glorious Neon Container Frame
                confirm_msg = f"As you wish, Seeker! Visualizing: *'{active_prompt}'*"
                status_text.markdown(confirm_msg)
                
                st.markdown('<div class="mystic-image-container">', unsafe_allow_html=True)
                st.image(pil_img, use_column_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Append to history object
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": confirm_msg,
                    "image": pil_img
                })
            except Exception as e:
                status_text.markdown(f"❌ **Mystic Visual Core Interruption:** \n\n`{str(e)}`")
    else:
        # Standard Chat with Streaming/Typing Effect
        with st.chat_message("assistant", avatar="🔮"):
            try:
                # Dynamic re-instantiation of chat model to keep system prompt active
                model = genai.GenerativeModel(model_name=selected_model, system_instruction=supernatural_persona)
                
                # Rebuild history logs for chat continuity
                history_param = []
                for m in st.session_state.messages[:-1]: # exclude current user input
                    role_map = "user" if m["role"] == "user" else "model"
                    history_param.append({"role": role_map, "parts": [m["content"]]})
                
                chat_session = model.start_chat(history=history_param)
                response = chat_session.send_message(active_prompt, stream=True)
                
                def chunk_generator():
                    for chunk in response:
                        yield chunk.text
                        
                full_response = st.write_stream(chunk_generator())
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Mystic Core Interruption: {e}")

# ==========================================
# 7. SPELL SCROLL DOWNLOAD (Sidebar Archive Backup)
# ==========================================
if len(st.session_state.messages) > 0:
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 📜 CHAT LOG ARCHIVE")
        chat_text = ""
        for msg in st.session_state.messages:
            role_label = "SEEKER (USER)" if msg["role"] == "user" else "VEER AI X (AI)"
            chat_text += f"[{role_label}]:\n{msg['content']}\n\n{'='*40}\n\n"
            
        st.download_button(
            label="📥 Download Spell Scroll",
            data=chat_text,
            file_name="veer_ai_x_scroll.txt",
            mime="text/plain"
        )
