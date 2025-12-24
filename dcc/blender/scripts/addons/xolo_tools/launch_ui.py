
import sys
import threading
from PySide6 import QtWidgets, QtCore

from core.xolo_core.extractors.dcc import detect_dcc
from core.xolo_core.utils.logging import log_core, log_ui, log_error


""" ui loader"""
try:
    from core.xolo_core.ui.xolo_window import XoloMainWindow
    log_ui("ui imported ")
except ModuleNotFoundError as e:
    log_error(f"could not import: {e}")


""" Qt thread """
def _qt_thread():
    log_core("Starting Qt thread")

    """build app if not exists"""
    app = QtWidgets.QApplication.instance()
    if not app:
        log_ui("No QApplication found, build")
        app = QtWidgets.QApplication(sys.argv)
    else:
        log_ui("QApplication exists")

    """ instace """
    try:
        current_dcc = detect_dcc()
        window_instance = XoloMainWindow(dcc=current_dcc)
        log_ui("window build correctly")
    except Exception as e:
        log_error(f"Error building window: {e}")
        return

    """ show window """
    try:
        window_instance.show()
        log_ui("window shown")
    except Exception as e:
        log_error(f"Error showing window: {e}")
        return

    """ event loop with QTimer"""
    timer = QtCore.QTimer()
    timer.start(100)  # 100ms
    timer.timeout.connect(lambda: None)  # blender not get blocked
    log_core("QTimer configured")

    """ execute event loop"""
    try:
        app.exec()
        log_core("Event loop finished")
    except Exception as e:
        log_error(f"Error event loop: {e}")

""" function to launch ui"""
def launch_window():
    log_core("launch_window() called")
    qt_thread = threading.Thread(target=_qt_thread, daemon=True)
    qt_thread.start()
    log_core("Hilo Qt started")
