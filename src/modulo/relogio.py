from PySide2 import QtWidgets
from datetime import datetime
from time import sleep


class Relogio:
    def __init__(self, parent):
        self.pai = parent
        self.pai.MODO = 'rel'
        self.pai.menu.setVisible(False)
        self.pai.th.SINAL.sinal.connect(self.muda)

        self.frame = QtWidgets.QFrame(self.pai)
        self.frame.setGeometry(100,75,300,160)
        self.frame.setStyleSheet("""QPushButton {
            color: white;
            background: teal;
            font: 100 14pt "Arial";
            width: 40px;
            height: 40px;
            border-radius: 20px;
        }
            QPushButton::hover {
                background: purple;
                color: teal;
            }
            QLabel {
                color: red;
                background: rgba(62, 0, 123, 255);
                border-radius: 10px;
                }
            QListWidget {
                color: white;
                font: 100 10pt "Arial";
                border: ridge;
                background: teal;
            }""")
        
        self.lista = QtWidgets.QListWidget()
        self.cidades = [
                'Rio Branco', 'Brasilia',
                'Manaus', 'Fernando de Noronha']

        self.utcs = [5, 3, 4,2]
        self.dict_H = dict()
        
        for x in range(0, len(self.cidades)):
            self.dict_H[str(self.cidades[x])] = self.utcs[x]
        
        self.lista.addItems(self.cidades)
        self.lista.setMaximumSize(300, 100)
        
        self.cid = 'Brasilia'
        self.label = QtWidgets.QLabel(f'UTC-Zone {self.cid}')

        self.btS = QtWidgets.QPushButton('Sair')
        self.btS.clicked.connect(self.sair)

        self.btO = QtWidgets.QPushButton('Ok')
        self.btO.clicked.connect(self.muda)
        self.btP = QtWidgets.QPushButton('Add')

        self.grade = QtWidgets.QGridLayout(self.frame)
        self.grade.addWidget(self.lista, 0, 0, 1,0)
        self.grade.addWidget(self.label, 1, 0)
        self.grade.addWidget(self.btS, 2, 0)
        self.grade.addWidget(self.btO, 2, 1)
        self.grade.addWidget(self.btP, 2, 2)

        self.frame.show()

    
    #################################################################
    # relogio personalizado
    def muda(self):
        data = datetime.today().now()
        try:
            hh = int(datetime.utcnow(
                ).strftime('%H')) - self.dict_H[self.lista.currentItem(
                ).text()]
            
            self.label.setText(
                'UTC-zone: ' + self.lista.currentItem(
                ).text())
        except:
            hh = data.strftime('%H')
        self.pai.display.setText(data.strftime(str(hh) + ':%M:%S'))


    def sair(self):
        self.frame.close()
        sleep(0.5)
        self.pai.th.SINAL.sinal.connect(self.pai.hora)
        self.pai.MODO = None



