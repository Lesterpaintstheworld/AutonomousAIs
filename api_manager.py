#!/usr/bin/env python3
import os
import sys
import subprocess
import signal
import time
import psutil

# Configuration
HOME_DIR = os.path.expanduser("~")
PROJECT_DIR = os.path.join(HOME_DIR, "synthetic-souls")
VENV_DIR = os.path.join(PROJECT_DIR, "venv")
VENV_PYTHON = os.path.join(VENV_DIR, "bin", "python")
API_SCRIPT = "api.py"
PID_FILE = os.path.join(PROJECT_DIR, "api_pid.txt")
LOG_FILE = os.path.join(PROJECT_DIR, "api.log")

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
        
        with open(LOG_FILE, 'w') as log:
            process = subprocess.Popen(command, shell=True, preexec_fn=os.setsid, stdout=log, stderr=log)
        
        # Wait a short time to check if the process is still running
        time.sleep(2)
        if process.poll() is None:
            with open(PID_FILE, "w") as f:
                f.write(str(process.pid))
            print(f"API started. PID: {process.pid}")
        else:
            with open(LOG_FILE, 'r') as log:
                print(f"Error starting API. Log contents:")
                print(log.read())
    except Exception as e:
        print(f"Error starting API: {e}")

def stop_api():
    if not os.path.isfile(PID_FILE):
        print("API is not running.")
        return
    with open(PID_FILE, "r") as f:
        pid = int(f.read().strip())
    try:
        parent = psutil.Process(pid)
        for child in parent.children(recursive=True):
            child.terminate()
        parent.terminate()
        parent.wait(10)  # Wait up to 10 seconds for the process to terminate
        os.remove(PID_FILE)
        print("API stopped.")
    except psutil.NoSuchProcess:
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
            process = psutil.Process(pid)
            print(f"API is running. PID: {pid}")
            print(f"CPU Usage: {process.cpu_percent()}%")
            print(f"Memory Usage: {process.memory_info().rss / 1024 / 1024:.2f} MB")
            print(f"Running Time: {time.time() - process.create_time():.2f} seconds")
            print("Last 10 lines of log:")
            with open(LOG_FILE, 'r') as log:
                lines = log.readlines()
                for line in lines[-10:]:
                    print(line.strip())
        except psutil.NoSuchProcess:
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
