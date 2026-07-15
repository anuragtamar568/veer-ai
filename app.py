def ask_gemini(prompt):

    try:
        api_key = st.secrets["GEMINI_API_KEY"]

        url = (
            "https://generativelanguage.googleapis.com"
            f"/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        )

        contents = []

        for msg in st.session_state.messages:

            role = (
                "user"
                if msg["role"] == "user"
                else "model"
            )

            contents.append({
                "role": role,
                "parts": [
                    {"text": msg["content"]}
                ]
            })

        if st.session_state.pdf_text:

            prompt = f"""
PDF CONTENT:
{st.session_state.pdf_text[:10000]}

QUESTION:
{prompt}
"""

        contents.append({
            "role": "user",
            "parts": [{"text": prompt}]
        })

        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json"
            },
            json={
                "contents": contents
            },
            timeout=60
        )

        if response.status_code != 200:
            return f"""
Status Code: {response.status_code}

Response:
{response.text}
"""

        data = response.json()

        if "candidates" not in data:
            return str(data)

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"ERROR: {str(e)}"
