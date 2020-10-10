from PySide2 import QtWidgets, QtGui, QtCore
from modulo.sub_processo import MyThread

class Chrono:
    # controles
    MODO = None
    MIL = SEG = MIN = HOR = 0

    
    def __init__(self, pai):
        self.pai = pai
        self.cronometro_()
        self.pai.th.SINAL.sinal.disconnect()
        self.pai.display.setText('0:00:0')

    
    # constroi o cronometro
    def cronometro_(self):
        self.conteiner = QtWidgets.QFrame(self.pai)
        self.conteiner.setGeometry(55, 100, 400,80)
        self.conteiner.show()
        self.pai.menu.setVisible(False)
        self.grade_cron = QtWidgets.QHBoxLayout(self.conteiner)
        
        self.bt_reset = QtWidgets.QPushButton('Limpar')
        self.bt_reset.clicked.connect(
            lambda: self.roda_cronometro(self.bt_reset.text()))
        self.bt_print = QtWidgets.QPushButton('Print')
        self.bt_print.clicked.connect(
            lambda: self.roda_cronometro(self.bt_print.text()))
        self.bt_pausar = QtWidgets.QPushButton('Play')
        self.bt_pausar.clicked.connect(
            lambda: self.roda_cronometro(self.bt_pausar.text()))
        self.bt_sair = QtWidgets.QPushButton('Sair')
        self.bt_sair.clicked.connect(
            lambda: self.roda_cronometro(self.bt_sair.text()))

        # // lista de prints
        self.listar = QtWidgets.QListWidget(self.pai)
        self.listar.setVisible(True)
        self.listar.setGeometry(160, 170, 200, 150)
        self.listar.setStyleSheet('color: white; font: 100 14pt "Arial";')

        self.grade_cron2 = QtWidgets.QHBoxLayout(self.conteiner)
        self.grade_cron2.addWidget(self.listar)

        bts = [
            self.bt_reset, self.bt_print,
            self.bt_pausar, self.bt_sair]

        for x in range(0, len(bts)):
            self.grade_cron.addWidget(bts[x])

        for x in bts:
            x.setStyleSheet('''color: white; font: 100 12pt "Arial";
            width: 50px; height: 50px; border-radius: 25px;
            background: teal;''')        

    
    # função de controle dos botoes
    def roda_cronometro(self, botao):
        if botao == 'Print':
            self.print_()
        elif botao == 'Limpar':
            self.limpar()
        elif botao == 'Play':
            self.pai.th.SINAL.sinal.connect(self.play)
        elif botao == 'Pausar':
            self.pai.th.SINAL.sinal.disconnect()
            self.bt_pausar.setText('Play')
        if botao == 'Sair':
            self.listar.close()
            self.conteiner.close()
            self.pai.th.SINAL.sinal.connect(self.pai.hora)


    
    # // print tempos 
    def print_(self):
        self.listar.addItem(self.pai.display.text())
    
    
    # limpa
    def limpar(self):
        self.MIL = self.SEG = self.MIN = self.HOR = 0
        self.listar.clear()
        self.pai.display.setText('0:00:0')
    
    
    # toca
    def play(self):
        self.bt_pausar.setText('Pausar')
        self.MIL += 1
        if self.MIL == 9:
            self.SEG += 1
            self.MIL = 0
        elif self.SEG == 59:
            self.MIN += 1
            self.SEG = 0
        elif self.MIN == 59:
            self.HOR += 1
            self.MIN = 0
        self.pai.display.setText(
            f'{self.HOR}:{self.MIN}:{self.SEG}:{self.MIL}')

