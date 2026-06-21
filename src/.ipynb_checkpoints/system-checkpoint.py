import subprocess
import sys

def run_commands(commands: list[str], executable: str = "/bin/bash") -> bool:
    """
    General-purpose engine to execute multiple specified shell commands by joining them with ' && ',
    displaying stdout and stderr in real-time.
    
    :param commands: List of shell commands to execute (strings)
    :param executable: Shell to use (defaults to /bin/bash)
    :return: True if all commands succeed (exit code 0), False if any fail
    """
    if not commands:
        print("⚠️ No commands specified for execution.")
        return False

    current_cmd = ""
    
    try:
        for cmd in commands:
            # Concatenate commands (link with && to maintain state)
            if current_cmd:
                current_cmd += " && " + cmd
            else:
                current_cmd = cmd
                
            print(f"▶ Running: {cmd}")
            
            # Start subprocess
            # Separate stdout and stderr to handle error output explicitly
            process = subprocess.Popen(
                current_cmd,
                shell=True,
                executable=executable,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1 # Line buffering
            )
            
            # Read stdout and stderr concurrently in real-time
            # Simple line-by-line reading for immediate feedback in Jupyter
            while True:
                stdout_line = process.stdout.readline()
                if stdout_line:
                    print(stdout_line.strip())
                    sys.stdout.flush()
                
                stderr_line = process.stderr.readline()
                if stderr_line:
                    print(f"[Error Output]: {stderr_line.strip()}")
                    sys.stderr.flush()
                
                if stdout_line == '' and stderr_line == '' and process.poll() is not None:
                    break
            
            returncode = process.poll()
            
            if returncode != 0:
                print(f"❌ Failed: Stopped with exit code {returncode}.")
                return False
                
        print("✨ All processes completed successfully.")
        return True
        
    except Exception as e:
        print(f"🚨 An unexpected system error occurred: {e}")
        return False