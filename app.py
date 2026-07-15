st.markdown("""
<style>

/* ===== HACKER BACKGROUND ===== */

.stApp{
    background:
    radial-gradient(circle at top left,#0f0f0f,#050505,#000000);
    color:#00ff88;
}

/* ===== SIDEBAR ===== */

section[data-testid="stSidebar"]{
    background:#050505;
    border-right:1px solid #00ff88;
}

/* ===== GLOW TITLE ===== */

.glow-title{
    text-align:center;
    font-size:60px;
    font-weight:bold;
    color:#00ff88;

    text-shadow:
        0 0 5px #00ff88,
        0 0 10px #00ff88,
        0 0 20px #00ff88,
        0 0 40px #00ff88;

    animation:glow 2s infinite alternate;
}

@keyframes glow{

    from{
        text-shadow:
            0 0 10px #00ff88,
            0 0 20px #00ff88;
    }

    to{
        text-shadow:
            0 0 20px #00ff88,
            0 0 40px #00ff88,
            0 0 80px #00ff88;
    }

}

/* ===== SHINING TEXT ===== */

.shine{

    background:linear-gradient(
        90deg,
        #00ff88,
        #ffffff,
        #00ff88
    );

    background-size:200% auto;

    color:transparent;

    -webkit-background-clip:text;

    animation:shine 3s linear infinite;
}

@keyframes shine{

    to{
        background-position:200% center;
    }

}

/* ===== CHAT BOX ===== */

[data-testid="stChatMessage"]{

    background:#0d1117;

    border:1px solid #00ff88;

    border-radius:15px;

    box-shadow:
        0 0 10px rgba(0,255,136,.2);

    padding:10px;

}

/* ===== INPUT ===== */

.stChatInputContainer{

    border:2px solid #00ff88;

    border-radius:15px;

    box-shadow:
        0 0 15px rgba(0,255,136,.4);

}

/* ===== BUTTON ===== */

.stButton button{

    background:#00ff88 !important;

    color:black !important;

    border:none !important;

    font-weight:bold !important;

    border-radius:10px !important;

}

/* ===== TEXT ===== */

p,span,div{
    color:#e5ffe5 !important;
}

/* ===== SCROLLBAR ===== */

::-webkit-scrollbar{
    width:8px;
}

::-webkit-scrollbar-thumb{
    background:#00ff88;
    border-radius:20px;
}

</style>
""", unsafe_allow_html=True)
