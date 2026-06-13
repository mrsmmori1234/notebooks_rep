import sys
from pathlib import Path
import os
from google import genai
from typing import Any
from IPython.core.getipython import get_ipython
from IPython.display import display, Markdown

# --- Configuration ---
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# 1. Project Root & Path Setup
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Enable autoreload if running in an IPython/Jupyter environment
ip: Any = get_ipython()
if ip:
    ip.run_line_magic('load_ext', 'autoreload')
    ip.run_line_magic('autoreload', '2')

# 2. Function to globally inject basic data analysis and visualization libraries
def init_analysis_env():
    """Imports major libraries into the Notebook's global namespace"""
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import yfinance as yf
    from src.data_loader import load_local_data
    from src.gemini_helper import ai
    
    # Mapping for easier maintenance of injected libraries
    libs = {
        'pd': pd,
        'np': np,
        'yf': yf,
        'plt': plt,
        'sns': sns,
        'load_local_data': load_local_data,
        'ai': ai,
    }

    # Inject imports directly into the caller's Jupyter environment (__main__)
    import __main__
    for name, obj in libs.items():
        setattr(__main__, name, obj)
    
    # Apply basic styles or configurations
    sns.set_theme(style="darkgrid")
    
    print(f"🚀 Analysis environment initialized: {', '.join(libs.keys())} are ready.")

def _gemini_magic_handler(line, cell):
    """Internal handler for the %%gemini magic command."""
    try:
        client = genai.Client()  # Uses GEMINI_API_KEY environment variable
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=cell,
        )
        display(Markdown(response.text))
    except Exception as e:
        print(f"❌ Error in %%gemini: {e}")

def setup_gemini_magic():
    """Enables the %%gemini magic command within Jupyter."""
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️ GEMINI_API_KEY env variable not found. %%gemini magic disabled.")
        return

    if ip:
        ip.register_magic_function(_gemini_magic_handler, 'cell', 'gemini')
    # Silent fail if not in IPython environment