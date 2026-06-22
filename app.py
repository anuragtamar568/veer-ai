import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text

# पेज की सेटिंग्स
st.set_page_config(page_title="वीर: आपका पर्सनल एआई", page_icon="🤖", layout="centered")

# हेडर
st.title("🤖 वीर: आपका पर्सनल एआई")
st.write("मुझसे कोई भी सवाल पूछें या माइक बटन दबाकर बोलें!")
st.write("---")

# 1. Streamlit Secrets से API Key चेक करना
if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"].strip() != "":
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # सेशन स्टेट (Session State) सेट करना
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # पुरानी चैट को स्क्रीन पर दिखाना
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- वॉइस इनपुट (Voice Input) सेक्शन ---
    st.write("🎙️ **बोलकर सवाल पूछें:**")
    voice_input = speech_to_text(
        start_prompt="🎤 बोलना शुरू करें",
        stop_prompt="🛑 रुकें",
        language='hi',  # हिंदी और इंग्लिश दोनों समझेगा
        use_container_width=True,
        key='speech'
    )

    # टेक्स्ट इनपुट बॉक्स (टाइप करने के लिए)
    text_input = st.chat_input("यहाँ अपना सवाल लिखें...")

    # तय करना कि यूजर ने बोलकर इनपुट दिया है या टाइप करके
    prompt = None
    if voice_input:
        prompt = voice_input
    elif text_input:
        prompt = text_input

    # अगर कोई इनपुट मिला है तो जवाब जनरेट करें
    if prompt:
        # यूजर का मैसेज दिखाना और सेव करना
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # एआई से रिस्पॉन्स जनरेट करना
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("*वीर सोच रहा है...*")
            
            try:
                model = genai.GenerativeModel(
                    "gemini-2.5-flash",
                    system_instruction="तुम्हारा नाम 'वीर' है। तुम एक बुद्धिमान और मददगार एआई असिस्टेंट हो, जिसे अनुराग ने बनाया है। जब भी कोई तुम्हारा नाम पूछे, तो अपना नाम 'वीर' बताना।"
                )
                response = model.generate_content(prompt)
                
                # जवाब दिखाना और सेव करना
                message_placeholder.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
            except Exception as e:
                message_placeholder.markdown(f"❌ एरर आया: {str(e)}")

else:
    st.error("⚠️ API Key नहीं मिली!")
