import streamlit as st
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="VEER AI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 VEER AI - Media Control Interface")

# Aapka HTML aur SVG Dashboard Code
custom_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            background-color: #0d1117;
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 80vh;
            margin: 0;
        }
        .media-container {
            background: linear-gradient(135deg, #1e293b, #0f172a);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            text-align: center;
            border: 1px solid #334155;
            width: 80%;
            max-width: 600px;
        }
        .media-control {
            margin-top: 20px;
            display: flex;
            justify-content: center;
            gap: 20px;
        }
        .btn {
            background: #2563eb;
            border: none;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            transition: 0.3s;
        }
        .btn:hover {
            background: #1d4ed8;
        }
        svg {
            filter: drop-shadow(0px 4px 8px rgba(0, 0, 0, 0.3));
        }
    </style>
</head>
<body>

<div class="media-container">
    <svg width="96" height="96" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#3b82f6" />
                <stop offset="100%" stop-color="#8b5cf6" />
            </linearGradient>
        </defs>
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z" fill="url(#grad)"/>
    </svg>

    <h2>VEER AI Player</h2>
    <p style="color: #94a3b8;">System Engine Ready & Functional</p>

    <div class="media-control">
        <button class="btn">⏮ Prev</button>
        <button class="btn" style="background:#10b981;">▶ Play</button>
        <button class="btn">⏭ Next</button>
    </div>
</div>

</body>
</html>
"""

# HTML component ko sahi tarike se render karne ke liye component ka use karein
components.html(custom_html, height=500, scrolling=True)

# Streamlit Native Elements (Optional - controls chalane ke liye)
st.sidebar.header("Settings")
volume = st.sidebar.slider("Volume Control", 0, 100, 70)
st.sidebar.write(f"Current Volume: {volume}%")
