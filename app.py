
# app.py
from flask import Flask, request, render_template
from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    prompt = request.form.get('prompt')
    file = request.files['file']
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))
        file = client.files.upload(file=filepath)
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=[prompt, file]
        )
        return f"Here are the results: {response.text}"
    return "No file uploaded"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
