from PySide2 import QtWidgets, QtCore
from modulo.barra_titulos import Barra


class MyWindow(QtWidgets.QWidget):
    BACKGROUND = '#400080'
    LARGURA = 500
    ALTURA = 500

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.resize(self.LARGURA, self.ALTURA)
        self.setStyleSheet('background: %s;' % self.BACKGROUND)

        self.barra = Barra(self)

        self.corpo = QtWidgets.QFrame()

        self.grade_h = QtWidgets.QGridLayout(self)
        self.grade_h.setContentsMargins(0, 0, 0, 0)
        self.grade_h.addWidget(self.barra, 0, 0, QtCore.Qt.AlignTop)
        self.grade_h.addWidget(self.corpo, 1, 0, QtCore.Qt.AlignHCenter)

        self.display = QtWidgets.QLabel('0:00:0')
        self.display.setStyleSheet('color: #e6ccff; font: 200 80pt "Ds-Digital";')

        self.d = QtWidgets.QLabel('0:00:0')
        self.d.setStyleSheet('color: #e6ccff; font: 200 80pt "Ds-Digital";')

        self.grade_corpo = QtWidgets.QGridLayout(self.corpo)
        self.grade_corpo.setContentsMargins(0, 0, 0, 0)
        self.grade_corpo.addWidget(self.display, 0, 0, QtCore.Qt.AlignCenter)


app = QtWidgets.QApplication([])
form = MyWindow()
form.show()
app.exec_()