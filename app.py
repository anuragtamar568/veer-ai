import streamlit as st

# 1. ऐप का नाम और टाइटल सेट करना
st.set_page_config(page_title="वीर AI", page_icon="🤖")
st.title("🤖 वीर: आपका पर्सनल एआई")
st.write("प्रणाम भाई! मैं आपका वफादार असिस्टेंट 'वीर' हूँ। कमांड दीजिए!")

# 2. चैट हिस्ट्री (बातचीत याद रखने के लिए) का सेटअप
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. पुरानी बातें स्क्रीन पर दिखाना
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. यूजर से इनपुट (कमांड) लेना
if user_input := st.chat_input("यहाँ अपनी कमांड लिखें भाई..."):
    # यूजर का मैसेज स्क्रीन पर दिखाना
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # वीर का जवाब तैयार करना
    veer_response = f"जी भाई, आपने कहा '{user_input}'। मैंने आपकी कमांड नोट कर ली है और मैं इसपर काम कर रहा हूँ!"
    
    # वीर का जवाब स्क्रीन पर दिखाना
    with st.chat_message("assistant"):
        st.markdown(veer_response)
    st.session_state.messages.append({"role": "assistant", "content": veer_response})
