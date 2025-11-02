from pathlib import Path
from core.xolo_core.extractors.system_extractor import get_os_type

"""Global DCC generator functions."""


def get_system_root() -> Path:
    """
    Returns root path depending of OS:
    - Windows → C:\
    - macOS → /Applications/
    - Linux → /opt/

    """
    try:
        system = get_os_type().lower()

        if system == "windows":
            # look for the system drive (normally C:)
            drive = Path.home().drive
            if not drive:
                raise RuntimeError("Can't determine system drive in  Windows.")
            root = Path(drive + "\\")
        elif system == "darwin":
            root = Path("/Applications")
        elif system == "linux":
            root = Path("/opt")
        else:
            raise OSError(f"Unsuported system: {system}")

        # Root Validation
        if not root.exists():
            raise FileNotFoundError(f"Root Path does not exist: {root}")

        return root

    except Exception as e:
        print(f"⚠️ Error to optain root system: {e}")
        # home path secure return as fallback
        return Path.home()


def find_dcc_path(dcc_name: str) -> Path:
    """
    Search for a DCC by name in the system's app root.
    Special case for Nuke: searches inside 'nuke_installs/' for latest version.
    """
    apps_root = get_system_root()
    dcc_name = dcc_name.lower()
    candidates = [dcc_name, dcc_name.capitalize(), dcc_name.upper()]

    try:
        # --- Special case: Nuke autodiscovery ---
        if dcc_name == "nuke":
            nuke_root = apps_root / "nuke_installs"
            if not nuke_root.exists():
                raise print(f"Folder not found: {nuke_root}")

            # lookfor versions
            versions = [
                d
                for d in nuke_root.iterdir()
                if d.is_dir() and d.name.lower().startswith("nuke")
            ]
            if not versions:
                raise print(f"No versions found of Nuke in {nuke_root}")

            # lastest verssion
            latest = sorted(versions, reverse=True)[0]
            print(f"✅ Nuke Found: {latest}")
            return latest

        # --- Generic DCC search ---
        for sub in apps_root.iterdir():
            for name in candidates:
                if name in sub.name.lower():
                    print(f"✅ Found: {name}")
                    return sub.resolve()

        # --- Check PATH as fallback ---
        dcc_exe = which(dcc_name)
        if dcc_exe:
            print(f"✅ Found: {dcc_exe}")
            return Path(dcc_exe).resolve()

        raise print(f"App doesn't found'{dcc_name}' en {apps_root}")

    except FileNotFoundError:
        raise print(f"root path {apps_root} not exists.")
    except PermissionError:
        raise print(f"No permisions{apps_root}.")
    except Exception as e:
        raise print(f"Error searching  DCC '{dcc_name}': {e}")
