import streamlit as st
from google import genai
from google.genai import errors
from tenacity import retry, stop_after_attempt, wait_random_exponential

# 1. पेज का टाइटल और लेआउट सेट करना
st.set_page_config(page_title="वीर: आपका पर्सनल एआई", page_icon="🤖")
st.title("🤖 वीर: आपका पर्सनल एआई")

# 2. Gemini Client को इनिशियलाइज करना (Secrets से API Key लेकर)
# सुनिश्चित करें कि आपने Streamlit Secrets में GEMINI_API_KEY सेट की हुई है
@st.cache_resource
def get_genai_client():
    return genai.Client(api_key=st.secrets["AQ.Ab8RN6IkMPcqFCgPfQqoVvnxEhIu3fI68rjP2fRdTVJiJpsPvA"])

try:
    client = get_genai_client()
except Exception as e:
    st.error("API Key नहीं मिली! कृपया Streamlit Cloud के Secrets में GEMINI_API_KEY जोड़ें।")
    st.stop()

# 3. चैट हिस्ट्री (Chat History) को इनिशियलाइज करना
if "messages" not in st.session_state:
    st.session_state.messages = []

# पुराने मैसेज स्क्रीन पर दिखाना
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. API कॉल करने का फंक्शन (Caching और Automatic Retry के साथ)
@st.cache_data(ttl=1800)  # 30 मिनट के लिए एक जैसे सवालों का जवाब सेव रखेगा
@retry(wait=wait_random_exponential(min=2, max=30), stop=stop_after_attempt(4))
def get_ai_response(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        return response.text
    except errors.APIError as e:
        if e.code == 429:
            # यह एरर आने पर बैकएंड में tenacity दोबारा कोशिश करेगा
            raise e
        else:
            return f"कोई अन्य तकनीकी खराबी आई है: {e}"

# 5. यूजर इनपुट और रिस्पॉन्स हैंडलर
if user_input := st.chat_input("वीर से कुछ पूछें..."):
    # यूजर का मैसेज स्क्रीन पर दिखाएं और हिस्ट्री में सेव करें
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # एआई का रिस्पॉन्स जेनरेट करें
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("वीर सोच रहा है..."):
            try:
                reply = get_ai_response(user_input)
                message_placeholder.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                # अगर 4 बार रीट्राय करने के बाद भी कोटा फुल रहता है
                error_msg = "भाई, अभी फ्री लिमिट पूरी तरह खत्म हो चुकी है। कृपया कुछ समय बाद प्रयास करें या [Google AI Studio](https://ai.google.dev/pricing) पर जाकर Pay-As-You-Go चालू करें।"
                message_placeholder.error(error_msg)
