from PySide2 import QtWidgets, QtCore, QtGui
from modulo.todas_imagens import imagens_


# // classe que representa o menu de contexto
class MyMenu(QtWidgets.QFrame):
    def __init__(self, parent=None):
        self.pai = parent
        QtWidgets.QFrame.__init__(self, parent=self.pai)
        self.setStyleSheet('''background-color: qlineargradient(\
            spread:pad, x1:0.011236, y1:0.233, x2:1, y2:0.227,\
            stop:0.134831 rgba(132, 8, 255, 255), stop:0.94382 rgba(\
            62, 0, 123, 255));''')
        self.setVisible(True)
        self.setVisible(False)
        
        self.images = imagens_()

        self.im_despertador = QtWidgets.QLabel()
        self.im_relogio = QtWidgets.QLabel()
        self.im_cronometro = QtWidgets.QLabel()
        self.im_config = QtWidgets.QLabel()

        self.texto_despertador = QtWidgets.QPushButton('Alarmes')
        self.texto_relogio = QtWidgets.QPushButton('Relogio')
        self.texto_cronometro = QtWidgets.QPushButton('Cronometro')
        self.texto_config = QtWidgets.QPushButton('Mais')

        botoes = [
            self.texto_despertador, self.texto_relogio,
            self.texto_cronometro, self.texto_config]
        
        widgets = [
            self.im_despertador, self.im_relogio,
            self.im_cronometro, self.im_config]

        chaves = [
            'bell', 'relogio',
            'hourglass', 'settings'
        ]

        for n in range(0, len(widgets)):
            widgets[n].setPixmap(self.images[chaves[n]])
            widgets[n].setScaledContents(True)
            widgets[n].setMaximumSize(25, 25)
            widgets[n].setStyleSheet('background: rgba(\
                132, 8, 200, 255); border-radius: 5px; padding: 10pt;''')

        self.grade = QtWidgets.QGridLayout(self)
        
        for n in range(0, len(widgets)):
            self.grade.addWidget(widgets[n], n, 0, QtCore.Qt.AlignRight)

        for n in range(0, len(widgets)):
            self.grade.addWidget(botoes[n], n, 1, QtCore.Qt.AlignLeft)
            botoes[n].setStyleSheet('background: rgba(\
                0,0,0,0); font: 200 12pt "Arial"; color: rgba(\
                255, 255, 255, 200); text-align: left;\
                text-decoration: underline;')
            botoes[n].setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            