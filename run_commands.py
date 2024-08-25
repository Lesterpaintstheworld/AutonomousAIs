import subprocess

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(f"Command executed successfully: {command}")
        print(f"Output:\n{result.stdout}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Error message: {e}")
        print(f"Error output:\n{e.output}")
        return None

def run_commands():
    # Add your commands here
    commands = [
        "echo Hello, Infinite Storyteller!",
        "python --version",
        # Add more commands as needed
    ]
    
    for command in commands:
        run_command(command)

if __name__ == "__main__":
    run_commands()
