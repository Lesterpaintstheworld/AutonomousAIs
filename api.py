from flask import Flask, request, Response, stream_with_context
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

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
MAX_BUFFER_SIZE = int(os.getenv('MAX_BUFFER_SIZE', 1e6))  # 1MB default
TIMEOUT = int(os.getenv('TIMEOUT', 600))  # 10 minutes default
VENV_PATH = os.getenv('VENV_PATH', '/home/ubuntu/kinos/venv/bin')
PROJECT_PATH = os.getenv('PROJECT_PATH', '/home/ubuntu/kinos')

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
    try:
        data = request.json
        agent = data.get('agent')
        message = data.get('message')
        mission = data.get('mission')
        
        command = [f'{VENV_PATH}/python', '-m', 'aider']
        
        if agent:
            command.extend(['--agent', secure_filename(agent)])
        
        if input:
            command.extend(['--input', shlex.quote(input)])
       
        if mission:
            command.extend(['--mission', mission])
        
        # Log the full command for debugging
        logging.debug(f"Executing command: {' '.join(command)}")
        
        return Response(stream_with_context(stream_command(command)), mimetype='application/json')
    except Exception as e:
        logging.error(f"Error in kinos endpoint: {str(e)}", exc_info=True)
        return Response(json.dumps({'error': f'Internal server error: {str(e)}'}), status=500, mimetype='application/json')

@app.route('/health', methods=['GET'])
def health():
    try:
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        return Response(json.dumps({
            'cpu': cpu_usage,
            'memory': memory_usage,
            'disk': disk_usage
        }), mimetype='application/json')
    except Exception as e:
        logging.error(f"Error in health endpoint: {str(e)}")
        return Response(json.dumps({'error': f'Internal server error: {str(e)}'}), status=500, mimetype='application/json')

class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)

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

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this in production!
jwt = JWTManager(app)

# In-memory storage for patterns and users (replace with database in production)
patterns = []
users = {}

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
    return jsonify(patterns), 200

@app.route('/api/patterns', methods=['POST'])
@jwt_required()
def create_pattern():
    new_pattern = request.json
    if not new_pattern:
        return jsonify({"error": "Invalid pattern data"}), 400
    patterns.append(new_pattern)
    return jsonify(new_pattern), 201

@app.route('/api/patterns/<int:pattern_id>', methods=['GET'])
@jwt_required()
def get_pattern(pattern_id):
    if 0 <= pattern_id < len(patterns):
        return jsonify(patterns[pattern_id]), 200
    return jsonify({"error": "Pattern not found"}), 404

@app.route('/api/patterns/<int:pattern_id>', methods=['PUT'])
@jwt_required()
def update_pattern(pattern_id):
    if 0 <= pattern_id < len(patterns):
        updated_pattern = request.json
        if not updated_pattern:
            return jsonify({"error": "Invalid pattern data"}), 400
        patterns[pattern_id] = updated_pattern
        return jsonify(patterns[pattern_id]), 200
    return jsonify({"error": "Pattern not found"}), 404

@app.route('/api/patterns/<int:pattern_id>', methods=['DELETE'])
@jwt_required()
def delete_pattern(pattern_id):
    if 0 <= pattern_id < len(patterns):
        deleted_pattern = patterns.pop(pattern_id)
        return jsonify(deleted_pattern), 200
    return jsonify({"error": "Pattern not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
