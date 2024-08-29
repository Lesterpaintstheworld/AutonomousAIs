#!/usr/bin/env bash

# Function to create and activate a virtual environment
create_and_activate_venv() {
    local path=$1
    if [ -d "$path" ]; then
        echo "Virtual environment already exists at $path. Skipping creation."
    else
        echo "Creating virtual environment at $path..."
        python3 -m venv "$path" || { echo "Failed to create virtual environment at $path"; exit 1; }
    fi
    echo "Activating virtual environment..."
    source "$path/bin/activate" || { echo "Failed to activate virtual environment at $path"; exit 1; }
}

# Function to create an Aider function and alias
create_aider_function() {
    local name=$1
    local path=$2
    local function_name="run_${name//-/_}"
    local function_content='
    '"$function_name"'() {
        echo "Activating '"$name"' environment..."
        export VIRTUAL_ENV="'"$path"'"
        export PATH="'"$path"'/bin:$PATH"
        python_path="'"$path"'/bin/python"
        echo "Using Python executable: $python_path"
        echo "Running '"$name"' with arguments: $@"
        "$python_path" -m aider "$@"
        echo "'"$name"' execution completed."
    }
    '
    eval "$function_content"
    alias "$name"="$function_name"
    echo "Function and alias for $name created/updated."
}

# Main script
instances=("aider_nova" "aider_vox" "aider_lyra")
for instance in "${instances[@]}"; do
    echo "Setting up $instance..."

    venv_path="$HOME/synthetic-souls/venv_$instance"
    repo_path="$HOME/synthetic-souls"

    # Create and activate virtual environment
    create_and_activate_venv "$venv_path"

    # Update pip and setuptools
    pip install --upgrade pip setuptools wheel

    # Update the existing repository
    echo "Updating Aider repository..."
    cd "$repo_path"
    git pull

    # Install or update Aider and its dependencies
    echo "Installing/Updating Aider and dependencies..."

    if [ -f "requirements.txt" ]; then
        echo "Installing from requirements.txt..."
        pip install -r requirements.txt
    else
        echo "No requirements.txt found. Installing aider-chat manually."
        pip install aider-chat
    fi

    # Install additional dependencies
    pip install GitPython python-dotenv prompt_toolkit PyYAML

    # Verify Python version in this venv
    echo "Verifying Python version for ${instance}:"
    "$venv_path/bin/python" --version

    # Create function and alias
    create_aider_function "$instance" "$venv_path"

    # Deactivate virtual environment
    deactivate
    echo "Setup for $instance completed successfully."
    echo "--------------------------------------------------"

    echo "Setup complete. You can now use the $instance alias."

    # Add this to your Bash profile
    profile_content="
    # Aider function and alias for $instance
    $(declare -f create_aider_function)
    $(declare -f run_${instance//-/_})
    alias $instance='run_${instance//-/_}'
    "

    echo "$profile_content" >> "$HOME/.bashrc"
done

echo "Setup script has been added to your Bash profile for all instances. Please restart your terminal or run 'source ~/.bashrc' to use the new functions and aliases."
