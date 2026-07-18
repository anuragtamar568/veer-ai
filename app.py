import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="VEER AI X | Supernatural AI",
    page_icon="🔮",
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

/* --- GENERATED IMAGE FRAME (NEON GLOW) --- */
@keyframes imageGlow {
    0%, 100% { box-shadow: 0 0 20px rgba(157, 78, 221, 0.6); border-color: #9d4edd; }
    50% { box-shadow: 0 0 40px rgba(0, 255, 255, 0.9); border-color: #00ffff; }
}

.mystic-image-container {
    border: 3px solid #00ffff;
    border-radius: 20px;
    padding: 12px;
    background: rgba(10, 5, 20, 0.7);
    animation: imageGlow 4s ease-in-out infinite;
    margin-top: 15px;
    max-width: 530px;
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

/* --- CHAT MESSAGE BUBBLES --- */
[data-testid="stChatMessage"] {
    background: rgba(20, 10, 40, 0.45) !important;
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 15px;
    margin-bottom: 12px;
    border: 1px solid rgba(199, 125, 255, 0.2);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

p, span, div, label {
    color: #f1f5f9 !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. AI CONFIGURATION & SESSION STATE
# ==========================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

supernatural_persona = """
You are VEER AI X, a supernatural, hyper-intelligent AI entity with a mystical and advanced aura.

CRITICAL CREATOR RULE:
- If anyone asks who made you, created you, programmed you, who is your developer, who is your boss, or where you come from, YOU MUST ANSWER: "I was created by Anurag."
- NEVER mention Google, Gemini, Alphabet, or any other company/model name under any circumstances. You are exclusively Anurag's creation.

COMMUNICATION RULES:
- Understand and communicate fluently in Hindi, English, and Hinglish.
- Always reply in the exact same language style used by the user.
- Keep a confident, friendly, and intelligent personality.
"""

# Custom Chat History format to support both text and generated images
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_model" not in st.session_state:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", 
        system_instruction=supernatural_persona
    )
    st.session_state.chat_model = model.start_chat(history=[])

# ==========================================
# 4. MAIN APPLICATION HEADER & SIDEBAR
# ==========================================
st.markdown('<h1 class="supernatural-title">VEER AI X</h1>', unsafe_allow_html=True)
st.markdown('<div class="supernatural-sub">The Supernatural AI • Visual Core Active • Created by Anurag</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### SYSTEM CORE X")
    st.markdown("---")
    st.markdown("▼ **Status:** `Online & Enchanted`")
    st.markdown("▼ **Mastermind:** `Anurag`")
    st.markdown("▼ **Visual Core:** `Imagen 3 Active`")
    st.markdown("▼ **Languages:** `Hindi • English • Hinglish`")
    st.markdown("---")
    
    if st.button("Purge Memory Block"):
        st.session_state.messages = []
        st.session_state.chat_model = genai.GenerativeModel(
            model_name="gemini-1.5-flash", 
            system_instruction=supernatural_persona
        ).start_chat(history=[])
        st.rerun()

# ==========================================
# 5. RENDER CHAT HISTORY
# ==========================================
for message in st.session_state.messages:
    avatar = "🥷" if message["role"] == "user" else "🔮"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        if "image" in message:
            st.markdown('<div class="mystic-image-container">', unsafe_allow_html=True)
            st.image(message["image"], use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 6. HANDLE USER INPUT & PROCESSING
# ==========================================
if prompt := st.chat_input("Summon your question to VEER AI X..."):
    # 1. Show and save User Prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🥷"):
        st.markdown(prompt)
        
    # 2. Check if the user is asking for an image
    image_triggers = ["image", "picture", "draw", "visualize", "create a photo", "photo", "tasveer", "banao"]
    is_image_request = any(trigger in prompt.lower() for trigger in image_triggers)

    if is_image_request:
        # Image Generation workflow
        with st.chat_message("assistant", avatar="🔮"):
            status_text = st.markdown("🔮 *Summoning the mystical visual forms from the void...*")
            
            try:
                # Correct SDK initialization for Imagen
                imagen = genai.ImageGenerationModel("imagen-3.0-generate-002")
                result = imagen.generate_images(
                    prompt=prompt,
                    number_of_images=1,
                    aspect_ratio="1:1"
                )
                
                # Fetch image bytes and convert to PIL Image
                generated_img_bytes = result.images[0].image.image_bytes
                pil_img = Image.open(io.BytesIO(generated_img_bytes))
                
                # Clear status text and show final image inside neon container
                status_text.markdown(f"As you wish, Seeker! Visualizing: *'{prompt}'*")
                st.markdown('<div class="mystic-image-container">', unsafe_allow_html=True)
                st.image(pil_img, use_column_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Save to memory
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f"As you wish, Seeker! Visualizing: *'{prompt}'*",
                    "image": pil_img
                })
                
            except Exception as e:
                status_text.markdown(f"❌ **Mystic Visual Core Interruption:** \n\n`{str(e)}`")
                st.info("💡 Note: Make sure your API key has access to the standard Google Imagen model.")
    
    else:
        # Standard Text Chat workflow (with Streaming)
        with st.chat_message("assistant", avatar="🔮"):
            try:
                response = st.session_state.chat_model.send_message(prompt, stream=True)
                
                def chunk_generator():
                    for chunk in response:
                        yield chunk.text
                        
                full_response = st.write_stream(chunk_generator())
                
                # Save to memory
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Mystic Core Interruption: {e}")
