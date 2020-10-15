from PySide2 import QtWidgets, QtCore, QtGui
from modulo.barra_titulos import Barra
from modulo.menu_personalizado import MyMenu
from modulo.sub_processo import MyThread
from modulo.cronometro import Chrono
from modulo.relogio import Relogio
from modulo.alarmes import Alarmes
from modulo.leitura import ler_database
from modulo.todas_imagens import imagens_
from datetime import datetime
import pygame


pygame.init()


# janela Base
class MyWindow(QtWidgets.QWidget):
    # // controles ..
    BACKGROUND = '#400080'
    LARGURA = 500
    ALTURA = 500
    MODO = None
    DESPERTA = False

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.resize(self.LARGURA, self.ALTURA)
        self.setStyleSheet('background: %s;' % self.BACKGROUND)
        self.setWindowIcon(QtGui.QIcon(
            QtGui.QPixmap('./img/relogio.svg')))
        self.start()

    #################################################################
    # // Contem todos os widgets extras

    def start(self):
        self.barra = Barra(self)

        self.corpo = QtWidgets.QFrame()

        self.th = MyThread()
        self.th.start()
        self.th.SINAL.sinal.connect(self.hora)

        self.grade_h = QtWidgets.QGridLayout(self)
        self.grade_h.setContentsMargins(0, 0, 0, 0)
        self.grade_h.addWidget(self.barra, 0, 0, QtCore.Qt.AlignTop)
        self.grade_h.addWidget(self.corpo, 1, 0, QtCore.Qt.AlignHCenter)

        # visor.....
        self.display = QtWidgets.QLabel('0:00:0')
        self.display.setMinimumSize(420, 100)
        self.display.setStyleSheet(
            'color: #e6ccff; font: 200 80pt "Ds-Digital";')

        #############################################################
        # instancia do menu flutuante
        self.menu = MyMenu(self)
        self.menu.texto_cronometro.clicked.connect(self.cronometro)
        self.menu.texto_relogio.clicked.connect(self.relogio)
        self.menu.texto_despertador.clicked.connect(self.alarmes)

        # display .....
        self.d = QtWidgets.QLabel('0:00:0')
        self.d.setStyleSheet(
            'color: #e6ccff; font: 200 80pt "Ds-Digital";')

        self.grade_corpo = QtWidgets.QGridLayout(self.corpo)
        self.grade_corpo.setContentsMargins(0, 0, 0, 0)
        self.grade_corpo.addWidget(
            self.display, 0, 0, QtCore.Qt.AlignHCenter)

    ##########################################################################
    # // Captura o clique do mouse

    def mousePressEvent(self, event):
        e = event.buttons()
        r = QtCore.Qt.MouseButton.RightButton
        if e == r and self.MODO is None:
            self.menu.setVisible(True)
            self.menu.setGeometry(
                event.pos().x(),
                event.pos().y(),
                150, 150)
            self.setTabOrder(self, self.menu)
        else:
            self.menu.setVisible(False)

    #################################################################
    # // Mostra a hora no visor..

    def hora(self):
        data = datetime.today().now()
        self.display.setText(data.strftime('%H:%M:%S'))
        self.alarme_func()        

    #################################################################

    def cronometro(self):
        self.th.tempo = 0.1
        self.crono = Chrono(self)
        self.th.SINAL.sinal.connect(self.crono.roda_cronometro)
        self.display.setText('0:00:0')
        self.MODO = 'crono'

    #################################################################

    def relogio(self):
        self.relogio_ = Relogio(self)
      

    #################################################################
    # alarme configurações

    def alarmes(self):
        self.alarme = Alarmes(self)

    def alarme_func(self):
        self.leitura = ler_database()
        data = datetime.today().now()
        hh = data.strftime('%H')
        mm = data.strftime('%M')
        for x in self.leitura.values():
            if int(hh) == int(x[1]) and int(mm) == int(x[2]):
                if self.DESPERTA is False:
                    self.tocar(x[3])                    
                    
    #################################################################
    # toca a musica ...

    def tocar(self, caminho):
        self.DESPERTA = True
        pygame.mixer_music.load(caminho)
        pygame.mixer_music.play(0, 0.0)
        pygame.mixer_music.set_pos(1)
        self.popup = QtWidgets.QDialog()
        self.popup.setStyleSheet('background: %s;' % self.BACKGROUND)
        self.popup.resize(200, 200)
        self.popup.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        lab = QtWidgets.QLabel('Desligar', self.popup)
        lab.setStyleSheet('color: #fff; font: 200 20pt "Arial";')
        lab.move(100//3, 100//3)
        bt = QtWidgets.QPushButton(self.popup)
        img = imagens_()
        bt.setIcon(img['bell'])
        bt.setIconSize(QtCore.QSize(50, 50))
        bt.move(100//3 + 20, 100//3+50)
        bt.clicked.connect(self.desligar)
        self.popup.exec_()

    #################################################################
    # desliga a musica

    def desligar(self):
        pygame.mixer_music.stop()
        self.popup.close()
        self.DESPERTA = False
        

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app.setWindowIcon(QtGui.QIcon(
        QtGui.QPixmap('./img/relogio.svg')))
    form = MyWindow()
    form.show()
    app.exec_()