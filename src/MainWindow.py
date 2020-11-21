import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QComboBox,QPushButton,QGridLayout,QWidget,QLabel,QErrorMessage
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPainter,QPixmap

import Conexion #archivo de la conexión con Neo4j para hacer consultas
import Estimate #archivo donde va el algotirmo de calculo

class MainWindow(QWidget):#QMainWindow
    
    def __init__(self,teams,conexion):#le pasamos la conexión al constructor para que lo pueda usar la clase estimate
        QWidget.__init__(self)#QMainWindow
        
        self.teams = teams
        self.conexion = conexion
        
        self.grid_layout = QGridLayout(self)
        self.setLayout(self.grid_layout)
        self.setFixedSize(QSize(600, 400))    
        self.setWindowTitle("SAJEF") 
        
        self.team1 = QComboBox(self)
        self.team2 = QComboBox(self)
        self.elegir1 = QLabel("Elija el primer equipo")
        self.elegir2 = QLabel("Elija el segundo equipo")
        self.acept = QPushButton("Aceptar",self)
        self.acept.clicked.connect(self.accept_button) #evento para manejar el click del boton aceptar
        
        self.grid_layout.addWidget(self.elegir1,0,0)
        self.grid_layout.addWidget(self.elegir2,0,2)
        self.grid_layout.addWidget(self.team1,1,0)
        self.grid_layout.addWidget(self.acept,1,1)
        self.grid_layout.addWidget(self.team2,1,2)


        self.errorTeam = QErrorMessage()
        self.errorTeam.setFixedSize(250,150)
        
        for item in teams:
            self.team1.addItem(item)     
            self.team2.addItem(item)

    def accept_button(self):
        if str(self.team1.currentText()) == str(self.team2.currentText()):#si los dos equipos son el mismo,mostramos un error
            self.errorTeam.showMessage("No puedes elegir el mismo equipo.")
        else:#si pulsa el boton de aceptar y es correcto, primero tenemos que obtener de la base de datos los jugadores de los dos equipos y tambien las posiciones en las que juegan
            Estimate.Estimate(self.conexion,str(self.team1.currentText()),str(self.team2.currentText())) #creamos el nuevo objeto y ya se encarga de llamar a todos los métodos el solo
            
        
    #Para poner el background sobrescribimos el QWidget
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), QPixmap("../resources/ball-soccer-600x400.jpg"))
        QWidget.paintEvent(self, event)

        
        
        
if __name__ == "__main__":
    #Conexión y consulta
    conexion = Conexion.Neo4j("bolt://localhost:7687", "neo4j", "SIBI20")
    teams = conexion.query("MATCH (p)-[r:PLAYS]->(c) RETURN DISTINCT c.id")
    
    #Ventana
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow(teams,conexion)
    mainWin.show()
    sys.exit( app.exec_() )
    
    conexion.close() #igual hay que moverlo