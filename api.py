from flask import Flask, request, Response, stream_with_context
import subprocess
import json
import shlex
import os
import sys
from gunicorn.app.base import BaseApplication

app = Flask(__name__)

def stream_command(command):
    env = os.environ.copy()
    env['PATH'] = f"/home/ubuntu/synthetic-souls/venv/bin:{env['PATH']}"
    
    def generate():
        yield json.dumps({'debug': 'Starting command execution'}) + '\n'
        
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            cwd="/home/ubuntu/synthetic-souls",
            env=env
        )
        
        yield json.dumps({'debug': 'Process started'}) + '\n'
        
        while True:
            output = process.stdout.readline()
            error = process.stderr.readline()
            
            if output:
                yield json.dumps({'output': output.strip()}) + '\n'
            if error:
                yield json.dumps({'error': error.strip()}) + '\n'
            
            if output == '' and error == '' and process.poll() is not None:
                break
        
        return_code = process.poll()
        yield json.dumps({'debug': f'Process ended with return code {return_code}'}) + '\n'
    return generate()

@app.route('/', methods=['GET'])
def ping():
    return "PONG"

@app.route('/kinos', methods=['GET'])
def kinos():
    role = request.args.get('role')
    user_request = request.args.get('request')
    folder = request.args.get('folder')
    
    if not role:
        return Response(json.dumps({'error': 'Role parameter is required'}), status=400, mimetype='application/json')
    
    command = ['/home/ubuntu/synthetic-souls/venv/bin/python', '-m', 'aider', '--role', role]
    
    if user_request:
        command.extend(['--request', shlex.quote(user_request)])
    
    if folder:
        command.extend(['--folder', shlex.quote(folder)])
    
    return Response(stream_with_context(stream_command(command)), mimetype='application/json')

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
        'bind': '0.0.0.0:8501',
        'workers': 4,
        'timeout': 600,  # 10 minutes in seconds
        'worker_class': 'gevent',
    }
    StandaloneApplication(app, options).run()
