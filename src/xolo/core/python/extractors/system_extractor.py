import pathlib
import platform


def get_os_type() -> str:
    system = platform.system()
    if system == "Windows":
        return "windows"
    elif system == "Darwin":
        return "macos"
    elif system == "Linux":
        return "linux"
    else:
        return "unknown"


def get_home_directory() -> dict:
    HOME = pathlib.Path.home()
    sys_info = {"os": get_os_type(), "home": str(HOME)}

    return sys_info
