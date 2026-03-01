#!/bin/bash

# pyenv 初期化（必要に応じて）
export PATH="$HOME/.pyenv/bin:$PATH"
if command -v pyenv 1>/dev/null 2>&1; then
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
else
    echo "❌ pyenv not found!"
    exit 1
fi

# 使用する pyenv 仮想環境名
PYENV_ENV="notebooks-env"

# 仮想環境に切り替え
pyenv activate "$PYENV_ENV"
if [ $? -ne 0 ]; then
    echo "❌ Failed to activate pyenv environment: $PYENV_ENV"
    exit 1
fi

# Jupyter Lab がすでに起動しているか確認
if pgrep -f "jupyter-lab" > /dev/null; then
    echo "⚠️ Jupyter Lab is already running. Nothing to do."
    exit 0
fi

# ログディレクトリ作成
mkdir -p "$HOME/notebooks/log"

# タイムスタンプ付きログファイル
timestamp=$(date +"%Y%m%d_%H%M%S")
logfile="$HOME/notebooks/log/jupyterlab_$timestamp.log"

# Jupyter Lab 起動（nohupでバックグラウンド実行）
nohup jupyter lab > "$logfile" 2>&1 &

if [ $? -eq 0 ]; then
    echo "✅ Launch Jupyter successful (log: $logfile)"
    echo "⏳ Waiting for Jupyter to start..."
    sleep 5
    echo "📋 Jupyter Server List:"
    jupyter server list
else
    echo "❌ Launch Jupyter failed"
fi
