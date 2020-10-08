# função que retorna um dicionario contendo as imagens
from PySide2.QtGui import QPixmap
from os import path, listdir

def imagens_():
    dicio = dict()
    diretorio = path.abspath('.') + '\\img\\'
    
    for x in listdir(diretorio):
        dicio[str(x.replace('.svg', ''))] = QPixmap(diretorio + x)
    return dicio
