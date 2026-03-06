from pathlib import Path
from typing import Optional
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from ateru.ui.utils.ui_loader import load_ui
import ateru.ui.uix.ateru_rc


class BasePanel(QWidget):
    def __init__(
        self,
        tools_widget: Optional[QWidget],
        context_widget: Optional[QWidget],
        publish_widget: Optional[QWidget],
        parent=None,
    ):
        super().__init__(parent)

        # 1. Configurar Layout Principal de este Widget
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 2. Cargar UI con ScrollArea
        ui_path = Path(__file__).parent.parent / "uix" / "shered" / "base_panel.ui"
        self.ui = load_ui(ui_path, self)
        main_layout.addWidget(self.ui)

        # 3. Icono y Título
        self.setWindowIcon(QIcon(":/manager/icons/ateru.svg"))
        self.setWindowTitle("Ateru Pipeline")

        # 4. Inyectar los widgets
        # Buscamos los placeholders dentro del contenido del ScrollArea
        self._inject(self.ui.findChild(QWidget, "context_placeholder"), context_widget)
        self._inject(self.ui.findChild(QWidget, "tools_container"), tools_widget)
        self._inject(self.ui.findChild(QWidget, "publish_placeholder"), publish_widget)

    def _inject(self, placeholder: QWidget, widget: QWidget):
        """Añade el widget al placeholder de forma sencilla."""
        if not placeholder or not widget:
            return

        # Asegurar que el placeholder tenga layout para que el widget se estire
        layout = placeholder.layout()
        if not layout:
            layout = QVBoxLayout(placeholder)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

        # Limpiar previos por si acaso
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Añadir y mostrar
        layout.addWidget(widget)

        widget.show()
