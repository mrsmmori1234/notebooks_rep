import os
import subprocess
import shutil
import datetime
import sys

# --- Configuration ---
PYENV_ENV = "notebooks-env"
LOG_DIR = os.path.expanduser("~/notebooks/log")
PYENV_ROOT = os.environ.get("PYENV_ROOT", os.path.expanduser("~/notebooks/.pyenv"))
JUPYTER_PATH = f"{PYENV_ROOT}/versions/{PYENV_ENV}/bin/jupyter-lab"

def launch_jupyter():
    # 1. Check Jupyter executable
    if not os.path.exists(JUPYTER_PATH):
        print(f"❌ Error: Jupyter Lab not found in {PYENV_ENV}")
        print(f"Path: {JUPYTER_PATH}")
        sys.exit(1)

    # 2. Prevent double execution
    try:
        check_proc = subprocess.run(["pgrep", "-f", "jupyter-lab"], capture_output=True)
        if check_proc.returncode == 0:
            print("⚠️ Jupyter Lab is already running. Nothing to do.")
            return
    except Exception as e:
        pass

    # 3. Create log directory
    os.makedirs(LOG_DIR, exist_ok=True)

    # 4. Log filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_path = os.path.join(LOG_DIR, f"jupyterlab_{timestamp}.log")

    # 5. Launch
    print(f"🚀 Launching Jupyter Lab...")
    try:
        with open(log_file_path, "w") as log_file:
            subprocess.Popen(
                [JUPYTER_PATH],
                stdout=log_file,
                stderr=subprocess.STDOUT,
                preexec_fn=os.setpgrp
            )
        print(f"✅ Launch Jupyter successful (log: {log_file_path})")
    except Exception as e:
        print(f"❌ Launch Jupyter failed: {e}")

if __name__ == "__main__":
    launch_jupyter()