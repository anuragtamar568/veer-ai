st.markdown("""
<style>

/* Main App */
.stApp{
    background:#0d1117;
    color:#00ff88;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#090c10;
    border-right:1px solid #00ff88;
}

/* Headings */
h1,h2,h3{
    color:#00ff88 !important;
    text-shadow:0 0 10px #00ff88;
}

/* User Chat */
[data-testid="stChatMessage"]:has(.st-emotion-cache-janbn0){
    background:#1f2937;
}

/* Assistant Chat */
[data-testid="stChatMessage"]{
    background:#111827;
    border:1px solid #00ff88;
    border-radius:12px;
}

/* Text */
p,div,span{
    color:#e5e7eb !important;
}

/* Input */
.stChatInputContainer{
    border:2px solid #00ff88;
    border-radius:12px;
}

/* Buttons */
.stButton button{
    background:#00ff88;
    color:black;
    font-weight:bold;
    border:none;
}

/* Scrollbar */
::-webkit-scrollbar{
    width:8px;
}
::-webkit-scrollbar-thumb{
    background:#00ff88;
}

</style>
""", unsafe_allow_html=True)
