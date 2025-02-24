from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
API_KEY = 'AIzaSyDCuWm5sKlxNeWGfdctfBRxvm5zuERVNIs'
BASE_URL = 'https://generativelanguage.googleapis.com/v1/models/'

@app.route('/generate-text', methods=['POST'])
def generate_text():
    model = request.json.get('model', 'gemini-pro')
    prompt = request.json['prompt']
    
    full_url = f"{BASE_URL}{model}:generateText?key={API_KEY}"
    
    response = requests.post(full_url, json={"prompt": {"text": prompt}})
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
