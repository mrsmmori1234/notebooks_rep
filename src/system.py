import subprocess
import sys

def run_commands(commands: list[str], executable: str = "/bin/bash") -> bool:
    """
    指定された複数のシェルコマンドを ' && ' で1つのセッションとして結合し、
    stdout と stderr をリアルタイムで完全に同期して表示するエンジン。
    """
    if not commands:
        print("⚠️ No commands specified for execution.")
        return False

    # 1. すべてのコマンドをはじめから1本の独立したタイムラインに結合する
    # これにより、仮想環境の有効化(source)や移動(cd)の状態が最後まで維持されます
    full_command = " && ".join(commands)
    
    print(f"▶ Execution Started:\n   " + "\n   ➔ ".join(commands))
    print("-" * 50)
    
    try:
        # 2. stdoutとstderrを現在のJupyter/ターミナル画面に直接結合（パススルー）
        # PIPEでPythonに吸い込ませないため、デッドロックが100%発生せず、
        # コマンドを直接叩いたときと完全に同じリアルタイムログが出力されます。
        process = subprocess.Popen(
            full_command,
            shell=True,
            executable=executable,
            stdout=None,  # Noneにすることで現在のターミナルに出力を直結
            stderr=None   # エラー出力も同様に直結
        )
        
        # プロセスの完了を待つ（Jupyter側でもリアルタイムでログが流れます）
        process.wait()
        
        print("-" * 50)
        if process.returncode != 0:
            print(f"❌ Failed: Stopped with exit code {process.returncode}.")
            return False
            
        print("✨ All processes completed successfully.")
        return True
        
    except Exception as e:
        print(f"🚨 An unexpected system error occurred: {e}")
        return False