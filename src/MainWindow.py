import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QComboBox,QPushButton,QGridLayout,QWidget,QLabel,QErrorMessage,QHBoxLayout
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPainter,QPixmap,QIcon

import Conexion #archivo de la conexión con Neo4j para hacer consultas
import Estimate #archivo donde va el algotirmo de calculo

class MainWindow(QWidget):#QMainWindow
    
    def __init__(self,teams,conexion):#le pasamos la conexión al constructor para que lo pueda usar la clase estimate
        QWidget.__init__(self)#QMainWindow
        
        self.teams = teams
        self.conexion = conexion
        
        self.gridLayout = QGridLayout(self)
        self.setLayout(self.gridLayout)
        self.setFixedSize(QSize(500, 300))    
        self.setWindowTitle("SAJEF") 
        self.setWindowIcon(QIcon('../resources/iconmonstr-soccer-1-240.png'))
        
        self.team1 = QComboBox(self)
        self.team2 = QComboBox(self)
        self.elegir1 = QLabel("Elija el primer equipo")
        self.elegir2 = QLabel("Elija el segundo equipo")
        #Añadidos para hacer hueco
        """
        self.elegir3 = QLabel("")
        self.elegir4 = QLabel("")
        self.elegir5 = QLabel("")
        self.elegir6 = QLabel("")
        """
        self.acept = QPushButton("Aceptar",self)
        self.acept.clicked.connect(self.accept_button) #evento para manejar el click del boton aceptar
        
        self.gridLayout.addWidget(self.elegir1,0,0)
        self.gridLayout.addWidget(self.elegir2,0,2)
        """
        self.gridLayout.addWidget(self.elegir3,2,0)
        self.gridLayout.addWidget(self.elegir4,3,2)
        self.gridLayout.addWidget(self.elegir5,4,0)
        self.gridLayout.addWidget(self.elegir6,5,2)
        """
        self.gridLayout.addWidget(self.team1,1,0)
        self.gridLayout.addWidget(self.acept,1,1)
        self.gridLayout.addWidget(self.team2,1,2)



        #self.hbox = QHBoxLayout()
        #self.gridLayout.addLayout(self.hbox,2,1)
        self.labelImage = QLabel(self)
        self.pixmap = QPixmap("../resources/ball-soccer-600x400.jpg")
        self.labelImage.setPixmap(self.pixmap)
        self.gridLayout.addWidget(self.labelImage,2, 0, 2, 0)
        #self.hbox.addWidget(self.labelImage)

        self.errorTeam = QErrorMessage()
        self.errorTeam.setFixedSize(250,150)
        
        for index,item in enumerate(teams):
            self.team1.addItem(item)     
            self.team2.addItem(item)
            self.team1.setItemIcon(index, QIcon('../resources/iconmonstr-soccer-1-240.png'))
            self.team2.setItemIcon(index, QIcon('../resources/iconmonstr-soccer-1-240.png'))

    def accept_button(self):
        if str(self.team1.currentText()) == str(self.team2.currentText()):#si los dos equipos son el mismo,mostramos un error
            self.errorTeam.showMessage("No puedes elegir el mismo equipo.")
        else:#si pulsa el boton de aceptar y es correcto, primero tenemos que obtener de la base de datos los jugadores de los dos equipos y tambien las posiciones en las que juegan
            Estimate.Estimate(self.conexion,str(self.team1.currentText()),str(self.team2.currentText())) #creamos el nuevo objeto y ya se encarga de llamar a todos los métodos el solo
            
    """    
    #Para poner el background sobrescribimos el QWidget
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), QPixmap("../resources/ball-soccer-600x400.jpg"))
        QWidget.paintEvent(self, event)
    """
        
        
        
if __name__ == "__main__":
    #Conexión y consulta
    conexion = Conexion.Neo4j("bolt://localhost:11006", "neo4j", "SIBI20")
    teams = conexion.query("MATCH (p)-[r:PLAYS]->(c) RETURN DISTINCT c.id")
    
    #Ventana
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow(teams,conexion)
    mainWin.show()
    sys.exit( app.exec_() )
    
    conexion.close() #igual hay que moverlo