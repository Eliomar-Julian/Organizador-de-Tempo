from PySide2 import QtWidgets, QtCore
from modulo.barra_titulos import Barra
from modulo.menu_personalizado import MyMenu
from modulo.sub_processo import MyThread
from modulo.cronometro import Chrono
from modulo.relogio import Relogio
from datetime import datetime



# janela Base
class MyWindow(QtWidgets.QWidget):
    # // controles ..
    BACKGROUND = '#400080'
    LARGURA = 500
    ALTURA = 500
    MODO = None

    
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.resize(self.LARGURA, self.ALTURA)
        self.setStyleSheet('background: %s;' % self.BACKGROUND)
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
        if e == r and self.MODO == None: 
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



app = QtWidgets.QApplication([])
form = MyWindow()
form.show()
app.exec_()