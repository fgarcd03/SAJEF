#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QComboBox,QPushButton,QGridLayout,QWidget,QLabel,QErrorMessage,QListWidget,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt #para el Qt.Horizontal

import Conexion #archivo de la conexión con Neo4j para hacer consultas
import Estimate #archivo donde va el algoritmo de cálculo

class MainWindow(QWidget):
    
    def __init__(self,teams,conexion,parent=None):#le pasamos la conexión al constructor para que lo pueda usar la clase estimate
        super().__init__(parent)
        actualPath = os.path.dirname(os.path.realpath(__file__)) #para saber el directorio actual, usado para que sea compatible con las appimages
        
        self.teams = teams
        self.conexion = conexion
        
        self.mainTeam2 = [] #El eqipo que creará el usuario
        
        self.setWindowTitle("SAJEF") 
        self.setWindowIcon(QIcon('{}/../resources/iconmonstr-soccer-1-240.png'.format(actualPath)))
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
            self.team1.setItemIcon(index, QIcon('{}/../resources/iconmonstr-soccer-1-240.png'.format(actualPath)))
            self.team2.setItemIcon(index, QIcon('{}/../resources/iconmonstr-soccer-1-240.png'.format(actualPath)))

        
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
            if "GK" in player:#dependiendo de lo que sea lo metemos a un layout diferente, si es GK o SUB-GK o RES-GK lo añade
                self.listItemPorteria.addItem(itemPlayer) #y añadimos el item a la lista de Items
            if "CB" in player or "LCB" in player or "RCB" in player or "LB" in player or "LWB" in player or "RB" in player or "RWB" in player:
                self.listItemDefensa.addItem(itemPlayer)   
            if "CDM" in player or "LDM" in player or "RDM" in player or "CM" in player or "LM" in player or "LCM" in player or "RM" in player or "RCM" in player or "CAM" in player or "LAM" in player or "RAM" in player:
                self.listItemCentro.addItem(itemPlayer)
            if "CF" in player or "LS" in player or "RS" in player or "ST" in player or "LW" in player or "RW" in player and "LWB" not in player and "RWB" not in player: #los not in son para evitar que algunos jugadores entrer en mas de un if(porque coincide el término de bésqueda)
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
    
    def checkRepeatedPositions(self):#comprobamos si hay más jugadores que posiciones disponibles, por ejemplo que no haya mas de 3 centrales
        counterGK = counterCM = counterST = False
        counterCB = counterLRB = counterCDM = counterLRM = counterCAM = counterCF = counterLRW = 0
        for player in self.mainTeam2:
            if "GK" in player:
                if counterGK:
                    return True
                counterGK = True
            if "CB" in player or "RCB" in player or "LCB" in player:
                counterCB = counterCB + 1
                if counterCB > 3: #si hay mas de 3 centrales damos error
                    return True
            if "LB" in player or "LWB" in player or "RB" in player or "RWB" in player:
                counterLRB = counterLRB + 1
                if counterLRB > 4:
                    return True
            if "CDM" in player or "LDM" in player or "RDM" in player:
                counterCDM = counterCDM + 1
                if counterCDM > 3:
                    return True
            if "CM" in player and "LCM" not in player and "RCM" not in player:
                if counterCM:
                    return True
                counterCM = True  
            if "LM" in player or "LCM" in player or "RM" in player or "RCM" in player:
                counterLRM = counterLRM + 1
                if counterLRM > 4:
                    return True
            if "CAM" in player or "LAM" in player or "RAM" in player:
                counterCAM = counterCAM + 1
                if counterCAM > 3:
                    return True
            if "CF" in player or "LS" in player or "RS" in player:
                counterCF = counterCF + 1
                if counterCF > 3:
                    return True
            if "ST" in player:
                if counterST:
                    return True
                counterST = True
            if "LW" in player or "RW" in player and "LWB" not in player and "RWB" not in player:
                counterLRW = counterLRW + 1
                if counterLRW > 2:
                    return True           
                
        return False        
    
    def accept_button(self):
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
                
        if str(self.team1.currentText()) == str(self.team2.currentText()):#si los dos equipos son el mismo,mostramos un error
            self.errorTeam.showMessage("No puedes elegir el mismo equipo.")
        elif counter != 11:
            self.errorTeam.showMessage("El número de jugadores elegido no es 11.")
        elif self.checkRepeatedPositions() == True:
            self.errorTeam.showMessage("Hay demasiados jugadores en una misma posición, revise de nuevo.")
        else:#si pulsa el boton de aceptar y es correcto, primero tenemos que obtener de la base de datos los jugadores de los dos equipos y tambien las posiciones en las que juegan  
            Estimate.Estimate(self.conexion,str(self.team1.currentText()),str(self.team2.currentText()),self.mainTeam2)#le pasamos el nombre de los dos equipos y el equipo 2(el equipo 1 lo crea Estimate), creamos el nuevo objeto y ya se encarga de llamar a todos los métodos el solo
    
                
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
