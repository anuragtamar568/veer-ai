import streamlit as st
import requests
import streamlit.components.v1 as components

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="VEER AI // SECURE MODULE",
    page_icon="💻",
    layout="wide"
)

# ================= SESSION STATE FOR AUTH =================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# ================= CYBERPUNK VIBE CSS =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(rgba(0, 10, 0, 0.92), rgba(0, 0, 0, 0.97)), 
                url('https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1920') no-repeat center center fixed;
    background-size: cover;
}
header { visibility: hidden; }
.main-title {
    text-align: center;
    font-size: 55px;
    font-weight: 900;
    color: #00ff41;
    text-shadow: 0 0 8px #00ff41, 0 0 20px #00ff41;
    font-family: 'Courier New', Consolas, monospace !important;
    margin-bottom: 25px;
}
[data-testid="stSidebar"] {
    background: rgba(0, 5, 0, 0.95) !important;
    border-right: 2px solid #00ff41;
}
[data-testid="stSidebar"] * { color: #00ff41 !important; }
.cyber-card {
    background: rgba(0, 12, 0, 0.85);
    border: 2px solid #00ff41;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 0 15px rgba(0, 255, 65, 0.25);
}
.stChatMessage {
    background: rgba(0, 15, 0, 0.85) !important;
    border: 1px solid #00ff41 !important;
    border-radius: 10px !important;
    margin-bottom: 12px;
}
[data-testid="stChatInput"] {
    border: 2px solid #00ff41 !important;
    border-radius: 10px !important;
    background-color: #000000 !important;
    box-shadow: 0 0 20px rgba(0, 255, 65, 0.4) !important;
}
p, span, div, label, h1, h2, h3, h4, li { 
    color: #00ff41 !important; font-family: 'Courier New', Consolas, monospace !important; 
}
</style>
""", unsafe_allow_html=True)


# ================= SCREEN 1: 3D CYBER PATTERN LOCK =================
if not st.session_state.authenticated:
    st.markdown("<h1 class='main-title'>🔒 VEER AI // NODE LOCKED</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:#00ff41;'>ANURAG SIR, PLEASE DRAW THE PATTERN TO UNLOCK MICRO-CORE</h3>", unsafe_allow_html=True)
    
    # 3D Pattern Component (HTML/JS Canvas with Neon Effects)
    pattern_html = """
    <div id="pattern-container" style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 450px; background: rgba(0,10,0,0.4); border: 2px solid #00ff41; border-radius: 15px; box-shadow: 0 0 30px rgba(0,255,65,0.3); transform: perspective(800px) rotateX(10deg);">
        <canvas id="lockCanvas" width="300" height="300" style="cursor: pointer;"></canvas>
        <div id="status" style="color: #00ff41; font-family: monospace; margin-top: 15px; font-size: 16px; text-shadow: 0 0 5px #00ff41;">[ WAITING FOR BIOMETRIC PATTERN ]</div>
    </div>

    <script>
    const canvas = document.getElementById('lockCanvas');
    const ctx = canvas.getContext('2d');
    const status = document.getElementById('status');
    
    const rows = 3, cols = 3;
    const r = 15;
    const dots = [];
    let isDrawing = false;
    let selectedDots = [];

    // Create 3x3 Dot Matrix
    for(let i=0; i<rows; i++) {
        for(let j=0; j<cols; j++) {
            dots.push({
                id: (i*cols + j + 1),
                x: 60 + j * 90,
                y: 60 + i * 90
            });
        }
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw Lines
        if (selectedDots.length > 0) {
            ctx.beginPath();
            ctx.strokeStyle = '#00ff41';
            ctx.lineWidth = 5;
            ctx.shadowBlur = 15;
            ctx.shadowColor = '#00ff41';
            ctx.moveTo(selectedDots[0].x, selectedDots[0].y);
            for(let i=1; i<selectedDots.length; i++) {
                ctx.lineTo(selectedDots[i].x, selectedDots[i].y);
            }
            ctx.stroke();
        }

        // Draw Nodes
        dots.forEach(dot => {
            ctx.beginPath();
            let isSelected = selectedDots.some(d => d.id === dot.id);
            ctx.arc(dot.x, dot.y, isSelected ? r + 3 : r, 0, Math.PI * 2);
            ctx.fillStyle = isSelected ? '#00ff41' : '#003300';
            ctx.strokeStyle = '#00ff41';
            ctx.lineWidth = 2;
            ctx.shadowBlur = isSelected ? 20 : 5;
            ctx.shadowColor = '#00ff41';
            ctx.fill();
            ctx.stroke();
        });
    }

    function getMousePos(e) {
        const rect = canvas.getBoundingClientRect();
        return {
            x: (e.clientX || e.touches[0].clientX) - rect.left,
            y: (e.clientY || e.touches[0].clientY) - rect.top
        };
    }

    function startDraw(e) {
        isDrawing = true;
        selectedDots = [];
        status.innerText = "[ DRAWING COMMAND VECTOR... ]";
        handleMove(e);
    }

    function handleMove(e) {
        if (!isDrawing) return;
        const pos = getMousePos(e);
        dots.forEach(dot => {
            const dist = Math.hypot(dot.x - pos.x, dot.y - pos.y);
            if (dist < r + 10) {
                if (!selectedDots.some(d => d.id === dot.id)) {
                    selectedDots.push(dot);
                }
            }
        });
        draw();
    }

    function endDraw() {
        if (!isDrawing) return;
        isDrawing = false;
        const patternCode = selectedDots.map(d => d.id).join('');
        
        // मास्टर की चेक (कम से कम 3 डॉट्स कनेक्ट होने चाहिए टेस्टिंग को आसान रखने के लिए)
        if (patternCode.length >= 3) {
            status.innerHTML = "<span style='color:#00ff41;'>ACCESS GRANTED. BOOTING CORE...</span>";
            // Streamlit को सीक्रेट सिग्नल भेजना
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'SYSTEM_UNLOCKED'}, '*');
        } else {
            status.innerHTML = "<span style='color:#ff0000;'>ACCESS DENIED // PATTERN TOO SHORT</span>";
            selectedDots = [];
            setTimeout(draw, 1000);
        }
    }

    canvas.addEventListener('mousedown', startDraw);
    canvas.addEventListener('mousemove', handleMove);
    window.addEventListener('mouseup', endDraw);

    canvas.addEventListener('touchstart', startDraw);
    canvas.addEventListener('touchmove', handleMove);
    window.addEventListener('touchend', endDraw);

    draw();
    </script>
    """
    
    # Custom Trigger Receiver
    response_trigger = components.html(pattern_html, height=480)
    
    # सीक्रेट पैटर्न बाईपास बटन (सिर्फ बैकअप के लिए)
    if st.button("⌨️ EMERGENCY ACCESS CODE OVERRIDE"):
        st.session_state.authenticated = True
        st.rerun()

# ================= SCREEN 2: MAIN VEER AI INTERFACE =================
else:
    # ================= SIDEBAR (CORE CONTROL) =================
    with st.sidebar:
        st.markdown("# ⚡ VEER AI")
        st.success("🔒 ANURAG SIR AUTHENTICATED")

        st.markdown("---")
        selected_mode = st.radio(
            "🧠 CHOOSE SYSTEM CORE MODULE:",
            ["🟢 HACKER MODE", "📚 TEACHER MODE"]
        )
        st.markdown("---")
        if st.button("🔒 LOCK CONSOLE"):
            st.session_state.authenticated = False
            st.rerun()
        if st.button("🗑️ CLEAR SYSTEM MEMORY"):
            st.session_state.messages = []
            st.rerun()

    # ================= AI ENGINE LOGIC =================
    def fetch_unlimited_response(prompt, mode):
        if "HACKER" in mode:
            system_rules = (
                "You are VEER AI, a highly advanced cyber core intelligence. You were created and developed by 'Anurag Sir'. "
                "Always address the user respectfully as 'Anurag Sir'. Proudly state that Anurag Sir engineered you."
            )
        else:
            system_rules = (
                "You are VEER AI in Teacher Mode. You are a wise and patient educator. "
                "You were engineered by your brilliant student 'Anurag Sir'. Teach concepts simply in Hindi/Hinglish."
            )
        
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
            payload = {"contents": [{"parts": [{"text": f"System Instructions:\n{system_rules}\n\nUser Question:\n{prompt}"}]}]}
            response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=15)
            if response.status_code == 200:
                return response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            return "Anurag Sir, कनेक्शन एरर आ रहा है।"
        except Exception:
            return "Anurag Sir, सर्वर रिस्पॉन्स नहीं कर रहा है।"

    # ================= MAIN RENDERING =================
    st.markdown("<h1 class='main-title'>⚡ VEER AI // CORE INTERFACE ⚡</h1>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='cyber-card'>
        <h3 style='margin-top:0; color:#00ff41;'>[ {selected_mode} DEPLOYED ]</h3>
        • ARCHITECT & CREATOR : ANURAG SIR<br>
        • STATUS : MAINCORE ACCESS UNLOCKED ✔️
    </div>
    """, unsafe_allow_html=True)

    # Chat Logs
    for msg in st.session_state.messages:
        avatar = "👤" if msg["role"] == "user" else ("🤖" if "HACKER" in selected_mode else "👨‍🏫")
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # Chat Input
    input_hint = "यहाँ अपना हैकर कमांड लिखें, Anurag Sir..." if "HACKER" in selected_mode else "कोई भी पढ़ाई का सवाल पूछें, Anurag Sir..."
    prompt = st.chat_input(input_hint)

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
            
        with st.chat_message("assistant", avatar="🤖" if "HACKER" in selected_mode else "👨‍🏫"):
            with st.spinner("⚡ PROCESSING LOGS..."):
                reply = fetch_unlimited_response(prompt, selected_mode)
                st.markdown(reply)
                
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()
