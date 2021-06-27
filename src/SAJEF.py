#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Interfaz donde se elijen los equipos y jugadores
import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QComboBox,QPushButton,QGridLayout,QWidget,QLabel,QErrorMessage,QListWidget,QVBoxLayout,QCheckBox,QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from threading import Thread

import Conexion #archivo de la conexión con Neo4j para hacer consultas
import Estimate #archivo donde va el algoritmo de cálculo

class MainWindow(QWidget):
    
    def __init__(self,teams,conexion,parent=None):
        super().__init__(parent)
        self.teams = teams
        self.conexion = conexion
        
        self.mainTeam2 = [] #El equipo que creará el usuario opcionalmente
        
        self.setWindowTitle("SAJEF") 
        self.setWindowIcon(QIcon('{}/../resources/iconmonstr-soccer-1-240.png'.format(os.path.dirname(os.path.realpath(__file__)))))
        
        self.gridLayout = QGridLayout(self)
        self.setLayout(self.gridLayout)
        self.hBoxLayoutPorteria = QVBoxLayout()
        self.hBoxLayoutDefensa = QVBoxLayout()
        self.hBoxLayoutCentro = QVBoxLayout()
        self.hBoxLayoutAtaque = QVBoxLayout()
        
        self.errorTeam = QMessageBox()
        self.errorTeam.setWindowTitle("Error")
        self.errorTeam.setText("No puedes elegir el mismo equipo")
        self.errorTeam.setIcon(QMessageBox.Critical)
        self.error11 = QMessageBox()
        self.error11.setWindowTitle("Error")
        self.error11.setText("El equipo tiene que estar compuesto por exactamente 11 jugadores")
        self.error11.setIcon(QMessageBox.Critical)
        self.errorPos = QMessageBox()
        self.errorPos.setWindowTitle("Error")
        self.errorPos.setText("Hay demasiados jugadores en una misma posición, revise de nuevo.")
        self.errorPos.setIcon(QMessageBox.Critical)
        self.listItemPorteria = QListWidget()
        self.listItemDefensa = QListWidget()
        self.listItemCentro = QListWidget()
        self.listItemAtaque = QListWidget()
        self.combinatoricsTeam1 = QCheckBox("¿Quiere usar combinatoria para su equipo?")
        self.combinatoricsTeam2 = QCheckBox("¿Quiere usar combinatoria para el equipo rival?")
        self.combinatoricsTeam2.clicked.connect(self.combinatoricsTeam2CheckBox)
        self.team1 = QComboBox(self)
        self.team2 = QComboBox(self)
        self.team2.currentTextChanged.connect(self.combobox2)
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
        self.acept.clicked.connect(self.acceptButton)
        self.defaultTeam.clicked.connect(self.defaultTeamButton)
        
        self.gridLayout.addWidget(self.choose1,0,0)
        self.gridLayout.addWidget(self.combinatoricsTeam1,0,1)
        self.gridLayout.addWidget(self.combinatoricsTeam2,0,2)
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
            self.team1.setItemIcon(index, QIcon('{}/../resources/iconmonstr-soccer-1-240.png'.format(os.path.dirname(os.path.realpath(__file__)))))
            self.team2.setItemIcon(index, QIcon('{}/../resources/iconmonstr-soccer-1-240.png'.format(os.path.dirname(os.path.realpath(__file__)))))

        
    def combobox2(self):

        self.listItemPorteria.clear()
        self.listItemDefensa.clear()
        self.listItemCentro.clear()
        self.listItemAtaque.clear()

        team2 = str(self.team2.currentText())
        team2 = self.conexion.query("MATCH (p)-[r:PLAYS]->(c) WHERE c.id='{team}' RETURN DISTINCT p.name,r.teamPosition".format(team=team2))

        for player in team2:
            itemPlayer = QtWidgets.QListWidgetItem(player[2:-2].replace("'",""))
            itemPlayer.setFlags(itemPlayer.flags() | Qt.ItemIsUserCheckable)
            itemPlayer.setCheckState(Qt.Unchecked)
            if "GK" in player:
                self.listItemPorteria.addItem(itemPlayer)
            if "CB" in player or "LCB" in player or "RCB" in player or "LB" in player or "LWB" in player or "RB" in player or "RWB" in player:
                self.listItemDefensa.addItem(itemPlayer)   
            if "CDM" in player or "LDM" in player or "RDM" in player or "CM" in player or "LM" in player or "LCM" in player or "RM" in player or "RCM" in player or "CAM" in player or "LAM" in player or "RAM" in player:
                self.listItemCentro.addItem(itemPlayer)
            if "CF" in player or "LS" in player or "RS" in player or "ST" in player or "LW" in player or "RW" in player and "LWB" not in player and "RWB" not in player:
                self.listItemAtaque.addItem(itemPlayer)
        
        if self.combinatoricsTeam2.isChecked():
            self.combinatoricsTeam2CheckBox()

    def defaultTeamButton(self):
         for index in range(self.listItemPorteria.count()):
            if "SUB" in self.listItemPorteria.item(index).text() or "RES" in self.listItemPorteria.item(index).text():
                self.listItemPorteria.item(index).setCheckState(Qt.Unchecked)#si son suplentes los desmarcamos
            else:
                self.listItemPorteria.item(index).setCheckState(Qt.Checked)#si no lo son, marcamos
                
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
    
    def combinatoricsTeam2CheckBox(self):
        if self.combinatoricsTeam2.isChecked():
            for index in range(self.listItemPorteria.count()):
                self.listItemPorteria.item(index).setFlags(self.listItemPorteria.item(index).flags() & ~Qt.ItemIsEnabled)
            for index in range(self.listItemDefensa.count()):
                self.listItemDefensa.item(index).setFlags(self.listItemDefensa.item(index).flags() & ~Qt.ItemIsEnabled)
            for index in range(self.listItemCentro.count()):
                self.listItemCentro.item(index).setFlags(self.listItemCentro.item(index).flags() & ~Qt.ItemIsEnabled)
            for index in range(self.listItemAtaque.count()):
                self.listItemAtaque.item(index).setFlags(self.listItemAtaque.item(index).flags() & ~Qt.ItemIsEnabled)
        else:
            for index in range(self.listItemPorteria.count()):
                self.listItemPorteria.item(index).setFlags(self.listItemPorteria.item(index).flags() | Qt.ItemIsEnabled)
            for index in range(self.listItemDefensa.count()):
                self.listItemDefensa.item(index).setFlags(self.listItemDefensa.item(index).flags() | Qt.ItemIsEnabled)
            for index in range(self.listItemCentro.count()):
                self.listItemCentro.item(index).setFlags(self.listItemCentro.item(index).flags() | Qt.ItemIsEnabled)
            for index in range(self.listItemAtaque.count()):
                self.listItemAtaque.item(index).setFlags(self.listItemAtaque.item(index).flags() | Qt.ItemIsEnabled)
    
    def checkRepeatedPositions(self):
        positionsDictionary = {"GK" : False, "CB" : False,"RCB" : False, "LCB" : False,"LB" : False, "LWB" : False,"RB" : False, "RWB" : False,"CDM" : False, "LDM" : False,"RDM" : False, "CM" : False,"LM" : False, "LCM" : False,"RM" : False, "RCM" : False,"CAM" : False, "LAM" : False,"RAM" : False, "CF" : False,"LS" : False, "RS" : False,"ST" : False, "LW" : False,"RW" : False}
        counterGK = counterCM = counterST = False
        counterCB = counterLRB = counterCDM = counterLRM = counterCAM = counterCF = counterLRW = 0
        for positionPlayer in self.mainTeam2:
            positionPlayer = positionPlayer.split(",")[1]
            positionPlayer = positionPlayer.replace(" RES-","")
            positionPlayer = positionPlayer.replace(" SUB-","")
            positionPlayer = positionPlayer.replace(" ","")
            
            if positionsDictionary[positionPlayer] == False:
                positionsDictionary[positionPlayer] = True
            else:
                return True
            
        return False        
    
    def acceptButton(self):
        self.mainTeam2.clear()
        counter = 0
        for index in range(self.listItemPorteria.count()):
            if self.listItemPorteria.item(index).checkState() == Qt.Checked:
                self.mainTeam2.append(self.listItemPorteria.item(index).text())
                counter = counter + 1
        for index in range(self.listItemDefensa.count()):
            if self.listItemDefensa.item(index).checkState() == Qt.Checked:
                self.mainTeam2.append(self.listItemDefensa.item(index).text())
                counter = counter + 1
        for index in range(self.listItemCentro.count()):
            if self.listItemCentro.item(index).checkState() == Qt.Checked:
                self.mainTeam2.append(self.listItemCentro.item(index).text())
                counter = counter + 1
        for index in range(self.listItemAtaque.count()):
            if self.listItemAtaque.item(index).checkState() == Qt.Checked:
                self.mainTeam2.append(self.listItemAtaque.item(index).text())
                counter = counter + 1
                
        if str(self.team1.currentText()) == str(self.team2.currentText()):
            self.errorTeam.exec_()
        elif self.combinatoricsTeam2.isChecked():
            threadComb = Thread(target = self.aceptComb) # hilo de ejecución diferente
            threadComb.start()
        elif counter != 11:
            self.error11.exec_()
        elif self.checkRepeatedPositions() == True:
            self.errorPos.exec_()
        else:
            threadNoComb = Thread(target = self.aceptNoComb) # hilo de ejecución diferente
            threadNoComb.start()

    def aceptComb(self):
        Estimate.Estimate(self.conexion,str(self.team1.currentText()),str(self.team2.currentText()),[],self.combinatoricsTeam1.isChecked(),self.combinatoricsTeam2.isChecked())
        
    def aceptNoComb(self):
        Estimate.Estimate(self.conexion,str(self.team1.currentText()),str(self.team2.currentText()),self.mainTeam2,self.combinatoricsTeam1.isChecked(),self.combinatoricsTeam2.isChecked())

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
