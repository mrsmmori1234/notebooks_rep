#!/bin/bash

echo "🔎 Checking for running Jupyter Lab processes..."

# Jupyter Labが起動しているか確認
if pgrep -f "jupyter-lab" > /dev/null; then
    echo "🛑 Stopping Jupyter Lab..."
    # Attempt to stop gracefully (SIGTERM)
    pkill -f "jupyter-lab" 2>/dev/null

    # Wait a few seconds for cleanup
    sleep 3

    # If still running, attempt to force kill (SIGKILL)
    if pgrep -f "jupyter-lab" > /dev/null; then
        echo "⚠️ Still running. Attempting force kill (SIGKILL)..."
        pkill -9 -f "jupyter-lab" 2>/dev/null
        sleep 2
    fi

    if pgrep -f "jupyter-lab" > /dev/null; then
        echo "❌ Failed to stop Jupyter Lab. Please check manually."
    else
        echo "✅ Jupyter Lab stopped successfully."
    fi
else
    echo "🤷‍♀️ Jupyter Lab is not running."
fi