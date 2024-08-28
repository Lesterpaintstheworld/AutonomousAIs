import subprocess
import sys

def run_aider_nova(message):
    cmd = [
        sys.executable, 
        "-m", 
        "aider_nova", 
        "--yes", 
        "--test-cmd", 
        "python -m main", 
        "--auto-test", 
        "true", 
        "--cache-prompts", 
        "--message", 
        message
    ]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    full_output = ""
    for line in process.stdout:
        print(line, end='')  # Print the output in real-time
        full_output += line
    
    process.wait()
    return full_output

message = 'Work autonomously on what you think should be done'

while True:
    print(f"Running aider_nova with message: {message}")
    output = run_aider_nova(message)
    print(f"Output: {output}")
    
    # Use the full output as the next message
    message = output.strip()