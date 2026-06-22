import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Veer AI", page_icon="🤖")
st.title("🤖 Veer AI Assistant")

# Hum secrets ko safe tarike se access karenge
try:
    # Pehle st.secrets check karein
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["AQ.Ab8RN6LGFv3-HifsFLhY2VRwbxd6baWF2irmRzdfOAcxmWtB3g"]
    else:
        st.error("Error: 'GOOGLE_API_KEY' naam ki secret key nahi mili. Manage App > Settings > Secrets mein check karein.")
        st.stop()
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

# ... baki ka code jo pehle tha ...
