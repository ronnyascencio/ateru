"""logger for terminal"""


def log_core(msg: str):
    message: str = f"[XOLO CORE] {msg}"

    return print(message)


def log_ui(msg: str):
    message: str = f"[XOLO UI] {msg}"

    return print(message)


def log_error(msg: str):
    message: str = f"[XOLO ERROR] ❌ {msg}"
    return print(message)
