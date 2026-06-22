import streamlit as st

# Streamlit page configuration (Tabs configurations)
st.set_page_config(page_title="VEER AI Workstation", layout="centered")

# Visual elements ko frontend ke liye string me pack kiya hai
interface_html = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VEER AI - Specialist Workstation</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Courier New', Courier, monospace;
        }

        body {
            background-color: #0b0f19;
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 95vh;
            padding: 10px;
        }

        .workstation-container {
            width: 100%;
            max-width: 800px;
            background: #0d1321;
            border: 1px solid #1e293b;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
        }

        .header {
            margin-bottom: 25px;
            border-bottom: 1px solid #1e293b;
            padding-bottom: 20px;
        }

        .brand-title {
            font-size: 2.5rem;
            font-weight: 900;
            color: #00ffff;
            text-transform: uppercase;
            letter-spacing: 3px;
            text-shadow: 0 0 10px rgba(0, 255, 255, 0.5), 0 0 20px rgba(0, 255, 255, 0.2);
            margin-bottom: 15px;
        }

        .meta-text {
            font-size: 0.85rem;
            color: #00ff66;
            font-weight: bold;
            letter-spacing: 1.5px;
            line-height: 1.8;
            text-transform: uppercase;
        }

        .chat-log {
            height: 380px;
            overflow-y: auto;
            margin-bottom: 20px;
            padding-right: 10px;
        }

        .chat-log::-webkit-scrollbar {
            width: 6px;
        }
        .chat-log::-webkit-scrollbar-thumb {
            background: #1e293b;
            border-radius: 4px;
        }

        .msg-card {
            background: #161f30;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            display: flex;
            align-items: flex-start;
            gap: 15px;
            border: 1px solid transparent;
            box-shadow: 0 0 15px rgba(0, 212, 255, 0.05);
        }

        .msg-card.ai-card {
            border-left: 4px solid #00d4ff;
            box-shadow: 0 0 15px rgba(0, 212, 255, 0.15);
        }

        .msg-card.user-card {
            border-left: 4px solid #94a3b8;
        }

        .avatar {
            background: #1e293b;
            padding: 6px 10px;
            border-radius: 6px;
            font-size: 1.1rem;
            border: 1px solid #334155;
        }

        .msg-content {
            flex: 1;
        }

        .msg-text {
            font-size: 0.95rem;
            line-height: 1.6;
            color: #e2e8f0;
            letter-spacing: 0.5px;
        }

        .controls-section {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .record-btn {
            background: #161f30;
            border: 1px solid #334155;
            color: #94a3b8;
            padding: 10px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
            font-size: 0.8rem;
            letter-spacing: 1px;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            width: fit-content;
        }

        .command-bar-wrapper {
            position: relative;
            display: flex;
            align-items: center;
            background: #161f30;
            border: 1px solid #00d4ff;
            border-radius: 8px;
            padding: 5px 10px;
        }

        .command-input {
            width: 100%;
            background: transparent;
            border: none;
            outline: none;
            color: #ffffff;
            font-size: 0.95rem;
            padding: 12px;
            letter-spacing: 1px;
        }

        .submit-btn {
            background: #00d4ff;
            border: none;
            color: #0b0f19;
            width: 36px;
            height: 36px;
            border-radius: 6px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }
    </style>
</head>
<body>

    <div class="workstation-container">
        <div class="header">
            <h1 class="brand-title">VEER AI</h1>
            <div class="meta-text">
                SPECIALIST WORKSTATION<br>
                DEVELOPER: ANURAG // SECURE CONNECTION
            </div>
        </div>

        <div class="chat-log" id="chatLog">
            <div class="msg-card user-card">
                <div class="avatar">👤</div>
                <div class="msg-content">
                    <div class="msg-text">hii</div>
                </div>
            </div>

            <div class="msg-card ai-card">
                <div class="avatar">🤖</div>
                <div class="msg-content">
                    <div class="msg-text">पिंग रिसीव्ड। वीर ऑनलाइन है, अनुराग। बताओ, क्या टास्क एक्जीक्यूट करना है? कोई कोड पैच करना है या डेटा सिंक?</div>
                </div>
            </div>
        </div>

        <div class="controls-section">
            <button class="record-btn" id="recordBtn">
                <span>🎙️</span> START RECORDING
            </button>

            <div class="command-bar-wrapper">
                <input type="text" class="command-input" id="cmdInput" placeholder="ENTER COMMAND..." autocomplete="off">
                <button class="submit-btn" id="sendBtn">▲</button>
            </div>
        </div>
    </div>

    <script>
        const chatLog = document.getElementById('chatLog');
        const cmdInput = document.getElementById('cmdInput');
        const sendBtn = document.getElementById('sendBtn');

        function appendMessage(sender, text) {
            const card = document.createElement('div');
            card.className = `msg-card \${sender === 'user' ? 'user-card' : 'ai-card'}`;
            
            card.innerHTML = `
                <div class="avatar">\${sender === 'user' ? '👤' : '🤖'}</div>
                <div class="msg-content">
                    <div class="msg-text">\${text}</div>
                </div>
            `;
            
            chatLog.appendChild(card);
            chatLog.scrollTop = chatLog.scrollHeight;
        }

        function handleCommand() {
            const query = cmdInput.value.trim();
            if(!query) return;

            appendMessage('user', query);
            cmdInput.value = '';

            setTimeout(() => {
                let response = "कमांड समझ नहीं आई। क्या आप दोबारा स्पेसिफाई कर सकते हैं?";
                
                if(query.includes('2+2') || query.includes('2 + 2')) {
                    response = "कैलकुलेशन कम्पलीट: **4**। इसके लिए ज्यादा कोर प्रोसेसिंग की जरूरत नहीं पड़ी।";
                } else if(query.toLowerCase() === 'hii' || query.toLowerCase() === 'hello') {
                    response = "सिस्टम ऑनलाइन है। कमांड दीजिए, अनुराग।";
                }
                
                appendMessage('ai', response);
            }, 800);
        }

        sendBtn.addEventListener('click', handleCommand);
        cmdInput.addEventListener('keypress', (e) => {
            if(e.key === 'Enter') handleCommand();
        });
    </script>
</body>
</html>
"""

# HTML code ko Streamlit frame ke andar render karne ke liye render call
st.components.v1.html(interface_html, height=650, scrolling=True)
