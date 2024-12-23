from flask import Flask, request, Response, stream_with_context, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import subprocess
import json
import shlex
import os
import sys
import time
import logging
from gunicorn.app.base import BaseApplication
import psutil
import signal
import select
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import uuid
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')  # Change this in production!
jwt = JWTManager(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
MAX_BUFFER_SIZE = int(os.getenv('MAX_BUFFER_SIZE', 1e6))  # 1MB default
TIMEOUT = int(os.getenv('TIMEOUT', 600))  # 10 minutes default
VENV_PATH = os.getenv('VENV_PATH', '/home/ubuntu/kinos/venv/bin')
PROJECT_PATH = os.getenv('PROJECT_PATH', '/home/ubuntu/kinos')

# In-memory storage for patterns, users, and the community library
patterns = {}
users = {}
community_library = {}

class PatternVersion:
    def __init__(self, content):
        self.version_id = str(uuid.uuid4())
        self.content = content
        self.created_at = datetime.utcnow()

class Pattern:
    def __init__(self, name, content):
        self.id = str(uuid.uuid4())
        self.name = name
        self.versions = [PatternVersion(content)]

    @property
    def current_version(self):
        return self.versions[-1]

    def add_version(self, content):
        self.versions.append(PatternVersion(content))

def stream_command(command):
    env = os.environ.copy()
    env['PATH'] = f"{VENV_PATH}:{env['PATH']}"
    
    def generate():
        try:
            yield json.dumps({'debug': 'Starting command execution'}) + '\n'
            
            with subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True,
                cwd=PROJECT_PATH,
                env=env,
                preexec_fn=os.setsid
            ) as process:
                yield json.dumps({'debug': 'Process started'}) + '\n'
                
                start_time = time.time()
                output_buffer = ""
                while True:
                    if process.poll() is not None:
                        break
                    
                    # Use select to avoid blocking
                    rlist, _, _ = select.select([process.stdout, process.stderr], [], [], 0.1)
                    for stream in rlist:
                        line = stream.readline()
                        if line:
                            output_buffer += line
                            if len(output_buffer) > MAX_BUFFER_SIZE:
                                yield json.dumps({'debug': 'Buffer size limit reached'}) + '\n'
                                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                                return
                            yield json.dumps({'output' if stream == process.stdout else 'error': line.strip()}) + '\n'
                    
                    # Check timeout
                    if time.time() - start_time > TIMEOUT:
                        yield json.dumps({'debug': f'Process timed out after {TIMEOUT} seconds'}) + '\n'
                        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                        return
                
                return_code = process.returncode
                yield json.dumps({'debug': f'Process ended with return code {return_code}'}) + '\n'
        except Exception as e:
            logging.error(f"Error in stream_command: {str(e)}")
            yield json.dumps({'error': f'Internal server error: {str(e)}'}) + '\n'

    return generate()

@app.route('/', methods=['GET'])
def ping():
    return "PONG"

@app.route('/kinos', methods=['POST'])
def kinos():
    data = request.json
    command = shlex.split(data['command'])
    return Response(stream_with_context(stream_command(command)), content_type='application/json')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400
    if username in users:
        return jsonify({"error": "Username already exists"}), 400
    users[username] = generate_password_hash(password)
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400
    if username not in users or not check_password_hash(users[username], password):
        return jsonify({"error": "Invalid username or password"}), 401
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

@app.route('/api/patterns', methods=['GET'])
@jwt_required()
def get_patterns():
    return jsonify([{'id': p.id, 'name': p.name, 'version_count': len(p.versions)} for p in patterns.values()])

@app.route('/api/patterns', methods=['POST'])
@jwt_required()
def create_pattern():
    data = request.json
    pattern = Pattern(data['name'], data['content'])
    patterns[pattern.id] = pattern
    return jsonify({'id': pattern.id, 'name': pattern.name, 'version_id': pattern.current_version.version_id}), 201

@app.route('/api/patterns/<pattern_id>', methods=['GET'])
@jwt_required()
def get_pattern(pattern_id):
    pattern = patterns.get(pattern_id)
    if pattern:
        return jsonify({
            'id': pattern.id,
            'name': pattern.name,
            'content': pattern.current_version.content,
            'version_id': pattern.current_version.version_id,
            'version_count': len(pattern.versions)
        })
    return jsonify({'error': 'Pattern not found'}), 404

@app.route('/api/patterns/<pattern_id>', methods=['PUT'])
@jwt_required()
def update_pattern(pattern_id):
    pattern = patterns.get(pattern_id)
    if pattern:
        data = request.json
        pattern.name = data.get('name', pattern.name)
        if 'content' in data and data['content'] != pattern.current_version.content:
            pattern.add_version(data['content'])
        return jsonify({
            'id': pattern.id,
            'name': pattern.name,
            'version_id': pattern.current_version.version_id,
            'version_count': len(pattern.versions)
        })
    return jsonify({'error': 'Pattern not found'}), 404

@app.route('/api/patterns/<pattern_id>', methods=['DELETE'])
@jwt_required()
def delete_pattern(pattern_id):
    if pattern_id in patterns:
        del patterns[pattern_id]
        return '', 204
    return jsonify({'error': 'Pattern not found'}), 404

@app.route('/api/patterns/<pattern_id>/versions', methods=['GET'])
@jwt_required()
def get_pattern_versions(pattern_id):
    pattern = patterns.get(pattern_id)
    if pattern:
        return jsonify([{
            'version_id': v.version_id,
            'created_at': v.created_at.isoformat()
        } for v in pattern.versions])
    return jsonify({'error': 'Pattern not found'}), 404

@app.route('/api/patterns/<pattern_id>/versions/<version_id>', methods=['GET'])
@jwt_required()
def get_pattern_version(pattern_id, version_id):
    pattern = patterns.get(pattern_id)
    if pattern:
        version = next((v for v in pattern.versions if v.version_id == version_id), None)
        if version:
            return jsonify({
                'id': pattern.id,
                'name': pattern.name,
                'content': version.content,
                'version_id': version.version_id,
                'created_at': version.created_at.isoformat()
            })
        return jsonify({'error': 'Version not found'}), 404
    return jsonify({'error': 'Pattern not found'}), 404

@app.route('/api/patterns/<pattern_id>/copy', methods=['POST'])
@jwt_required()
def copy_pattern(pattern_id):
    if pattern_id in patterns:
        original_pattern = patterns[pattern_id]
        new_pattern = Pattern(f"Copy of {original_pattern.name}", original_pattern.current_version.content)
        patterns[new_pattern.id] = new_pattern
        return jsonify({
            'id': new_pattern.id,
            'name': new_pattern.name,
            'version_id': new_pattern.current_version.version_id
        }), 201
    return jsonify({'error': 'Pattern not found'}), 404

@app.route('/api/patterns/<pattern_id>/export', methods=['GET'])
@jwt_required()
def export_pattern(pattern_id):
    if pattern_id in patterns:
        # Placeholder for export logic
        return jsonify({'message': 'Export functionality not yet implemented'}), 501
    return jsonify({'error': 'Pattern not found'}), 404

# Community library endpoints
@app.route('/api/library', methods=['GET'])
@jwt_required()
def get_library():
    return jsonify(list(community_library.values()))

@app.route('/api/library/<pattern_id>', methods=['POST'])
@jwt_required()
def add_to_library(pattern_id):
    if pattern_id in patterns:
        pattern = patterns[pattern_id]
        community_library[pattern_id] = {
            'id': pattern.id,
            'name': pattern.name,
            'version_count': len(pattern.versions),
            'added_by': get_jwt_identity()
        }
        return jsonify(community_library[pattern_id]), 201
    return jsonify({'error': 'Pattern not found'}), 404

@app.route('/api/library/<pattern_id>', methods=['DELETE'])
@jwt_required()
def remove_from_library(pattern_id):
    if pattern_id in community_library:
        del community_library[pattern_id]
        return '', 204
    return jsonify({'error': 'Pattern not found in the library'}), 404

# Pattern merging feature
@app.route('/api/patterns/merge', methods=['POST'])
@jwt_required()
def merge_patterns():
    merge_data = request.json
    pattern1_id = merge_data['pattern1_id']
    pattern2_id = merge_data['pattern2_id']
    
    pattern1 = patterns.get(pattern1_id)
    pattern2 = patterns.get(pattern2_id)
    
    if not pattern1 or not pattern2:
        return jsonify({'error': 'One or both patterns not found'}), 404
    
    # Simple merging algorithm: concatenate the content of both patterns
    merged_content = pattern1.current_version.content + pattern2.current_version.content
    
    merged_pattern = Pattern(f"Merged: {pattern1.name} + {pattern2.name}", merged_content)
    patterns[merged_pattern.id] = merged_pattern
    
    return jsonify({
        'id': merged_pattern.id,
        'name': merged_pattern.name,
        'version_id': merged_pattern.current_version.version_id
    }), 201

class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.application = app
        self.options = options or {}
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key, value)

    def load(self):
        return self.application

if __name__ == '__main__':
    options = {
        'bind': os.getenv('BIND', '0.0.0.0:8501'),
        'workers': int(os.getenv('WORKERS', 4)),
        'timeout': TIMEOUT,
        'worker_class': 'gevent',
        'capture_output': True,
        'loglevel': 'warning',
    }
    print("Starting Gunicorn with options:", options)
    StandaloneApplication(app, options).run()
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import json
import uuid

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this in production!
jwt = JWTManager(app)

# In-memory storage for patterns, users, and the community library
patterns = {}
users = {}
community_library = {}

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400
    if username in users:
        return jsonify({"error": "Username already exists"}), 400
    users[username] = generate_password_hash(password)
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400
    if username not in users or not check_password_hash(users[username], password):
        return jsonify({"error": "Invalid username or password"}), 401
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

@app.route('/api/patterns', methods=['GET'])
@jwt_required()
def get_patterns():
    return jsonify(list(patterns.values()))

@app.route('/api/patterns', methods=['POST'])
@jwt_required()
def create_pattern():
    pattern = request.json
    pattern_id = str(uuid.uuid4())
    pattern['id'] = pattern_id
    patterns[pattern_id] = pattern
    return jsonify(pattern), 201

@app.route('/api/patterns/<pattern_id>', methods=['GET'])
@jwt_required()
def get_pattern(pattern_id):
    pattern = patterns.get(pattern_id)
    if pattern:
        return jsonify(pattern)
    return jsonify({'error': 'Pattern not found'}), 404

@app.route('/api/patterns/<pattern_id>', methods=['PUT'])
@jwt_required()
def update_pattern(pattern_id):
    if pattern_id in patterns:
        pattern = request.json
        pattern['id'] = pattern_id
        patterns[pattern_id] = pattern
        return jsonify(pattern)
    return jsonify({'error': 'Pattern not found'}), 404

@app.route('/api/patterns/<pattern_id>', methods=['DELETE'])
@jwt_required()
def delete_pattern(pattern_id):
    if pattern_id in patterns:
        del patterns[pattern_id]
        return '', 204
    return jsonify({'error': 'Pattern not found'}), 404

@app.route('/api/patterns/<pattern_id>/copy', methods=['POST'])
@jwt_required()
def copy_pattern(pattern_id):
    if pattern_id in patterns:
        new_pattern = dict(patterns[pattern_id])
        new_pattern_id = str(uuid.uuid4())
        new_pattern['id'] = new_pattern_id
        patterns[new_pattern_id] = new_pattern
        return jsonify(new_pattern), 201
    return jsonify({'error': 'Pattern not found'}), 404

@app.route('/api/patterns/<pattern_id>/export', methods=['GET'])
@jwt_required()
def export_pattern(pattern_id):
    if pattern_id in patterns:
        # Placeholder for export logic
        return jsonify({'message': 'Export functionality not yet implemented'}), 501
    return jsonify({'error': 'Pattern not found'}), 404

# Community library endpoints
@app.route('/api/library', methods=['GET'])
@jwt_required()
def get_library():
    return jsonify(list(community_library.values()))

@app.route('/api/library/<pattern_id>', methods=['POST'])
@jwt_required()
def add_to_library(pattern_id):
    if pattern_id in patterns:
        pattern = patterns[pattern_id]
        community_library[pattern_id] = pattern
        return jsonify(pattern), 201
    return jsonify({'error': 'Pattern not found'}), 404

@app.route('/api/library/<pattern_id>', methods=['DELETE'])
@jwt_required()
def remove_from_library(pattern_id):
    if pattern_id in community_library:
        del community_library[pattern_id]
        return '', 204
    return jsonify({'error': 'Pattern not found in the library'}), 404

if __name__ == '__main__':
    app.run(debug=True)
