import sys
from pathlib import Path

nuke_path_dir = Path(os.environ.get("PROJECT_ROOT")) / "dcc" / "nuke"
if str(nuke_path_dir) not in sys.path:
    sys.path.insert(0, str(nuke_path_dir))

try:
    import menu
except Exception as e:
    print(f"Failed to load Xolo menu: {e}")
