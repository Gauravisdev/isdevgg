from flask import Flask, render_template, request, jsonify
import requests
import base64
import os

app = Flask(__name__)

GITHUB_TOKEN = 'your_github_token'
GITHUB_REPO = 'username/repo_name'  # Replace with your actual repo
GITHUB_BRANCH = 'main'  # Replace with the branch used for GitHub Pages
GITHUB_API_URL = f'https://api.github.com/repos/{GITHUB_REPO}/contents/'

def upload_to_github(filename, content):
    url = GITHUB_API_URL + filename
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'message': f'Add {filename}',
        'content': base64.b64encode(content).decode('utf-8'),
        'branch': GITHUB_BRANCH
    }
    response = requests.put(url, json=data, headers=headers)
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    content = file.read()
    filename = os.path.join("uploads", file.filename)  # Save files in 'uploads' directory

    response = upload_to_github(filename, content)

    if response.get('content'):
        file_url = f"https://{GITHUB_REPO.split('/')[0]}.github.io/{filename}"
        return jsonify({"url": file_url})
    else:
        return jsonify({"error": response.get('message', 'Something went wrong')}), 500

if __name__ == '__main__':
    app.run(debug=True)
