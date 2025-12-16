""" logger for terminal """
def log_core(msg):
    print(f"[XOLO CORE] {msg}")

def log_ui(msg):
    print(f"[XOLO UI] {msg}")


def log_error(msg):
    print(f"[XOLO ERROR] ❌ {msg}")
