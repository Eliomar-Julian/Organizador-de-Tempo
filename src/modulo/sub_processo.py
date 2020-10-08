from PySide2.QtCore import QThread, QObject, Signal


class MyThread(QThread):
    def __init__(self, tempo=1):
        self.tempo = tempo
        self.SINAL = self.MySignal()
        QThread.__init__(self, parent=None)

    class MySignal(QObject):
        sinal = Signal(int)

    def run(self):
        from time import sleep
        while True:
            sleep(self.tempo)
            self.SINAL.sinal.emit(1)