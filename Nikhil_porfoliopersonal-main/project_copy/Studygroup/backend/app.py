from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
from dotenv import load_dotenv
import openai
from datetime import datetime
import json
import bcrypt
from functools import wraps
import jwt

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
openai.api_key = os.getenv('OPENAI_API_KEY')

# Database simulation (replace with actual database in production)
users_db = {}
rooms_db = {}
active_rooms = {}

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = users_db.get(data['user_id'])
            if not current_user:
                return jsonify({'message': 'Invalid token'}), 401
        except:
            return jsonify({'message': 'Invalid token'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# Routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    if data['username'] in users_db:
        return jsonify({'message': 'Username already exists'}), 400
    
    # Hash password
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    
    # Create user
    user_id = str(len(users_db) + 1)
    users_db[data['username']] = {
        'id': user_id,
        'username': data['username'],
        'password': hashed_password,
        'created_at': datetime.now().isoformat()
    }
    
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    user = users_db.get(data['username'])
    if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    # Generate token
    token = jwt.encode({
        'user_id': user['id'],
        'username': user['username'],
        'exp': datetime.utcnow().timestamp() + 3600
    }, app.config['SECRET_KEY'])
    
    return jsonify({
        'token': token,
        'user': {
            'id': user['id'],
            'username': user['username']
        }
    })

@app.route('/api/rooms', methods=['GET'])
@token_required
def get_rooms(current_user):
    return jsonify(list(active_rooms.values()))

@app.route('/api/rooms', methods=['POST'])
@token_required
def create_room(current_user):
    data = request.get_json()
    if not data or not data.get('name') or not data.get('topic'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    room_id = str(len(active_rooms) + 1)
    room = {
        'id': room_id,
        'name': data['name'],
        'topic': data['topic'],
        'host': current_user['username'],
        'participants': [current_user['username']],
        'created_at': datetime.now().isoformat()
    }
    active_rooms[room_id] = room
    
    return jsonify(room), 201

# WebSocket events
@socketio.on('join')
def on_join(data):
    room = data['room']
    username = data['username']
    join_room(room)
    if room in active_rooms:
        active_rooms[room]['participants'].append(username)
    emit('user_joined', {'username': username}, room=room)

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    username = data['username']
    leave_room(room)
    if room in active_rooms:
        active_rooms[room]['participants'].remove(username)
    emit('user_left', {'username': username}, room=room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    message = data['message']
    username = data['username']
    emit('new_message', {
        'username': username,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }, room=room)

# AI Tutor endpoints
@app.route('/api/ai/ask', methods=['POST'])
@token_required
def ask_ai(current_user):
    data = request.get_json()
    if not data or not data.get('question'):
        return jsonify({'message': 'Missing question'}), 400
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful study assistant."},
                {"role": "user", "content": data['question']}
            ]
        )
        return jsonify({
            'answer': response.choices[0].message.content
        })
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/ai/generate-questions', methods=['POST'])
@token_required
def generate_questions(current_user):
    data = request.get_json()
    if not data or not data.get('topic'):
        return jsonify({'message': 'Missing topic'}), 400
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Generate 5 study questions about the given topic."},
                {"role": "user", "content": f"Generate questions about: {data['topic']}"}
            ]
        )
        return jsonify({
            'questions': response.choices[0].message.content.split('\n')
        })
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Serve frontend
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    socketio.run(app, debug=True) 