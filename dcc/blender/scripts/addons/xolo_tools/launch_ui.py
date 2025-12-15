# launch_ui.py
import sys
import threading
from PySide6 import QtWidgets, QtCore
from pathlib import Path

# ----- Debug helper -----
def debug(msg):
    print(f"[Xolo UI] {msg}")

# ----- Importar tu UI real -----
# Opción 1: tu clase Python
try:
    from core.xolo_core.ui.xolo_window import XoloMainWindow
    debug("XoloMainWindow importado ✅")
except ModuleNotFoundError as e:
    debug(f"No se pudo importar XoloMainWindow ❌: {e}")

# Opción 2: si quieres cargar un .ui en lugar de clase Python
# from PySide6 import QtUiTools, QtCore
# def load_ui(ui_path):
#     loader = QtUiTools.QUiLoader()
#     ui_file = QtCore.QFile(ui_path)
#     ui_file.open(QtCore.QFile.ReadOnly)
#     window = loader.load(ui_file)
#     ui_file.close()
#     return window

# ----- Función que corre Qt en un hilo -----
def _qt_thread():
    debug("Starting Qt thread")

    # Crear QApplication si no existe
    app = QtWidgets.QApplication.instance()
    if not app:
        debug("No QApplication found, creando nuevo")
        app = QtWidgets.QApplication(sys.argv)
    else:
        debug("QApplication ya existe")

    # Crear instancia de tu UI
    try:
        window_instance = XoloMainWindow()  # reemplaza si usas load_ui("path/to/ui.ui")
        debug("Ventana creada correctamente")
    except Exception as e:
        debug(f"Error creando ventana: {e}")
        return

    # Mostrar ventana
    try:
        window_instance.show()
        debug("Ventana mostrada ✅")
    except Exception as e:
        debug(f"Error mostrando ventana: {e}")
        return

    # Integrar con event loop de Blender usando QTimer
    timer = QtCore.QTimer()
    timer.start(100)  # 100ms, puede ajustarse
    timer.timeout.connect(lambda: None)  # evita que Blender se bloquee
    debug("QTimer configurado para integración con Blender")

    # Ejecutar event loop
    try:
        app.exec()
        debug("Event loop terminado")
    except Exception as e:
        debug(f"Error en event loop: {e}")

# ----- Función pública para lanzar UI -----
def launch_window():
    debug("launch_window() llamado")
    qt_thread = threading.Thread(target=_qt_thread, daemon=True)
    qt_thread.start()
    debug("Hilo Qt iniciado")
