#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QComboBox,QPushButton,QGridLayout,QWidget,QLabel,QErrorMessage,QCheckBox,QHBoxLayout,QScrollBar,QScrollArea,QWidget,QFormLayout,QScroller,QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt #para el Qt.Horizontal

import Conexion #archivo de la conexión con Neo4j para hacer consultas
import Estimate #archivo donde va el algotirmo de cálculo

class MainWindow(QWidget):
    
    def __init__(self,teams,conexion,parent=None):#le pasamos la conexión al constructor para que lo pueda usar la clase estimate
        super().__init__(parent)
        #self.widget = QWidget()#para el scroll
        self.checkBoxList = [] #lista de checkboxes de los jugadores
        self.teams = teams
        self.conexion = conexion
        
        self.gridLayout = QGridLayout(self)
        self.setLayout(self.gridLayout)
        self.hBoxSubLayoutPorteria = QHBoxLayout() #en el sublayout metemos el tipo y los jugadores de este tipo
        self.hBoxSubLayoutDefensa = QHBoxLayout()
        self.hBoxSubLayoutCentro = QHBoxLayout()
        self.hBoxSubLayoutAtaque = QHBoxLayout()
        self.hBoxLayoutPorteria = QHBoxLayout() #en layout horizontal metemos el sublayout para que al meterlo al gridlayout cuente como metemos un solo widget y no 2
        self.hBoxLayoutDefensa = QHBoxLayout()
        self.hBoxLayoutCentro = QHBoxLayout()
        self.hBoxLayoutAtaque = QHBoxLayout()
        
       
        self.scroll_area = QScrollArea()
        self.gridLayout.addWidget(self.scroll_area,2,0,4,3)
        self.scroll_widget = QWidget()
        self.scroll_layout = QFormLayout(self.scroll_widget)
        self.scroll_layout.addRow(self.gridLayout)
        self.scroll_area.setWidget(self.scroll_widget)

        
        """
        
        
        self.centralwid = QScrollArea()
        #self.centralwid.setOrientation(Qt.Horizontal())
        self.hBoxLayoutAtaque.add(self.hBoxLayoutAtaque)
        """
        self.setWindowTitle("SAJEF") 
        self.setWindowIcon(QIcon('../resources/iconmonstr-soccer-1-240.png'))
        self.setFixedSize(500, 500)
        
        self.team1 = QComboBox(self)
        self.team2 = QComboBox(self)
        self.team2.currentTextChanged.connect(self.on_combobox_changed)
        self.choose1 = QLabel("Elija su Equipo")
        self.choose2 = QLabel("Elija el Equipo Rival")
        self.porteria = QLabel("Portería")
        self.defensa = QLabel("Defensa")
        self.centro = QLabel("Centro del Campo")
        self.delantera = QLabel("Ataque")
        self.acept = QPushButton("Aceptar")
        self.defaultTeam = QPushButton("Equipo por Defecto")
        self.acept.clicked.connect(self.accept_button) #evento para manejar el click del boton aceptar
        self.defaultTeam.clicked.connect(self.defaultTeam_button)
        
        self.gridLayout.addWidget(self.choose1,0,0)
        self.gridLayout.addWidget(self.choose2,0,2)
        self.gridLayout.addWidget(self.team1,1,0)
        self.gridLayout.addWidget(self.acept,0,1)
        self.gridLayout.addWidget(self.team2,1,2)
        self.gridLayout.addWidget(self.defaultTeam,1,1)

        self.hBoxLayoutPorteria.addWidget(self.porteria)
        self.hBoxLayoutDefensa.addWidget(self.defensa)
        self.hBoxLayoutCentro.addWidget(self.centro)
        self.hBoxLayoutAtaque.addWidget(self.delantera)
        
        self.errorTeam = QErrorMessage()
        
        for index,item in enumerate(teams):
            self.team1.addItem(item[2:-2])     
            self.team2.addItem(item[2:-2])
            self.team1.setItemIcon(index, QIcon('../resources/iconmonstr-soccer-1-240.png'))
            self.team2.setItemIcon(index, QIcon('../resources/iconmonstr-soccer-1-240.png'))

        
    def on_combobox_changed(self):
        #eliminamos los widgets antiguos
        for checkBox in self.checkBoxList:
            self.gridLayout.removeWidget(checkBox)#ojo poner el layout que este mas encima
        #buscmaos los jugadores del equipo
        team2 = str(self.team2.currentText())
        team2 = self.conexion.query("MATCH (p)-[r:PLAYS]->(c) WHERE c.id='{team}' RETURN DISTINCT p.name,r.teamPosition".format(team=team2))
        self.checkBoxList = []
        #añadimos los jugadores con los checkboxes
        for player in team2:#creamos una lista de comboBoxes de tamaño los jugadores de cada equipo
            self.checkBox = QCheckBox(player)
            self.checkBoxList.append(self.checkBox)

            if(player.split("'")[3] == "GK" or player.split("'")[3] == "SUB,GK" or player.split("'")[3] == "RES,GK"):#dependiendo de lo que sea lo metemos a un layout diferente(la \ sirve para espacar caracteres)
                self.hBoxLayoutPorteria.addWidget(self.checkBox)#añadimos las checkboxes al layout
                
            if(player.split("'")[3] == "CB" or player.split("'")[3] == "SUB,CB" or player.split("'")[3] == "RES,CB" or player.split("'")[3] == "LCB" or player.split("'")[3] == "SUB,LCB" or player.split("'")[3] == "RES,LCB" or player.split("'")[3] == "RCB" or player.split("'")[3] == "SUB,RCB" or player.split("'")[3] == "RES,RCB" or player.split("'")[3] == "LB" or player.split("'")[3] == "SUB,LB" or player.split("'")[3] == "RES,LB" or player.split("'")[3] == "LWB" or player.split("'")[3] == "SUB,LWB" or player.split("'")[3] == "RES,LWB" or player.split("'")[3] == "RB" or player.split("'")[3] == "SUB,RB" or player.split("'")[3] == "RES,RB" or player.split("'")[3] == "RWB" or player.split("'")[3] == "SUB,RWB" or player.split("'")[3] == "RES,RWB"):
                self.hBoxSubLayoutDefensa.addWidget(self.checkBox)
            
            if(player.split("'")[3] == "CDM" or player.split("'")[3] == "SUB,CDM" or player.split("'")[3] == "RES,CDM" or player.split("'")[3] == "LDM" or player.split("'")[3] == "SUB,LDM" or player.split("'")[3] == "RES,LDM" or player.split("'")[3] == "RDM" or player.split("'")[3] == "SUB,RDM" or player.split("'")[3] == "RES,RDM" or player.split("'")[3] == "CM" or player.split("'")[3] == "SUB,CM" or player.split("'")[3] == "RES,CM" or player.split("'")[3] == "LM" or player.split("'")[3] == "SUB,LM" or player.split("'")[3] == "RES,LM" or player.split("'")[3] == "LCM" or player.split("'")[3] == "SUB,LCM" or player.split("'")[3] == "RES,LCM" or player.split("'")[3] == "RM" or player.split("'")[3] == "SUB,RM" or player.split("'")[3] == "RES,RM" or player.split("'")[3] == "RCM" or player.split("'")[3] == "SUB,RCM" or player.split("'")[3] == "RES,RCM" or player.split("'")[3] == "CAM" or player.split("'")[3] == "SUB,CAM" or player.split("'")[3] == "RES,CAM" or player.split("'")[3] == "LAM" or player.split("'")[3] == "SUB,LAM" or player.split("'")[3] == "RES,LAM" or player.split("'")[3] == "RAM" or player.split("'")[3] == "SUB,RAM" or player.split("'")[3] == "RES,RAM"):
                self.hBoxLayoutCentro.addWidget(self.checkBox)
            
            if(player.split("'")[3] == "CF" or player.split("'")[3] == "SUB,CF" or player.split("'")[3] == "RES,CF" or player.split("'")[3] == "LS" or player.split("'")[3] == "SUB,LS" or player.split("'")[3] == "RES,LS" or player.split("'")[3] == "RS" or player.split("'")[3] == "SUB,RS" or player.split("'")[3] == "RES,RS" or player.split("'")[3] == "ST" or player.split("'")[3] == "SUB,ST" or player.split("'")[3] == "RES,ST" or player.split("'")[3] == "LW" or player.split("'")[3] == "SUB,LW" or player.split("'")[3] == "RES,LW" or player.split("'")[3] == "RW" or player.split("'")[3] == "SUB,RW" or player.split("'")[3] == "RES,RW"):
                self.hBoxLayoutAtaque.addWidget(self.checkBox)
        
        self.hBoxLayoutPorteria.addLayout(self.hBoxSubLayoutPorteria)
        self.gridLayout.addLayout(self.hBoxLayoutPorteria,2,0,1,3) #el tercer número indica el número de filas que quiero juntar y el cuarto el número de columnas        
        self.hBoxLayoutDefensa.addLayout(self.hBoxSubLayoutDefensa)
        self.gridLayout.addLayout(self.hBoxLayoutDefensa,3,0,1,3)
        self.hBoxLayoutCentro.addLayout(self.hBoxSubLayoutCentro)
        self.gridLayout.addLayout(self.hBoxLayoutCentro,4,0,1,3)
        self.hBoxLayoutAtaque.addLayout(self.hBoxSubLayoutAtaque)
        self.gridLayout.addLayout(self.hBoxLayoutAtaque,5,0,1,3)
        

    def defaultTeam_button(self):
        for checkBox in self.checkBoxList:#si es un jugador titular, lo marcamos, y si no lo demascarcamos
            if "SUB" in checkBox.text() or "RES" in checkBox.text():
                checkBox.setChecked(False) #NO TESTEADO
            else:
                checkBox.setChecked(True)
                
    def accept_button(self):
        contador = 0
        for checkBox in self.checkBoxList:#contamos el número de checkboxes marcados
            if checkBox.isChecked():
                contador = contador + 1
        if str(self.team1.currentText()) == str(self.team2.currentText()):#si los dos equipos son el mismo,mostramos un error
            self.errorTeam.showMessage("No puedes elegir el mismo equipo.")
        elif contador != 11:
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
