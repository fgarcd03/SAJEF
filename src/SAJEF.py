#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QComboBox,QPushButton,QGridLayout,QWidget,QLabel,QErrorMessage,QCheckBox,QVBoxLayout
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon

import Conexion #archivo de la conexión con Neo4j para hacer consultas
import Estimate #archivo donde va el algotirmo de cálculo

class MainWindow(QWidget):
    
    def __init__(self,teams,conexion):#le pasamos la conexión al constructor para que lo pueda usar la clase estimate
        QWidget.__init__(self)
        
        self.teams = teams
        self.conexion = conexion
        
        self.gridLayout = QGridLayout(self)
        self.setLayout(self.gridLayout)
        #self.setFixedSize(QSize(500, 300))    
        self.setWindowTitle("SAJEF") 
        self.setWindowIcon(QIcon('../resources/iconmonstr-soccer-1-240.png'))
        
        self.team1 = QComboBox(self)
        self.team2 = QComboBox(self)
        self.team2.currentTextChanged.connect(self.on_combobox_changed)
        self.elegir1 = QLabel("Elija su Equipo")
        self.elegir2 = QLabel("Elija el Equipo Rival")
        self.acept = QPushButton("Aceptar",self)
        self.acept.clicked.connect(self.accept_button) #evento para manejar el click del boton aceptar
        
        self.gridLayout.addWidget(self.elegir1,0,0)
        self.gridLayout.addWidget(self.elegir2,0,2)
        self.gridLayout.addWidget(self.team1,1,0)
        self.gridLayout.addWidget(self.acept,1,1)
        self.gridLayout.addWidget(self.team2,1,2)
        self.vBoxLayout = QVBoxLayout() #layout para poner los checkboxes de los jugadores para elegir
        
        self.errorTeam = QErrorMessage()
        self.errorTeam.setFixedSize(250,150)
    
        
        for index,item in enumerate(teams):
            self.team1.addItem(item[2:-2])     
            self.team2.addItem(item[2:-2])
            self.team1.setItemIcon(index, QIcon('../resources/iconmonstr-soccer-1-240.png'))
            self.team2.setItemIcon(index, QIcon('../resources/iconmonstr-soccer-1-240.png'))
            

        team = str(self.team2.currentText())
        team = self.conexion.query("MATCH (p)-[r:PLAYS]->(c) WHERE c.id='{team}' RETURN DISTINCT p.name,r.teamPosition".format(team=team))
        self.checkBoxList = []
        
        for player in team:#creamos una lista de comboBoxes de tamaño los jugadores de cada equipo
            self.checkBox = QCheckBox(player)    
            self.checkBoxList.append(self.checkBox)
            self.vBoxLayout.addWidget(self.checkBox,stretch=1) #añadimos las checkboxes al layout

        self.gridLayout.addLayout(self.vBoxLayout,2,1)
        
    def on_combobox_changed(self):
        
        #eliminamos los widgets antiguos
        for checkBox in self.checkBoxList:
            self.vBoxLayout.removeWidget(checkBox)
        #buscmaos los jugadores del equipo
        team2 = str(self.team2.currentText())
        team2 = self.conexion.query("MATCH (p)-[r:PLAYS]->(c) WHERE c.id='{team}' RETURN DISTINCT p.name,r.teamPosition".format(team=team2))
        self.checkBoxList = []
        #añadimos los jugadores con los checkboxes
        for player in team2:#creamos una lista de comboBoxes de tamaño los jugadores de cada equipo
            self.checkBox = QCheckBox(player)    
            self.checkBoxList.append(self.checkBox)
            self.vBoxLayout.addWidget(self.checkBox) #añadimos las checkboxes al layout
    
    def accept_button(self):
        if str(self.team1.currentText()) == str(self.team2.currentText()):#si los dos equipos son el mismo,mostramos un error
            self.errorTeam.showMessage("No puedes elegir el mismo equipo.")
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
