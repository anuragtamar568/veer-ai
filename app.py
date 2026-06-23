}
/* Buttons */
.stButton button{
    width:100%;
    background:black;
    color:#00ff41;
    border:1px solid #00ff41;
    border-radius:12px;
    box-shadow:0 0 10px #00ff41;
}
.stButton button:hover{
    background:#00ff41;
    color:black;
}
/* Text Global Overrides */
p, span, div, label, h1, h2, h3, h4 {
    color: #00ff41 !important;
    font-family: Consolas, monospace !important;
}
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("# ⚡ VEER AI")
    st.success("🟢 SYSTEM ONLINE")

    # पुराने सारे कार्ड्स हटाकर यहाँ नया एनिमेटेड रोबोट लोगो सेट कर दिया गया है
    st.markdown("""
    <div class="cyber-logo-card">
        <div class="cyber-logo-text">🤖</div>
        <h3 style="margin:0; letter-spacing: 2px;">V E E R</h3>
        <span style="font-size:11px; opacity:0.8;">CORE v2.5</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("🗑️ NEW CHAT"):
        st.session_state.messages = []
        st.rerun()

    chat_text = ""
    for m in st.session_state.messages:
        chat_text += f"{m['role'].upper()} : {m['content']}\n\n"

    st.download_button(
        "📥 DOWNLOAD CHAT",
        chat_text,
        file_name="veer_chat.txt"
    )

# ================= MAIN TITLE =================
st.markdown("""
<h1 class='main-title'>
⚡ VEER AI // CYBER CORE ⚡
</h1>
""", unsafe_allow_html=True)

# ================= DASHBOARD =================
st.markdown("""
<div class='cyber-card'>
## 🟢 SYSTEM STATUS : ONLINE<br>
👤 USER : ANURAG SIR<br>
🧠 AI ENGINE : GEMINI<br>
🛡 SECURITY : ACTIVE<br>
⚡ MODE : CYBER INTELLIGENCE
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("💬 Messages", len(st.session_state.messages))
with c2:
    st.metric("🧠 AI", "ONLINE")
with c3:
    st.metric("⚡ Status", "ACTIVE")

st.markdown("---")

# ================= CHAT HISTORY DISPLAY =================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================= CHAT INPUT & LOGIC =================
prompt = st.chat_input(">>> ENTER COMMAND")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("⚡ ACCESSING CYBER CORE..."):
            try:
                response = model.generate_content(prompt)
                reply = response.text
            except Exception as e:
                if "429" in str(e):
                    reply = "🚫 API LIMIT EXCEEDED\n\nGemini free quota समाप्त हो गई है।\n\nकृपया कुछ समय बाद पुनः प्रयास करें।"
                else:
                    reply = f"❌ Error: {e}"
            
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
    color:#00ff41;
    border:1px solid #00ff41;
    border-radius:12px;
    box-shadow:0 0 10px #00ff41;
}
.stButton button:hover{
    background:#00ff41;
    color:black;
}
/* Text Global Overrides */
p,span,div,label,h1,h2,h3,h4{
    color:#00ff41 !important;
    font-family:Consolas, monospace !important;
}
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("# ⚡ VEER AI")
    st.success("🟢 SYSTEM ONLINE")

    # पुराना Face और Smart असिस्टेंट हटाकर यहाँ न्यू ग्लोइंग लोगो सेट कर दिया है
    st.markdown("""
    <div class="cyber-logo-card">
        <div class="cyber-logo-text">🤖</div>
        <h3 style="margin:0; letter-spacing: 2px;">V E E R</h3>
        <span style="font-size:10px; opacity:0.7;">CORE v2.5</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("🗑️ NEW CHAT"):
        st.session_state.messages = []
        st.rerun()

    chat_text = ""
    for m in st.session_state.messages:
        chat_text += f"{m['role'].upper()} : {m['content']}\n\n"

    st.download_button(
        "📥 DOWNLOAD CHAT",
        chat_text,
        file_name="veer_chat.txt"
    )

# ================= MAIN TITLE =================
st.markdown("""
<h1 class='main-title'>
⚡ VEER AI // CYBER CORE ⚡
</h1>
""", unsafe_allow_html=True)

# ================= DASHBOARD =================
st.markdown("""
<div class='cyber-card'>
## 🟢 SYSTEM STATUS : ONLINE<br>
👤 USER : ANURAG SIR<br>
🧠 AI ENGINE : GEMINI<br>
🛡 SECURITY : ACTIVE<br>
⚡ MODE : CYBER INTELLIGENCE
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("💬 Messages", len(st.session_state.messages))
with c2:
    st.metric("🧠 AI", "ONLINE")
with c3:
    st.metric("⚡ Status", "ACTIVE")

st.markdown("---")

# ================= CHAT HISTORY DISPLAY =================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================= CHAT INPUT & LOGIC =================
prompt = st.chat_input(">>> ENTER COMMAND")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("⚡ ACCESSING CYBER CORE..."):
            try:
                response = model.generate_content(prompt)
                reply = response.text
            except Exception as e:
                if "429" in str(e):
                    reply = "🚫 API LIMIT EXCEEDED\n\nGemini free quota समाप्त हो गई है।\n\nकृपया कुछ समय बाद पुनः प्रयास करें।"
                else:
                    reply = f"❌ Error: {e}"
            
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
