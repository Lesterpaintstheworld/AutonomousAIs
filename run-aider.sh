#!/bin/bash

VENV_PATH=~/synthetic-souls/venv
CUSTOM_AIDER_PATH=~/synthetic-souls/aider
MAX_ATTEMPTS=5
LOGFILE=~/aider_log.txt
OUTPUT_LOG=~/aider_output.log

source $VENV_PATH/bin/activate

# Add the custom aider path to PYTHONPATH
export PYTHONPATH=$CUSTOM_AIDER_PATH:$PYTHONPATH

run_aider() {
    python -m aider --cache-prompts --gui --no-check-update  --test-cmd "python -m main" --auto-test true "$@" >> $OUTPUT_LOG 2>&1
}

attempt=0
while [ $attempt -lt $MAX_ATTEMPTS ]; do
    attempt=$((attempt+1))
    echo "$(date): Starting custom aider (attempt $attempt of $MAX_ATTEMPTS)" >> $LOGFILE
    run_aider "$@"
    exit_code=$?

    if [ $exit_code -ne 0 ]; then
        echo "$(date): Custom Aider exited with code $exit_code. Restarting in 5 seconds..." >> $LOGFILE
        sleep 5
    else
        echo "$(date): Custom Aider exited normally. Stopping the script." >> $LOGFILE
        break
    fi
done

if [ $attempt -eq $MAX_ATTEMPTS ]; then
    echo "$(date): Reached maximum number of restart attempts. Please check the application." >> $LOGFILE
fi

deactivate
