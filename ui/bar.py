from PySide6.QtCore import QElapsedTimer, QTimer
from PySide6.QtWidgets import QApplication


class ProgressController:
    def __init__(self, ui, enable_fn, disable_fn, min_duration_ms=600):
        self.ui = ui
        self.enable_fn = enable_fn
        self.disable_fn = disable_fn
        self.min_duration_ms = min_duration_ms
        self._timer = QElapsedTimer()

    def start(self):
        bar = self.ui("status_progressBar")
        bar.setMinimum(0)
        bar.setMaximum(0)  # indeterminado
        bar.setVisible(True)

        self.disable_fn()
        self._timer.start()
        QApplication.processEvents()

    def stop(self, on_done=None):
        elapsed = self._timer.elapsed()
        remaining = max(0, self.min_duration_ms - elapsed)

        def finish():
            self.ui("status_progressBar").setVisible(False)
            self.enable_fn()
            if on_done:
                on_done()

        QTimer.singleShot(remaining, finish)
