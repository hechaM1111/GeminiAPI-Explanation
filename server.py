from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import requests
from flask_cors import CORS

# تحميل مفتاح API من ملف .env
load_dotenv()
API_KEY = os.getenv('GOOGLE_API_KEY', 'AIzaSyDCuWm5sKlxNeWGfdctfBRxvm5zuERVNIs')

# إنشاء تطبيق Flask
app = Flask(__name__)
CORS(app)  # تفعيل CORS للسماح بالطلبات من أي مصدر

@app.route('/')
def home():
    return '''
    <html dir="rtl">
        <head>
            <title>خدمة Gemini API</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    background-color: #f0f0f0;
                }
                .container {
                    background-color: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    max-width: 800px;
                    margin: 0 auto;
                }
                textarea {
                    width: 100%;
                    height: 100px;
                    margin: 10px 0;
                    padding: 10px;
                    border-radius: 5px;
                    border: 1px solid #ddd;
                }
                button {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #45a049;
                }
                #response {
                    margin-top: 20px;
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    min-height: 100px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>مرحباً بك في خدمة Gemini API</h1>
                <textarea id="prompt" placeholder="اكتب سؤالك هنا..."></textarea>
                <button onclick="sendPrompt()">إرسال</button>
                <div id="response"></div>
            </div>

            <script>
                async function sendPrompt() {
                    const prompt = document.getElementById('prompt').value;
                    const response = document.getElementById('response');
                    response.innerHTML = 'جاري المعالجة...';

                    try {
                        const result = await fetch('/ask', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ prompt: prompt })
                        });
                        const data = await result.json();
                        response.innerHTML = data.response || data.error;
                    } catch (error) {
                        response.innerHTML = 'حدث خطأ في المعالجة';
                    }
                }
            </script>
        </body>
    </html>
    '''

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({'error': 'الرجاء إدخال نص'})

        # إرسال الطلب إلى Gemini API
        response = requests.post(
            f'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}',
            json={
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ]
            }
        )
        
        # التحقق من الاستجابة
        if response.status_code == 200:
            result = response.json()
            text = result['candidates'][0]['content']['parts'][0]['text']
            return jsonify({'response': text})
        else:
            return jsonify({'error': f'خطأ في API: {response.status_code}'})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
