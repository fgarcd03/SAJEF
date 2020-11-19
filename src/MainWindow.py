import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QComboBox,QPushButton,QGridLayout,QWidget,QLabel
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPainter,QPixmap

import Conexion #archivo de la conexión con Neo4j para hacer consultas


class MainWindow(QWidget):#QMainWindow
    
    def __init__(self,teams):
        QWidget.__init__(self)#QMainWindow
        
        self.grid_layout = QGridLayout(self)
        self.setLayout(self.grid_layout)
        self.setFixedSize(QSize(600, 400))    
        self.setWindowTitle("SAJEF") 
        self.teams = teams
        
        self.team1 = QComboBox(self)
        self.team2 = QComboBox(self)
        self.elegir1 = QLabel("Elija el primer equipo")
        self.elegir2 = QLabel("Elija el segundo equipo")
        self.errorEquipo = QLabel("Ha elegido el mismo equipo")
        self.errorEquipo.hide() #La ocultamos, solo aparecera para mostrar error
        self.acept = QPushButton("Aceptar",self)
        self.acept.clicked.connect(self.accept_button) #evento para manejar el click del boton aceptar
        
        self.grid_layout.addWidget(self.elegir1,0,0)
        self.grid_layout.addWidget(self.errorEquipo,0,1)
        self.grid_layout.addWidget(self.elegir2,0,2)
        self.grid_layout.addWidget(self.team1,1,0)
        self.grid_layout.addWidget(self.acept,1,1)
        self.grid_layout.addWidget(self.team2,1,2)

        for item in teams:
            self.team1.addItem(item)     
            self.team2.addItem(item)

    def accept_button(self):
        if str(self.team1.currentText()) == str(self.team2.currentText()):#si los dos equipos son el mismo,mostramos un error
            self.errorEquipo.show()
        else:
            pass
            
        
    #Para poner el background sobrescribimos el QWidget
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), QPixmap("../resources/ball-soccer-600x400.jpg"))
        QWidget.paintEvent(self, event)

        
        
        
if __name__ == "__main__":
    #Conexión y consulta
    conexion = Conexion.Neo4j("bolt://localhost:11006", "neo4j", "SIBI20")
    teams = conexion.query("MATCH (p)-[r:PLAYS]->(c) RETURN DISTINCT c.id")
    conexion.close()
    
    #Ventana
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow(teams)
    mainWin.show()
    sys.exit( app.exec_() )