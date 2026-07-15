import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="VEER AI Pro",
    page_icon="🤖",
    layout="wide"
)

# Coder Theme
st.markdown("""
<style>
.stApp {background:#0d1117;color:#00ff41;}
h1 {color:#00ff41;text-align:center;}
</style>
""", unsafe_allow_html=True)

st.title("🤖 VEER AI PRO")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Ask anything...")

if prompt:
    st.session_state.messages.append(
        {"role":"user","content":prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    try:
        response = model.generate_content(prompt)
        reply = response.text

        with st.chat_message("assistant"):
            st.write(reply)

        st.session_state.messages.append(
            {"role":"assistant","content":reply}
        )

    except Exception as e:
        st.error(f"Error: {e}")
