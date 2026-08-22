<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>סופי (Sofy) - AI מתקדם</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f0f2f5;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        #chat-container {
            background-color: white;
            width: 100%;
            max-width: 650px;
            height: 100vh;
            display: flex;
            flex-direction: column;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }
        @media (min-width: 700px) {
            #chat-container {
                height: 90vh;
                border-radius: 15px;
            }
        }
        #header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: center;
            font-size: 1.3em;
            font-weight: bold;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .clear-btn {
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            cursor: pointer;
        }
        #chat-window {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .message {
            padding: 12px 16px;
            border-radius: 15px;
            max-width: 85%;
            line-height: 1.5;
            white-space: pre-wrap;
            position: relative;
        }
        .bot-message {
            background-color: #e9ecef;
            align-self: flex-start;
            border-bottom-right-radius: 2px;
        }
        .user-message {
            background-color: #667eea;
            color: white;
            align-self: flex-end;
            border-bottom-left-radius: 2px;
        }
        .play-btn {
            background: none;
            border: none;
            cursor: pointer;
            font-size: 1.2em;
            margin-right: 5px;
            vertical-align: middle;
        }
        /* עיצוב מיוחד לקוד */
        .code-box {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 8px;
            margin-top: 10px;
            font-family: monospace;
            direction: ltr;
            text-align: left;
            position: relative;
        }
        .copy-btn {
            position: absolute;
            top: 5px;
            right: 5px;
            background: #667eea;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.8em;
        }
        #controls {
            padding: 10px;
            display: flex;
            justify-content: space-around;
            background-color: #f8f9fa;
            border-top: 1px solid #ddd;
            overflow-x: auto;
        }
        .type-btn {
            background-color: white;
            border: 1px solid #ccc;
            padding: 8px 12px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: bold;
            white-space: nowrap;
            margin: 0 5px;
        }
        .type-btn.active {
            background-color: #764ba2;
            color: white;
            border-color: #764ba2;
        }
        #input-area {
            padding: 10px;
            display: flex;
            gap: 8px;
            background: white;
            border-top: 1px solid #ddd;
        }
        input[type="text"] {
            flex: 1;
            padding: 12px;
            border: 1px solid #ccc;
            border-radius: 25px;
            font-size: 1em;
            outline: none;
        }
        .action-btn {
            padding: 12px;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 50%;
            width: 45px;
            height: 45px;
            cursor: pointer;
            font-size: 1.2em;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .mic-btn {
            background-color: #ff4757;
        }
        .typing-indicator {
            align-self: flex-start;
            background-color: #e9ecef;
            padding: 10px 15px;
            border-radius: 15px;
            color: #555;
            font-style: italic;
            display: none;
        }
    </style>
</head>
<body>

<div id="chat-container">
    <div id="header">
        <span>✨ סופי (Sofy)</span>
        <button class="clear-btn" onclick="clearHistory()">🗑️ נקה שיחה</button>
    </div>
    
    <div id="chat-window">
        <!-- הודעות יופיעו כאן -->
    </div>
    
    <div id="typing-status" class="typing-indicator">סופי חושבת ומייצרת... ⏳</div>

    <div id="controls">
        <button class="type-btn active" onclick="setType('chat')">💬 צ'אט</button>
        <button class="type-btn" onclick="setType('code')">💻 קוד</button>
        <button class="type-btn" onclick="setType('image')">🖼️ תמונה</button>
        <button class="type-btn" onclick="setType('video')">🎬 וידאו+סאונד</button>
    </div>

    <div id="input-area">
        <button class="action-btn mic-btn" onclick="startDictation()" title="דבר אל סופי">🎤</button>
        <input type="text" id="user-input" placeholder="הקלד או דבר אל סופי..." onkeydown="checkEnter(event)">
        <button class="action-btn" onclick="sendMessage()">🚀</button>
    </div>
</div>

<script>
    let currentType = 'chat';
    const chatWindow = document.getElementById('chat-window');
    const typingStatus = document.getElementById('typing-status');

    // 1. שמירת היסטוריה לזיכרון הדפדפן (Local Storage)
    window.onload = function() {
        const savedChat = localStorage.getItem('sofy_history');
        if (savedChat) {
            chatWindow.innerHTML = savedChat;
        } else {
            addBotMessage("היי! אני סופי. אני זוכרת את השיחות שלנו, יודעת להקשיב לך וגם לדבר! מה תרצה שניצור היום?");
        }
    };

    function saveHistory() {
        localStorage.setItem('sofy_history', chatWindow.innerHTML);
    }

    function clearHistory() {
        if(confirm("למחוק את כל היסטוריית השיחה?")) {
            localStorage.removeItem('sofy_history');
            chatWindow.innerHTML = "";
            addBotMessage("הזיכרון נמחק. מתחילים דף חדש! ✨");
        }
    }

    // 2. בחירת סוג הפעולה
    function setType(type) {
        currentType = type;
        document.querySelectorAll('.type-btn').forEach(btn => btn.classList.remove('active'));
        event.target.classList.add('active');
    }

    function checkEnter(event) {
        if (event.key === 'Enter') sendMessage();
    }

    // 3. דיבור לטקסט (Speech-to-Text)
    function startDictation() {
        if (window.hasOwnProperty('webkitSpeechRecognition') || window.hasOwnProperty('SpeechRecognition')) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            const recognition = new SpeechRecognition();
            recognition.lang = 'he-IL';
            recognition.interimResults = false;
            
            document.getElementById('user-input').placeholder = "מקשיבה לך...";
            
            recognition.onresult = function(e) {
                document.getElementById('user-input').value = e.results[0][0].transcript;
                document.getElementById('user-input').placeholder = "הקלד או דבר אל סופי...";
                sendMessage(); // שולח אוטומטית אחרי שמדברים
            };
            
            recognition.onerror = function(e) {
                document.getElementById('user-input').placeholder = "הקלד או דבר אל סופי...";
            };
            
            recognition.start();
        } else {
            alert("הדפדפן שלך לא תומך בהקלטה קולית. נסה דרך Chrome.");
        }
    }

    // 4. הקראת טקסט קולית (Text-to-Speech)
    function speakText(text) {
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel(); // עוצר דיבור קודם אם יש
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'he-IL'; 
            utterance.rate = 1.0; // מהירות דיבור
            window.speechSynthesis.speak(utterance);
        } else {
            alert("הדפדפן שלך לא תומך בהקראת טקסט.");
        }
    }

    // העתקת קוד
    function copyCode(btnElement) {
        const codeText = btnElement.nextElementSibling.innerText;
        navigator.clipboard.writeText(codeText).then(() => {
            btnElement.innerText = "הועתק! ✔️";
            setTimeout(() => btnElement.innerText = "העתק 📋", 2000);
        });
    }

    // שליחת ההודעה לשרת
    async function sendMessage() {
        const inputField = document.getElementById('user-input');
        const prompt = inputField.value.trim();
        if (!prompt) return;

        // הוספת הודעת המשתמש
        const userMsgDiv = document.createElement('div');
        userMsgDiv.classList.add('message', 'user-message');
        userMsgDiv.innerText = prompt;
        chatWindow.appendChild(userMsgDiv);
        inputField.value = '';
        
        chatWindow.scrollTop = chatWindow.scrollHeight;
        saveHistory();

        // הפעלת אנימציית טעינה
        typingStatus.style.display = "block";
        chatWindow.scrollTop = chatWindow.scrollHeight;

        try {
            const response = await fetch('http://127.0.0.1:8000/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ request_type: currentType, prompt: prompt }),
            });

            const data = await response.json();
            typingStatus.style.display = "none"; // כיבוי טעינה
            
            if (currentType === 'code') {
                addCodeMessage(data.bot_message, data.result.code);
            } else if (currentType === 'image') {
                addBotMessage(`${data.bot_message}\n🔗 קישור לתמונה: ${data.result.url}`);
            } else if (currentType === 'video') {
                addBotMessage(`${data.bot_message}\n🎬 וידאו: ${data.result.video_url}\n🎵 פסקול: ${data.result.audio_url}\n⚙️ ${data.result.sync_status}`);
            } else {
                addBotMessage(data.result.response || data.bot_message);
            }

        } catch (error) {
            typingStatus.style.display = "none";
            addBotMessage('⚠️ שגיאה בתקשורת עם סופי. ודא ששרת הפייתון פועל ברקע.');
        }
    }

    // הוספת הודעת בוט רגילה עם כפתור הקראה
    function addBotMessage(text) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', 'bot-message');
        
        const playBtn = document.createElement('button');
        playBtn.classList.add('play-btn');
        playBtn.innerText = "🔊";
        playBtn.onclick = () => speakText(text);
        
        const textSpan = document.createElement('span');
        textSpan.innerText = text;

        msgDiv.appendChild(playBtn);
        msgDiv.appendChild(textSpan);
        
        chatWindow.appendChild(msgDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
        saveHistory();
    }

    // הוספת הודעת קוד עם כפתור העתקה
    function addCodeMessage(introText, codeText) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', 'bot-message');
        
        msgDiv.innerHTML = `
            <button class="play-btn" onclick="speakText('${introText}')">🔊</button>
            <span>${introText}</span>
            <div class="code-box">
                <button class="copy-btn" onclick="copyCode(this)">העתק 📋</button>
                <pre style="margin:0;">${codeText}</pre>
            </div>
        `;
        
        chatWindow.appendChild(msgDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
        saveHistory();
    }
</script>

</body>
</html>
