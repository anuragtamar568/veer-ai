import streamlit as st

st.set_page_config(page_title="VEER AI", layout="centered")

# Basic style for clean look
st.markdown("""
    <style>
        .stApp { background-color: #000000; color: #00FF00; font-family: monospace; }
        .stTextInput > div > div > input { background: #111; color: #0f0; border: 1px solid #0f0; }
        .stButton>button { border: 1px solid #0f0; color: #0f0; background: #000; }
    </style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("## ☣️ VEER AI TERMINAL")
    key = st.text_input("ENTER KEY", type="password")
    if st.button("UNLOCK"):
        if key == "veer123":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("ACCESS DENIED")
else:
    st.markdown("## 📟 SYSTEM ONLINE")
    st.write("Master Anurag, terminal ready hai. Command type karein:")
    query = st.text_input("COMMAND:")
    if query:
        st.write(f"🤖 VEER AI: Processing '{query}' for Master Anurag...")
