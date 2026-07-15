import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")

response = model.generate_content("Hello")

st.write(response.text)

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
