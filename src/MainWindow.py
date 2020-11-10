import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow,QComboBox,QPushButton
from PyQt5.QtCore import QSize

stylesheet = """
    MainWindow {
        background-image: url("../resources/ball-soccer-600x400"); 
        background-repeat: no-repeat; 
        background-position: center;
    }
"""

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setFixedSize(QSize(600, 400))    
        self.setWindowTitle("SAJEF") 
        
        equipo1 = QComboBox(self)
        equipo1.move(50,10)
        equipo2 = QComboBox(self)
        equipo2.move(450,10)
        aceptar = QPushButton("Aceptar",self)
        aceptar.move(250,50)
     

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.setStyleSheet(stylesheet)
    mainWin.show()
    sys.exit( app.exec_() )