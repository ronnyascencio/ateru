import bpy
import sys
import os

# ------------------------------
# Configurar paths antes de cualquier import
# ------------------------------
PIPELINE_ROOT = os.environ.get("PIPELINE_ROOT")
if PIPELINE_ROOT is None:
    raise EnvironmentError("La variable PIPELINE_ROOT no está definida en el sistema")

# Agregamos PIPELINE_ROOT a sys.path
if PIPELINE_ROOT not in sys.path:
    sys.path.insert(0, PIPELINE_ROOT)

# Site-packages de tu .venv
venv_site_packages = os.path.join(PIPELINE_ROOT, ".venv", "lib", "python3.11", "site-packages")
if venv_site_packages not in sys.path:
    sys.path.insert(0, venv_site_packages)
    print(f"VENV agregado a sys.path: {venv_site_packages}")

# Carpeta core
CORE_PATH = os.path.join(PIPELINE_ROOT, "core")
if CORE_PATH not in sys.path:
    sys.path.insert(0, CORE_PATH)

print("PIPELINE_ROOT agregado a sys.path:", PIPELINE_ROOT)
print("CORE_PATH agregado a sys.path:", CORE_PATH)

# ------------------------------
# Ahora sí podemos importar módulos
# ------------------------------
# Prueba PySide6
try:
    from PySide6 import QtWidgets
    print("PySide6 encontrado ✅")
except ModuleNotFoundError:
    print("PySide6 NO encontrado ❌")

# Importar core
try:
    import xolo_core
    print("xolo_core encontrado:", xolo_core)
except ModuleNotFoundError:
    print("xolo_core NO encontrado")

# Ahora los módulos de Blender
from .operators import XOLO_OT_OpenUI
from .menu import XOLO_MT_Menu

# ------------------------------
# Registro de clases
# ------------------------------
classes = [XOLO_OT_OpenUI, XOLO_MT_Menu]

def draw_menu(self, context):
    self.layout.menu("XOLO_MT_menu")

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.TOPBAR_MT_editor_menus.append(draw_menu)
    print("Xolo Tools registrado")

def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(draw_menu)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    print("Xolo Tools desregistrado")
