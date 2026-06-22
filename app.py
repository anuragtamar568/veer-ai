import streamlit as st
import google.generativeai as genai

# पेज की सेटिंग्स (Title और Icon)
st.set_page_config(page_title="वीर: आपका पर्सनल एआई", page_icon="🤖", layout="centered")

# हेडर (Header)
st.title("🤖 वीर: आपका पर्सनल एआई")
st.write("मुझसे कोई भी सवाल पूछें, मैं आपकी मदद के लिए तैयार हूँ!")
st.write("---")

# 1. Streamlit Secrets से API Key चेक करना
if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"].strip() != "":
    api_key = st.secrets["GEMINI_API_KEY"]
    
    # Gemini AI को कॉन्फ़िगर करना
    genai.configure(api_key=api_key)
    
    # चैट हिस्ट्री के लिए सेशन स्टेट (Session State) सेट करना
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # पुरानी चैट को स्क्रीन पर दिखाना
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # यूजर से इनपुट लेना
    if prompt := st.chat_input("यहाँ अपना सवाल लिखें..."):
        # यूजर का मैसेज स्क्रीन पर दिखाना और सेव करना
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # एआई से रिस्पॉन्स जनरेट करना
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("*वीर सोच रहा है...*")
            
            try:
                # यहाँ हमने मॉडल अपडेट कर दिया है
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(prompt)
                
                # जवाब दिखाना और सेव करना
                message_placeholder.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
            except Exception as e:
                message_placeholder.markdown(f"❌ एरर आया: {str(e)}")

else:
    # अगर Secrets में API Key नहीं मिलती है तो यह एरर दिखेगा
    st.error("⚠️ API Key नहीं मिली!")
