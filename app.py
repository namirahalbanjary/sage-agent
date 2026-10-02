from flask import Flask, request, jsonify
from flask_cors import CORS
import ollama
import os 
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT
from authlib.integrations.flask_client import OAuth
from flask import session, redirect, url_for

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)
CORS(app)
client = ollama.Client(host='http://100.65.216.10:11434')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    response = client.chat(
        model='qwen2.5:3b',
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': user_message}
        ]
    )
    
    return jsonify({'reply': response['message']['content']})

@app.route('/login')
def login():
    redirect_uri = url_for('auth_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/auth/callback')
def auth_callback():
    token = google.authorize_access_token()
    user_info = token.get('userinfo')
    session['user'] = user_info
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))
    return f"Selamat datang, {user['name']}!"

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')