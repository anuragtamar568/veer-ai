<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VEER AI - Specialist Workstation</title>
    <style>
        /* Global & Theme Settings */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Courier New', Courier, monospace;
        }
        body {
            background-color: #0b0f19; /* Perfect Dark Terminal Background */
            color: #ffffff;
            display: flex;
            flex-direction: column;
            height: 100vh;
            padding: 20px;
        }

        /* Header Section */
        header {
            border-bottom: 1px solid #334155;
            padding-bottom: 15px;
            margin-bottom: 20px;
        }
        .title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #ffffff;
            text-shadow: 0 0 10px rgba(0, 255, 255, 0.6), 0 0 20px rgba(0, 255, 255, 0.3);
            letter-spacing: 2px;
        }
        .subtitle {
            color: #00ff66; /* Neon Green */
            font-size: 0.9rem;
            margin-top: 5px;
            font-weight: bold;
        }

        /* Chat Container */
        .chat-container {
            flex: 1;
            overflow-y: auto;
            padding-right: 10px;
            margin-bottom: 20px;
        }

        /* Message Boxes */
        .message-row {
            display: flex;
            margin-bottom: 20px;
            align-items: flex-start;
        }
        .message-box {
            background-color: #1e293b;
            border-radius: 8px;
            padding: 15px;
            max-width: 85%;
            display: flex;
            gap: 15px;
            align-items: center;
            box-shadow: 0 0 15px rgba(0, 212, 255, 0.15);
        }
        /* Border color logic based on sender */
        .user-row .message-box {
            border: 1px solid #00d4ff; /* Sleek Cyan for User */
        }
        .ai-row .message-box {
            border: 1px solid #00ff66; /* Cyber Green for AI */
        }

        /* Icons */
        .icon-container {
            background-color: #ffffff;
            border-radius: 5px;
            padding: 5px;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 32px;
            height: 32px;
        }
        .icon-container span {
            font-size: 1.2rem;
        }

        /* Text Styling */
        .text-content {
            font-size: 1rem;
            line-height: 1.5;
            color: #e2e8f0;
        }

        /* Controls & Recording */
        .controls {
            margin-bottom: 15px;
        }
        .record-btn {
            background-color: #1e293b;
            border: 1px solid #475569;
            color: #e2e8f0;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 0.85rem;
            transition: all 0.2s ease;
        }
        .record-btn:hover {
            border-color: #00ff66;
            color: #00ff66;
            box-shadow: 0 0 8px rgba(0, 255, 102, 0.3);
        }

        /* Input Area Fixes */
        .input-area {
            position: relative;
            display: flex;
            align-items: center;
        }
        .command-input {
            width: 100%;
            background-color: #1e293b;
            border: 1px solid #334155; /* Normal subtle border */
            border-radius: 8px;
            padding: 15px 60px 15px 15px;
            color: #ffffff;
            font-size: 1rem;
            outline: none;
            transition: border-color 0.2s ease;
        }
        /* Red border strictly removed, now focuses with cyber green */
        .command-input:focus {
            border-color: #00ff66;
            box-shadow: 0 0 10px rgba(0, 255, 102, 0.2);
        }
        .send-btn {
            position: absolute;
            right: 15px;
            background-color: #00d4ff;
            border: none;
            color: #0b0f19;
            width: 32px;
            height: 32px;
            border-radius: 6px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            transition: background 0.2s;
        }
        .send-btn:hover {
            background-color: #00ff66;
        }
    </style>
</head>
<body>

    <!-- Header Section -->
    <header>
        <div class="title">VEER AI</div>
        <div class="subtitle">SPECIALIST WORKSTATION // DEVELOPER: ANURAG // SECURE CONNECTION</div>
    </header>

    <!-- Chat Stream -->
    <div class="chat-container" id="chatContainer">
        <!-- AI Initial Welcome Message -->
        <div class="message-row ai-row">
            <div class="message-box">
                <div class="icon-container"><span>🤖</span></div>
                <div class="text-content" id="welcome-text">Ping received. Veer online hai. Anurag, bolo kya command hai?</div>
            </div>
        </div>
    </div>

    <!-- Recording Section -->
    <div class="controls">
        <button class="record-btn">
            <span>🎙️</span> START RECORDING
        </button>
    </div>

    <!-- Command Input Box -->
    <div class="input-area">
        <input type="text" class="command-input" id="userInput" placeholder="ENTER COMMAND..." onkeypress="handleKeyPress(event)">
        <button class="send-btn" onclick="processCommand()">↑</button>
    </div>

    <!-- JavaScript for Terminal Mechanics -->
    <script>
        // Terminal Typewriter Effect function
        function typeWriter(element, text, speed = 30) {
            let i = 0;
            element.innerHTML = '';
            function type() {
                if (i < text.length) {
                    element.innerHTML += text.charAt(i);
                    i++;
                    setTimeout(type, speed);
                }
            }
            type();
        }

        // Handle Enter Key Press
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                processCommand();
            }
        }

        // Process Input and Simulate AI Reply
        function processCommand() {
            const inputField = document.getElementById('userInput');
            const chatContainer = document.getElementById('chatContainer');
            const query = inputField.value.trim();

            if (query === '') return;

            // 1. Append User Message
            const userRow = document.createElement('div');
            userRow.className = 'message-row user-row';
            userRow.innerHTML = `
                <div class="message-box">
                    <div class="icon-container"><span>👤</span></div>
                    <div class="text-content">${query}</div>
                </div>
            `;
            chatContainer.appendChild(userRow);
            inputField.value = ''; // Clear input

            // Scroll to bottom
            chatContainer.scrollTop = chatContainer.scrollHeight;

            // 2. Simulate AI Dynamic Response (Replace this block with your actual Fetch API call)
            setTimeout(() => {
                const aiRow = document.createElement('div');
                aiRow.className = 'message-row ai-row';
                
                // Temporary response simulation logic
                let replyText = "Command processed. System status normal.";
                if(query.includes('2+2')) {
                    replyText = "4. Yeh toh basic math tha, kuch complex pucho master!";
                } else if(query.toLowerCase() === 'hii' || query.toLowerCase() === 'hello') {
                    replyText = "Hello! Access granted. Kaise madad karu aapki?";
                }

                aiRow.innerHTML = `
                    <div class="message-box">
                        <div class="icon-container"><span>🤖</span></div>
                        <div class="text-content"></div>
                    </div>
                `;
                
                chatContainer.appendChild(aiRow);
                chatContainer.scrollTop = chatContainer.scrollHeight;

                // Trigger typewriter text effect on the newly added text block
                const textTarget = aiRow.querySelector('.text-content');
                typeWriter(textTarget, replyText, 25);

            }, 800);
        }
    </script>
</body>
</html>
