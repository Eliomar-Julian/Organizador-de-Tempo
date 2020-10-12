from PySide2 import QtWidgets, QtGui, QtCore
from modulo.todas_imagens import imagens_
import sqlite3 as sql

### // Gernciamento dos alarmes


class Alarmes:
    def __init__(self, parent=None):
        self.pai = parent
        self.pai.menu.close()
        self.janela = QtWidgets.QDialog()
        self.janela.resize(500, 500)
        self.janela.setWindowTitle('Chronos Organizer')
        self.imgs = imagens_()
        self.janela.setWindowIcon(QtGui.QIcon(self.imgs['hourglass']))
        self.janela.setStyleSheet('background: %s;' % self.pai.BACKGROUND)

        self.frame = QtWidgets.QListWidget()
        self.frame.setStyleSheet('border: none;')
        self.grid_frame = QtWidgets.QVBoxLayout(self.frame)

        self.lab = QtWidgets.QPushButton('+')
        self.lab.clicked.connect(self.formulario)
        self.lab.setStyleSheet('''font: 100 20pt "Arial";
        	color: white;
        	width: 50px;
        	height: 50px;
        	border-radius: 25px;
        	background-color: teal;''')

        self.menos = QtWidgets.QPushButton('-')
        self.menos.clicked.connect(self.retirar)
        self.menos.setStyleSheet('''font: 100 20pt "Arial";
        	color: white;
        	width: 50px;
        	height: 50px;
        	border-radius: 25px;
        	background-color: teal;''')

        self.grid = QtWidgets.QGridLayout(self.janela)
        self.grid.addWidget(self.frame, 0, 0)
        self.grid.addWidget(self.lab, 1, 0, QtCore.Qt.AlignLeft)
        self.grid.addWidget(self.menos, 1, 0, QtCore.Qt.AlignRight)
        self.ler_database()

        self.janela.exec_()

    ##################################################################
    # formulario para adicionar alarmes personalizados

    def formulario(self):
        self.frame_form = QtWidgets.QDialog()
        self.frame_form.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.frame_form.setStyleSheet('''
            background: %s;
            color: #fff;
            font: 12pt "Arial";
            ''' % self.pai.BACKGROUND)
        
        self.lb = QtWidgets.QLabel('Titulo')
        self.lb.setStyleSheet('color: white; font: 14pt "Arial";')
        
        self.nm = QtWidgets.QLineEdit()
        
        self.hr = QtWidgets.QSpinBox()
        self.hr.setMaximum(23)


        self.mi = QtWidgets.QSpinBox()
        self.mi.setMaximum(59)

        self.lb_al = QtWidgets.QLabel('Toque')

        self.bt_save = QtWidgets.QPushButton('musica')
        self.bt_save.setIcon(QtGui.QIcon(self.imgs['file']))
        self.bt_save.clicked.connect(self.get_file)

        self.bt_ok = QtWidgets.QPushButton('ok')
        self.bt_ok.clicked.connect(self.get_var)

        self.bt_sair = QtWidgets.QPushButton('sair')
        self.bt_sair.clicked.connect(self.frame_form.close)       
        
        
        self.grade = QtWidgets.QGridLayout(self.frame_form)
        
        bts = [
            self.lb, self.nm, self.hr,
            self.mi, self.lb_al, self.bt_save,
            self.bt_ok, self.bt_sair]
        
        coo = [[0, 0], [0, 1], [0, 2],
            [0, 3], [1, 0], [1, 1],
            [1, 2], [1, 3]]
        
        for x in range(0, len(bts)):
            self.grade.addWidget(bts[x], coo[x][0], coo[x][1])

        self.frame_form.exec_()

    ##################################################################
    # adiciona dados dos alarmes

    def cria_database(self, *args):
        query = sql.connect('./db/data.db')
        conn = query.cursor()
        conn.execute('''CREATE TABLE IF NOT EXISTS alarmes 
            (titulo TEXT NOT NULL, hora INT(2), minuto INT(2), som TEXT);''')
        conn.execute(
            f'''INSERT INTO alarmes (titulo, hora, minuto, som)\
            VALUES (?,?,?,?)''', [args[0], args[1], args[2], args[3]])
        query.commit()
        query.close()

    #################################################################
    # recupera dados do banco de dados dos alarmes

    def ler_database(self):
        query = sql.connect('./db/data.db')
        cursor = query.cursor()
        cursor.execute('SELECT * FROM alarmes;')
        dict_alarmes = dict()
        for alarm in cursor.fetchall():
            dict_alarmes[str(alarm[0])] = list(alarm)
        query.close()

        for k in dict_alarmes.keys():
            vars()[k] = QtWidgets.QFrame()
            vars()[k + 'lb_nome'] = QtWidgets.QLabel(
                str(k) + ' '*5 + str(str(dict_alarmes[str(k)][1])) +
                ':' + str(str(dict_alarmes[str(k)][2])))
            
            vars()[k + 'lb_nome'].setStyleSheet('border-radius: 10px; ' +
                'background: teal; color: #fff; font: 100 14pt "Arial";\
                padding: 100px;')
            
            self.grid_frame.addWidget(vars()[k + 'lb_nome'])
        return dict_alarmes


    ####################################################################
    # pega os arquivos de audio

    def get_file(self):
         self.arquivo = QtWidgets.QFileDialog.getOpenFileName()

    ###################################################################
    # passa dados para a funçao de crud

    def get_var(self):
        nome = self.nm.text()
        hora = self.hr.value()
        minu = self.mi.value()
        musi = self.arquivo

        self.cria_database(nome, hora, minu, musi[0])
        self.frame_form.close()
        self.janela.close()
        self.__init__(self.pai)
    
    ###################################################################
    # desenha retira alarmes ....
    
    def retirar(self):
        dados = self.ler_database()
        self.lista = QtWidgets.QListWidget(self.janela)
        for x in dados.values():
            self.lista.addItem(x[0])

        self.lista.setGeometry(180, 100, 150, 250)
        self.lista.setStyleSheet('color: #fff;')

        bt = QtWidgets.QPushButton('Retirar', self.lista)
        bt.setStyleSheet('background: teal; color; white; border-radius: 10px;')
        bt.setGeometry(100, 220, 40, 20)
        bt.clicked.connect(self.retirar_)
        self.lista.show()
    
    ##################################################################
    # retira de fato

    def retirar_(self):
        nome = self.lista.currentItem().text()
        print(nome)
        con = sql.connect('./db/data.db')
        cur = con.cursor()
        cur.execute('DELETE FROM alarmes WHERE titulo=(?)', [nome])
        con.commit()
        con.close()
        self.lista.close()
        self.janela.close()
        self.__init__(self.pai)

        
