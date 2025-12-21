
import json

import subprocess
import sys
from pathlib import Path

try:
    from PySide6.QtCore import QThread, Signal
    from PySide6.QtWidgets import (
        QApplication,
        QCheckBox,
        QComboBox,
        QFileDialog,
        QHBoxLayout,
        QLabel,
        QListWidget,
        QPlainTextEdit,
        QProgressBar,
        QPushButton,
        QVBoxLayout,
        QWidget,
    )
except Exception as e:
    print(f"PySide6 not installed{e}")
    raise

# Heurística simple para detectar tipos de mapa por nombre de archivo
TYPE_KEYWORDS = {
    "albedo": ["albedo", "basecolor", "base_color", "diffuse", "color", "albedo"],
    "normal": ["normal", "nrm", "norm"],
    "bump": ["bump"],
    "displacement": ["disp", "displacement"],
    "roughness": ["roughness", "rough", "rgh"],
    "metalness": ["metalness", "metal"],
    "specular": ["specular", "spec"],
    "ao": ["ao", "ambientocclusion", "occlusion"],
    "emissive": ["emissive", "emit", "emission"],
}

IMAGE_EXTS = {
    ".exr",
    ".tif",
    ".tiff",
    ".jpg",
    ".jpeg",
    ".png",
    ".hdr",
    ".bmp",
    ".tx",
    ".tex",
}


def detect_type_from_name(name: str) -> str:
    n = name.lower()
    for t, keys in TYPE_KEYWORDS.items():
        for k in keys:
            if k in n:
                return t
    return "unknown"


def find_images_in_dir(directory: Path):
    files = []
    for p in directory.rglob("*"):
        if p.suffix.lower() in IMAGE_EXTS and p.is_file():
            files.append(p)
    return sorted(files)


class ConverterThread(QThread):
    log = Signal(str)
    progress = Signal(int)
    finished = Signal(dict)

    def __init__(self, files, out_ext, use_maketx, overwrite, extra_flags_map):
        super().__init__()
        self.files = files
        self.out_ext = out_ext
        self.use_maketx = use_maketx
        self.overwrite = overwrite
        self.extra_flags_map = extra_flags_map

    def run(self):
        results = {}
        total = len(self.files)
        for i, fpath in enumerate(self.files, start=1):
            try:
                fname = fpath.name
                detected = detect_type_from_name(fname)
                out_path = fpath.with_suffix(self.out_ext)

                if out_path.exists() and not self.overwrite:
                    self.log.emit(f"[SKIP] {out_path} (exists, overwrite=False)")
                    results[str(fpath)] = {
                        "status": "skipped",
                        "tx": str(out_path),
                        "type": detected,
                    }
                    self.progress.emit(int(100 * i / total))
                    continue

                # construir comando
                if self.use_maketx:
                    # maketx (OpenImageIO) recommended flags; user can customize via extra_flags_map
                    cmd = ["maketx", "-v"]
                    extra = self.extra_flags_map.get(detected, "")
                    if extra:
                        cmd += extra.split()
                    cmd += [str(fpath)]
                    # output option -o
                    cmd += ["-o", str(out_path)]
                else:
                    # txmake (RenderMan)
                    cmd = ["txmake"]
                    extra = self.extra_flags_map.get(detected, "")
                    if extra:
                        cmd += extra.split()
                    # force format pixar for RenderMan compatibility
                    cmd += ["-format", "pixar", str(fpath), str(out_path)]

                self.log.emit(f"[RUN] {' '.join(cmd)}")
                # ejecutar
                completed = subprocess.run(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                if completed.returncode == 0:
                    self.log.emit(f"[OK] Converted: {fname} -> {out_path.name}")
                    status = "ok"
                else:
                    self.log.emit(
                        f"[ERR] Fallo al convertir {fname}: rc={completed.returncode}"
                    )
                    self.log.emit(completed.stdout)
                    self.log.emit(completed.stderr)
                    status = "error"

                results[str(fpath)] = {
                    "status": status,
                    "tx": str(out_path),
                    "type": detected,
                    "stdout": completed.stdout,
                    "stderr": completed.stderr,
                }
            except Exception as e:
                self.log.emit(f"[EXC] {e}")
                results[str(fpath)] = {"status": "exception", "error": repr(e)}
            self.progress.emit(int(100 * i / total))
        self.finished.emit(results)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Xolo RenderMan  Texture Converter")
        self.resize(800, 600)
        layout = QVBoxLayout()
        top = QHBoxLayout()
        btn_select = QPushButton("Seleccionar carpeta")
        btn_select.clicked.connect(self.select_folder)
        self.lbl_folder = QLabel("Ninguna carpeta seleccionada")
        top.addWidget(btn_select)
        top.addWidget(self.lbl_folder, 1)
        layout.addLayout(top)

        mid = QHBoxLayout()
        self.list_files = QListWidget()
        mid.addWidget(self.list_files, 3)

        right = QVBoxLayout()
        right.addWidget(QLabel("Salida:"))
        self.cmb_ext = QComboBox()
        self.cmb_ext.addItems([".tex", ".tx"])
        right.addWidget(self.cmb_ext)
        self.chk_use_maketx = QCheckBox("Usar maketx (OIIO) si disponible")
        right.addWidget(self.chk_use_maketx)
        self.chk_overwrite = QCheckBox("Sobrescribir archivos existentes")
        right.addWidget(self.chk_overwrite)
        right.addStretch(1)

        # opciones por tipo (simplificado): campo de texto para flags extra por cada tipo
        right.addWidget(QLabel("Flags extra por tipo (ej: '-u --oiio')"))
        self.extra_flags = {}
        for t in sorted(TYPE_KEYWORDS.keys()):
            lbl = QLabel(t)
            txt = QPlainTextEdit()
            txt.setMaximumHeight(30)
            txt.setPlaceholderText("flags (opcional)")
            self.extra_flags[t] = txt
            right.addWidget(lbl)
            right.addWidget(txt)

        mid.addLayout(right, 1)
        layout.addLayout(mid)

        bottom = QHBoxLayout()
        self.btn_start = QPushButton("Convertir")
        self.btn_start.clicked.connect(self.start_conversion)
        bottom.addWidget(self.btn_start)
        self.progress = QProgressBar()
        bottom.addWidget(self.progress, 1)
        layout.addLayout(bottom)

        self.log_widget = QPlainTextEdit()
        self.log_widget.setReadOnly(True)
        layout.addWidget(self.log_widget, 1)

        self.setLayout(layout)
        self.current_folder = None
        self.files = []

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Selecciona carpeta con texturas"
        )
        if folder:
            self.current_folder = Path(folder)
            self.lbl_folder.setText(str(self.current_folder))
            self.refresh_file_list()

    def refresh_file_list(self):
        self.list_files.clear()
        self.files = find_images_in_dir(self.current_folder)
        for p in self.files:
            detected = detect_type_from_name(p.name)
            self.list_files.addItem(
                f"{p.relative_to(self.current_folder)}    [{detected}]"
            )

    def append_log(self, text):
        self.log_widget.appendPlainText(text)

    def start_conversion(self):
        if not self.current_folder:
            self.append_log("[ERROR] Selecciona una carpeta primero.")
            return
        out_ext = self.cmb_ext.currentText()
        use_maketx = self.chk_use_maketx.isChecked()
        overwrite = self.chk_overwrite.isChecked()
        extra_flags_map = {
            t: self.extra_flags[t].toPlainText().strip() for t in self.extra_flags
        }
        self.btn_start.setEnabled(False)
        self.thread = ConverterThread(
            self.files, out_ext, use_maketx, overwrite, extra_flags_map
        )
        self.thread.log.connect(self.append_log)
        self.thread.progress.connect(self.progress.setValue)
        self.thread.finished.connect(self.on_finished)
        self.thread.start()

    def on_finished(self, results):
        self.btn_start.setEnabled(True)
        # guardar manifest en carpeta seleccionada
        manifest_path = self.current_folder / "textures_manifest.json"
        try:
            with open(manifest_path, "w", encoding="utf-8") as fh:
                json.dump(results, fh, indent=2)
            self.append_log(f"[INFO] Manifest guardado en {manifest_path}")
        except Exception as e:
            self.append_log(f"[ERR] Guardando manifest: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
