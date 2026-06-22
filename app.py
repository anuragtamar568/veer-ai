import streamlit as st
import google.generativeai as genai

# पेज की सेटिंग्स (Title और Icon)
st.set_page_config(page_title="वीर: आपका पर्सनल एआई", page_icon="🤖", layout="centered")

# हेडर (Header)
st.title("🤖 वीर: आपका पर्सनल एआई")
st.write("मुझसे कोई भी सवाल पूछें, मैं आपकी मदद के लिए तैयार हूँ!")
st.write("---")

# 1. Streamlit Secrets से API Key चेक करना और कॉन्फ़िगर करना
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    
    # Gemini AI को सही तरीके से कॉन्फ़िगर करना
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
                # Gemini Pro मॉडल का उपयोग
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                
                # जवाब दिखाना और सेव करना
                message_placeholder.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                message_placeholder.markdown(f"❌ एरर आया: {str(e)}")
else:
    # अगर Secrets में API Key नहीं मिलती है तो यह एरर दिखेगा
    st.error("⚠️ API Key नहीं मिली!")
    st.info("""
    **इसे ठीक करने के लिए नीचे दिए गए स्टेप्स को फॉलो करें:**
    1. अपने Streamlit Cloud डैशबोर्ड पर जाएं।
    2. अपने ऐप के सामने बने **Three Dots (...)** पर क्लिक करके **Settings** में जाएं।
    3. बाईं तरफ **Secrets** विकल्प पर क्लिक करें।
    4. नीचे दिया गया टेक्स्ट बॉक्स में पेस्ट करें और **Save** कर दें:
    ```toml
    GEMINI_API_KEY = "आपकी_असली_Gemini_API_Key_यहाँ_लिखें"
    ```
    """)
