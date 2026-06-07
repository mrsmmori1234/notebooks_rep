import sys
from pathlib import Path

# 1. Automatically add the project root to sys.path (Countermeasure for Jupyter hierarchy)
# The grandparent directory of this file (src/env_setup.py) is the root (~/notebooks)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# 2. Function to globally inject basic data analysis and visualization libraries
def init_analysis_env():
    """Imports major libraries into the Notebook's global namespace"""
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from src.data_loader import load_local_data
    from pathlib import Path
    from src.data_loader import load_local_data
    
    # Inject imports directly into the caller's Jupyter environment (__main__)
    import __main__
    setattr(__main__, 'pd', pd)
    setattr(__main__, 'np', np)
    setattr(__main__, 'plt', plt)
    setattr(__main__, 'sns', sns)
    setattr(__main__, 'load_local_data', load_local_data)
    
    # Apply basic styles or configurations (e.g., Japanese font support)
    sns.set_theme(style="darkgrid")
    
    print("🚀 Analysis environment initialized: pd, np, plt, sns, load_local_data are ready.")