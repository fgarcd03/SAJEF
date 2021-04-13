#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QComboBox,QPushButton,QGridLayout,QWidget,QLabel,QErrorMessage,QListWidget,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt #para el Qt.Horizontal

import Conexion #archivo de la conexión con Neo4j para hacer consultas
import Estimate #archivo donde va el algotirmo de cálculo

class MainWindow(QWidget):
    
    def __init__(self,teams,conexion,parent=None):#le pasamos la conexión al constructor para que lo pueda usar la clase estimate
        super().__init__(parent)

        self.teams = teams
        self.conexion = conexion
        
        self.setWindowTitle("SAJEF") 
        self.setWindowIcon(QIcon('../resources/iconmonstr-soccer-1-240.png'))
        #self.setFixedSize(500, 500)
        
        self.gridLayout = QGridLayout(self)
        self.setLayout(self.gridLayout)
        self.hBoxLayoutPorteria = QVBoxLayout() #metemos la label y la lista de items
        self.hBoxLayoutDefensa = QVBoxLayout()
        self.hBoxLayoutCentro = QVBoxLayout()
        self.hBoxLayoutAtaque = QVBoxLayout()
        
        self.errorTeam = QErrorMessage()
        self.listItemPorteria = QListWidget()
        self.listItemDefensa = QListWidget()
        self.listItemCentro = QListWidget() #lista de items
        self.listItemAtaque = QListWidget()
        self.team1 = QComboBox(self)
        self.team2 = QComboBox(self)
        self.team2.currentTextChanged.connect(self.on_combobox_changed)
        self.choose1 = QLabel("Elija su Equipo")
        self.choose2 = QLabel("Elija el Equipo Rival")
        self.porteria = QLabel("Portería")
        self.defensa = QLabel("Defensa")
        self.centro = QLabel("Centro")
        self.ataque = QLabel("Ataque")
        self.porteria.setAlignment(Qt.AlignCenter)
        self.defensa.setAlignment(Qt.AlignCenter)
        self.centro.setAlignment(Qt.AlignCenter)
        self.ataque.setAlignment(Qt.AlignCenter)
        self.acept = QPushButton("Aceptar")
        self.defaultTeam = QPushButton("Equipo por Defecto")
        self.acept.clicked.connect(self.accept_button) #evento para manejar el click del boton aceptar
        self.defaultTeam.clicked.connect(self.defaultTeam_button)
        
        self.gridLayout.addWidget(self.choose1,0,0)
        self.gridLayout.addWidget(self.choose2,0,3)
        self.gridLayout.addWidget(self.team1,1,0)
        self.gridLayout.addWidget(self.acept,1,1)
        self.gridLayout.addWidget(self.team2,1,3)
        self.gridLayout.addWidget(self.defaultTeam,1,2)
        self.hBoxLayoutPorteria.addWidget(self.porteria)
        self.hBoxLayoutPorteria.addWidget(self.listItemPorteria)
        self.gridLayout.addLayout(self.hBoxLayoutPorteria,2,0,4,1)
        self.hBoxLayoutDefensa.addWidget(self.defensa)
        self.hBoxLayoutDefensa.addWidget(self.listItemDefensa)
        self.gridLayout.addLayout(self.hBoxLayoutDefensa,2,1,4,1)
        self.hBoxLayoutCentro.addWidget(self.centro)
        self.hBoxLayoutCentro.addWidget(self.listItemCentro)
        self.gridLayout.addLayout(self.hBoxLayoutCentro,2,2,4,1)
        self.hBoxLayoutAtaque.addWidget(self.ataque)
        self.hBoxLayoutAtaque.addWidget(self.listItemAtaque)
        self.gridLayout.addLayout(self.hBoxLayoutAtaque,2,3,4,1)
        
        for index,item in enumerate(teams):
            self.team1.addItem(item[2:-2])     
            self.team2.addItem(item[2:-2])
            self.team1.setItemIcon(index, QIcon('../resources/iconmonstr-soccer-1-240.png'))
            self.team2.setItemIcon(index, QIcon('../resources/iconmonstr-soccer-1-240.png'))

        
    def on_combobox_changed(self):
        #eliminamos los itemAntiguos
        self.listItemPorteria.clear()
        self.listItemDefensa.clear()
        self.listItemCentro.clear()
        self.listItemAtaque.clear()
        
        #buscamos los jugadores del equipo
        team2 = str(self.team2.currentText())
        team2 = self.conexion.query("MATCH (p)-[r:PLAYS]->(c) WHERE c.id='{team}' RETURN DISTINCT p.name,r.teamPosition".format(team=team2))

        #añadimos los jugadores con los checkboxes
        for player in team2:#creamos una lista de comboBoxes de tamaño los jugadores de cada equipo
            itemPlayer = QtWidgets.QListWidgetItem(player[2:-2].replace("'",""))#creamos un item con el jugador
            itemPlayer.setFlags(itemPlayer.flags() | Qt.ItemIsUserCheckable)
            itemPlayer.setCheckState(Qt.Unchecked) #ponemos la checkbox a desactivado
            if(player.split("'")[3] == "GK" or player.split("'")[3] == "SUB,GK" or player.split("'")[3] == "RES,GK"):#dependiendo de lo que sea lo metemos a un layout diferente(la \ sirve para espacar caracteres)
                self.listItemPorteria.addItem(itemPlayer) #y añadimos el item a la lista de Items
            if(player.split("'")[3] == "CB" or player.split("'")[3] == "SUB,CB" or player.split("'")[3] == "RES,CB" or player.split("'")[3] == "LCB" or player.split("'")[3] == "SUB,LCB" or player.split("'")[3] == "RES,LCB" or player.split("'")[3] == "RCB" or player.split("'")[3] == "SUB,RCB" or player.split("'")[3] == "RES,RCB" or player.split("'")[3] == "LB" or player.split("'")[3] == "SUB,LB" or player.split("'")[3] == "RES,LB" or player.split("'")[3] == "LWB" or player.split("'")[3] == "SUB,LWB" or player.split("'")[3] == "RES,LWB" or player.split("'")[3] == "RB" or player.split("'")[3] == "SUB,RB" or player.split("'")[3] == "RES,RB" or player.split("'")[3] == "RWB" or player.split("'")[3] == "SUB,RWB" or player.split("'")[3] == "RES,RWB"):
                self.listItemDefensa.addItem(itemPlayer)   
            if(player.split("'")[3] == "CDM" or player.split("'")[3] == "SUB,CDM" or player.split("'")[3] == "RES,CDM" or player.split("'")[3] == "LDM" or player.split("'")[3] == "SUB,LDM" or player.split("'")[3] == "RES,LDM" or player.split("'")[3] == "RDM" or player.split("'")[3] == "SUB,RDM" or player.split("'")[3] == "RES,RDM" or player.split("'")[3] == "CM" or player.split("'")[3] == "SUB,CM" or player.split("'")[3] == "RES,CM" or player.split("'")[3] == "LM" or player.split("'")[3] == "SUB,LM" or player.split("'")[3] == "RES,LM" or player.split("'")[3] == "LCM" or player.split("'")[3] == "SUB,LCM" or player.split("'")[3] == "RES,LCM" or player.split("'")[3] == "RM" or player.split("'")[3] == "SUB,RM" or player.split("'")[3] == "RES,RM" or player.split("'")[3] == "RCM" or player.split("'")[3] == "SUB,RCM" or player.split("'")[3] == "RES,RCM" or player.split("'")[3] == "CAM" or player.split("'")[3] == "SUB,CAM" or player.split("'")[3] == "RES,CAM" or player.split("'")[3] == "LAM" or player.split("'")[3] == "SUB,LAM" or player.split("'")[3] == "RES,LAM" or player.split("'")[3] == "RAM" or player.split("'")[3] == "SUB,RAM" or player.split("'")[3] == "RES,RAM"):
                self.listItemCentro.addItem(itemPlayer)
            if(player.split("'")[3] == "CF" or player.split("'")[3] == "SUB,CF" or player.split("'")[3] == "RES,CF" or player.split("'")[3] == "LS" or player.split("'")[3] == "SUB,LS" or player.split("'")[3] == "RES,LS" or player.split("'")[3] == "RS" or player.split("'")[3] == "SUB,RS" or player.split("'")[3] == "RES,RS" or player.split("'")[3] == "ST" or player.split("'")[3] == "SUB,ST" or player.split("'")[3] == "RES,ST" or player.split("'")[3] == "LW" or player.split("'")[3] == "SUB,LW" or player.split("'")[3] == "RES,LW" or player.split("'")[3] == "RW" or player.split("'")[3] == "SUB,RW" or player.split("'")[3] == "RES,RW"):
                self.listItemAtaque.addItem(itemPlayer)

    def defaultTeam_button(self):
         for index in range(self.listItemPorteria.count()):
            if "SUB" in self.listItemPorteria.item(index).text() or "RES" in self.listItemPorteria.item(index).text():
                self.listItemPorteria.item(index).setCheckState(Qt.Unchecked)# si son suplentes los desmarcamos
            else:
                self.listItemPorteria.item(index).setCheckState(Qt.Checked)# si no lo son marcamos
                
         for index in range(self.listItemDefensa.count()):
            if "SUB" in self.listItemDefensa.item(index).text() or "RES" in self.listItemDefensa.item(index).text():
                self.listItemDefensa.item(index).setCheckState(Qt.Unchecked)
            else:
                self.listItemDefensa.item(index).setCheckState(Qt.Checked)
                
         for index in range(self.listItemCentro.count()):
            if "SUB" in self.listItemCentro.item(index).text() or "RES" in self.listItemCentro.item(index).text():
                self.listItemCentro.item(index).setCheckState(Qt.Unchecked)
            else:
                self.listItemCentro.item(index).setCheckState(Qt.Checked)
                
         for index in range(self.listItemAtaque.count()):
            if "SUB" in self.listItemAtaque.item(index).text() or "RES" in self.listItemAtaque.item(index).text():
                self.listItemAtaque.item(index).setCheckState(Qt.Unchecked)
            else:
                self.listItemAtaque.item(index).setCheckState(Qt.Checked)
                
    def accept_button(self):
        counter = 0
        for index in range(self.listItemPorteria.count()):
            if self.listItemPorteria.item(index).checkState() == Qt.Checked:
                counter = counter + 1
        for index in range(self.listItemDefensa.count()):
            if self.listItemDefensa.item(index).checkState() == Qt.Checked:
                counter = counter + 1
        for index in range(self.listItemCentro.count()):
            if self.listItemCentro.item(index).checkState() == Qt.Checked:
                counter = counter + 1
        for index in range(self.listItemAtaque.count()):
            if self.listItemAtaque.item(index).checkState() == Qt.Checked:
                counter = counter + 1
                
        if str(self.team1.currentText()) == str(self.team2.currentText()):#si los dos equipos son el mismo,mostramos un error
            self.errorTeam.showMessage("No puedes elegir el mismo equipo.")
        elif counter != 11:
            self.errorTeam.showMessage("El número de jugadores elegido no es 11.")
        else:#si pulsa el boton de aceptar y es correcto, primero tenemos que obtener de la base de datos los jugadores de los dos equipos y tambien las posiciones en las que juegan
            Estimate.Estimate(self.conexion,str(self.team1.currentText()),str(self.team2.currentText())) #creamos el nuevo objeto y ya se encarga de llamar a todos los métodos el solo
    
                
if __name__ == "__main__":
    #Conexión y consulta
    conexion = Conexion.Neo4j("bolt://localhost:7687", "neo4j", "SIBI20")
    teams = conexion.query("MATCH (p)-[r:PLAYS]->(c) RETURN DISTINCT c.id")
    
    #Ventana
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow(teams,conexion) 
    mainWin.show()
    sys.exit( app.exec_() )
    
    conexion.close()
