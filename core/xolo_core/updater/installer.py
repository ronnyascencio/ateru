import subprocess
import sys


def run_update() -> None:
    """
    Update Xolo Pipeline using git.
    """
    try:
        subprocess.check_call(["git", "pull", "--rebase"])
        print("✔ Xolo Pipeline updated. Please restart.")
    except Exception as exc:
        print("✖ Update failed:", exc)
        sys.exit(1)
