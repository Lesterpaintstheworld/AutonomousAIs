#!/bin/bash

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the required packages
pip install -r requirements.txt

# Set up the OpenAI API key
echo "Please enter your OpenAI API key:"
read api_key
echo "export OPENAI_API_KEY='$api_key'" >> venv/bin/activate

echo "Installation complete. To start using the project, run 'source venv/bin/activate' to activate the virtual environment."
