from PySide2 import QtCore, QtGui, QtWidgets
from modulo.todas_imagens import imagens_

# // barra de titulos personalizada
class Barra(QtWidgets.QFrame):
    LARG = 500
    ALTU = 500

    def __init__(self, parent):
        self.parent = parent
        QtWidgets.QFrame.__init__(self, parent=self.parent)
        self.imagens = imagens_()
        self.setStyleSheet(
            'background-color: qlineargradient(spread:pad, x1:0.479,\
             y1:0.125136, x2:0.499818, y2:1, stop:0 rgba(13, 0, 26, 100),\
             stop:1 rgba(255, 255, 255, 20));')
        self.elementos()

    # // definindo widgets ..
    def elementos(self):
        # // label que contem o icone da esquerda
        self.icone = QtWidgets.QLabel()
        self.icone.setPixmap(self.imagens['hourglass'])
        self.icone.setScaledContents(True)
        self.icone.setMaximumSize(15, 15)

        # contem o label de titulo
        self.titulo = QtWidgets.QLabel('Chronos Organizer')
        self.titulo.setStyleSheet('font: 100 14pt "Arial"; color: white;')

        # botoes ---
        self.botao_fechar = QtWidgets.QPushButton()
        self.botao_fechar.clicked.connect(lambda: self.parent.close())
        self.botao_fechar.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_fechar.setToolTip('Sair')
        self.botao_fechar.setStyleSheet(
            'width: 20px; height: 20px; border-radius:\
             10px; background: red; color: white;')

        self.botao_minim = QtWidgets.QPushButton()
        self.botao_minim.clicked.connect(lambda: self.parent.showMinimized())
        self.botao_minim.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.botao_minim.setToolTip('Minimizar')
        self.botao_minim.setStyleSheet(
            "width: 20px; height: 20px; border-radius:\
             10px; background: teal; color: white;")
        
        ## // Organizadores ....
        self.frame_esquerdo = QtWidgets.QFrame()
        self.frame_esquerdo.setStyleSheet('background: rgba(0, 0, 0, 0);')
        self.grade_frame_e = QtWidgets.QHBoxLayout(self.frame_esquerdo)
        self.grade_frame_e.addWidget(self.icone, QtCore.Qt.AlignLeft)
        self.grade_frame_e.addWidget(self.titulo, QtCore.Qt.AlignHCenter)

        self.frame_direito = QtWidgets.QFrame()
        self.frame_direito.setStyleSheet('background: rgba(0, 0, 0, 0);')
        self.grade_frame_d = QtWidgets.QHBoxLayout(self.frame_direito)
        self.grade_frame_d.addWidget(self.botao_minim)
        self.grade_frame_d.addWidget(self.botao_fechar)
        
        self.grade_pai = QtWidgets.QHBoxLayout(self)
        self.grade_pai.addWidget(self.frame_esquerdo)
        self.grade_pai.addWidget(self.frame_direito)

    # // evento ao pressionar o mouse
    def mousePressEvent(self, event):
        self.posi1 = self.parent.geometry().getRect()[0]
        self.posi2 = self.parent.geometry().getRect()[1]
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.setCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))

    # // evento ao soltar o mouse
    def mouseReleaseEvent(self, event):
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    # // movimenta a janela
    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.parent.setGeometry(
                self.mapToGlobal(event.pos()).x() - self.posi1 // 3,
                self.mapToGlobal(event.pos()).y() - self.posi2 // 3,
                self.LARG, self.ALTU)