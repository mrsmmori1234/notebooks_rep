#!/bin/bash

echo "🔎 Checking for running Jupyter Lab processes..."

# Jupyter Labが起動しているか確認
if pgrep -f "jupyter-lab" > /dev/null; then
    echo "🛑 Stopping Jupyter Lab..."
    # プロセスを停止
    pkill -f "jupyter-lab"

    # 少し待ってから再度確認
    sleep 2

    if pgrep -f "jupyter-lab" > /dev/null; then
        echo "❌ Failed to stop Jupyter Lab. Please check manually."
    else
        echo "✅ Jupyter Lab stopped successfully."
    fi
else
    echo "🤷‍♀️ Jupyter Lab is not running."
fi