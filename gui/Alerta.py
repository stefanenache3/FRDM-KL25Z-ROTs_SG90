from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QMessageBox
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtCore import QUrl
class SeismicAlert(QThread):
    seismic_alert_signal = Signal()

    def __init__(self, parent=None):
        super(SeismicAlert, self).__init__(parent)

    def run(self):
        self.seismic_alert_signal.emit()
