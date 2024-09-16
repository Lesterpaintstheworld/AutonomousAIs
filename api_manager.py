#!/usr/bin/env python3

import os
import sys
import subprocess
import signal
import time

# Configuration
HOME_DIR = os.path.expanduser("~")
PROJECT_DIR = os.path.join(HOME_DIR, "synthetic-souls")
VENV_DIR = os.path.join(PROJECT_DIR, "venv")
VENV_PYTHON = os.path.join(VENV_DIR, "bin", "python")
API_SCRIPT = "api.py"
PID_FILE = os.path.join(PROJECT_DIR, "api_pid.txt")

def run_command(command, shell=False):
    process = subprocess.Popen(command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr

def start_api():
    if os.path.isfile(PID_FILE):
        print("API is already running.")
        return

    try:
        os.chdir(PROJECT_DIR)
        command = f"{VENV_PYTHON} {API_SCRIPT}"
        
        process = subprocess.Popen(command, shell=True, preexec_fn=os.setsid, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a short time to check if the process is still running
        time.sleep(2)
        if process.poll() is None:
            with open(PID_FILE, "w") as f:
                f.write(str(process.pid))
            print(f"API started. PID: {process.pid}")
        else:
            stdout, stderr = process.communicate()
            print(f"Error starting API. Exit code: {process.returncode}")
            print(f"stdout: {stdout.decode()}")
            print(f"stderr: {stderr.decode()}")
    except Exception as e:
        print(f"Error starting API: {e}")

def stop_api():
    if not os.path.isfile(PID_FILE):
        print("API is not running.")
        return

    with open(PID_FILE, "r") as f:
        pid = int(f.read().strip())

    try:
        os.killpg(os.getpgid(pid), signal.SIGTERM)
        os.remove(PID_FILE)
        print("API stopped.")
    except ProcessLookupError:
        print("API process not found. Removing PID file.")
        os.remove(PID_FILE)
    except Exception as e:
        print(f"Error stopping API: {e}")

def restart_api():
    stop_api()
    time.sleep(2)  # Wait for the process to fully stop
    start_api()

def check_status():
    if os.path.isfile(PID_FILE):
        with open(PID_FILE, "r") as f:
            pid = int(f.read().strip())
        try:
            os.kill(pid, 0)  # Check if the process is running
            print(f"API is running. PID: {pid}")
        except ProcessLookupError:
            print("API process not found, but PID file exists. Cleaning up.")
            os.remove(PID_FILE)
        except Exception as e:
            print(f"Error checking API status: {e}")
    else:
        print("API is not running.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python api_manager.py [start|stop|restart|status]")
        sys.exit(1)

    action = sys.argv[1].lower()

    if action == "start":
        start_api()
    elif action == "stop":
        stop_api()
    elif action == "restart":
        restart_api()
    elif action == "status":
        check_status()
    else:
        print("Invalid action. Use start, stop, restart, or status.")
