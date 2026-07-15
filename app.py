import streamlit as st
import requests

st.set_page_config(page_title="VEER AI Pro", page_icon="🤖")

st.title("🤖 VEER AI Pro")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not found in Streamlit Secrets")
    st.stop()

prompt = st.chat_input("Ask anything...")

if prompt:
    with st.chat_message("user"):
        st.write(prompt)

    url = (
        f"https://generativelanguage.googleapis.com/"
        f"v1beta/models/gemini-2.5pro:generateContent?key={api_key}"
    )

    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json={
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ]
            },
            timeout=60
        )

        st.write("Status:", response.status_code)

        if response.status_code == 200:
            data = response.json()

            reply = data["candidates"][0]["content"]["parts"][0]["text"]

            with st.chat_message("assistant"):
                st.write(reply)

        else:
            st.error(response.text)

    except Exception as e:
        st.error(str(e))
