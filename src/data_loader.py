import glob
from pathlib import Path
import pandas as pd

# Project root (~/notebooks)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

def find_latest_file(pattern: str, base_dir: Path | None = None) -> Path:
    """Returns the path of the latest file matching the specified pattern (e.g., 'Stock Screener*.csv')"""
    search_dir = base_dir if base_dir else PROJECT_ROOT / "Win_Downloads"
    full_pattern = str(search_dir / pattern)
    files = glob.glob(full_pattern)
    
    if not files:
        raise FileNotFoundError(f"No files matching pattern '{pattern}' found in {search_dir}")
        
    # Identify the latest file by timestamp (or string order)
    return Path(max(files, key=Path).strip())

def load_local_data(pattern: str, base_dir: Path | None = None, **kwargs) -> pd.DataFrame:
    """
    General-purpose function to automatically identify the extension (.csv / .xlsx / .xls) and load the latest file.
    Arguments passed to pandas read_* (e.g., skiprows, usecols, na_values) can be specified via kwargs.
    """
    file_path = find_latest_file(pattern, base_dir)
    print(f"Loading: {file_path}")
    
    suffix = file_path.suffix.lower()
    
    if suffix == '.csv':
        return pd.read_csv(file_path, **kwargs)
    elif suffix in ['.xlsx', '.xls']:
        return pd.read_excel(file_path, **kwargs)
    else:
        raise ValueError(f"Unsupported file format: {suffix}")