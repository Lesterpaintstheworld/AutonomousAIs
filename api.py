from flask import Flask, request, Response, stream_with_context
import subprocess
import json
import shlex
import os
import sys

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8501, threaded=True)
