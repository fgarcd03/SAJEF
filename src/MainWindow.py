import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow,QComboBox,QPushButton
from PyQt5.QtCore import QSize

import conexion #archivo de la conexión con Neo4j para hacer consultas

#Para el background
stylesheet = """
    MainWindow {
        background-image: url("../resources/ball-soccer-600x400"); 
        background-repeat: no-repeat; 
        background-position: center;
    }
"""

class MainWindow(QMainWindow):
    def __init__(self,teams):
        QMainWindow.__init__(self)

        self.setFixedSize(QSize(600, 400))    
        self.setWindowTitle("SAJEF") 
        self.teams = teams
        
        team1 = QComboBox(self)
        team1.move(50,10)
        team2 = QComboBox(self)
        team2.move(450,10)
        acept = QPushButton("Aceptar",self)
        acept.move(250,10)

        for item in teams:
            team1.addItem(str(item))     
            team2.addItem(str(item))

if __name__ == "__main__":
    #Conexión y consulta
    conexion = conexion.Neo4j("bolt://localhost:11003", "neo4j", "SIBI20")
    teams = conexion.query("MATCH (p)-[r:PLAYS]->(c) RETURN c.id")
    conexion.close()
    print(teams)
    
    #Ventana
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow(teams)
    mainWin.setStyleSheet(stylesheet)
    mainWin.show()
    sys.exit( app.exec_() )