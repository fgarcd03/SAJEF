#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Interfaz donde se muestran los resultados
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout,QTextEdit,QRadioButton,QTableWidget,QTableWidgetItem,QHeaderView,QLabel,QHBoxLayout
from PyQt5.QtGui import QIcon 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt 
import numpy as np

SCOREADJUSTMENT = 100000 #usaremos la fórmula (dato/(dato+ScoreAdjustment))*100

class Window(QDialog): 
       
    def __init__(self,mainTeam1,mainTeam2,pointsVSPlayers1,pointsVSPlayers2,pointsOverallMainTeam1,pointsOverallMainTeam2,pointsOverallDefense1,pointsOverallMidfield1,pointsOverallForward1,pointsOverallDefense2,pointsOverallMidfield2,pointsOverallForward2,pointsAttack1,pointsDefense1,pointsAttack2,pointsDefense2,team1,team2,parent=None): 
        super(Window, self).__init__(parent)
        
        self.setWindowTitle("SAJEF-Resultados") 
        self.setWindowIcon(QIcon('../resources/iconmonstr-soccer-1-240.png'))
        self.setMinimumSize(900, 700)
        
        self.mainTeam1 = mainTeam1
        self.mainTeam2 = mainTeam2
        self.pointsVSPlayers1 = pointsVSPlayers1
        self.pointsVSPlayers2 = pointsVSPlayers2
        self.pointsOverallMainTeam1 = pointsOverallMainTeam1
        self.pointsOverallMainTeam2 = pointsOverallMainTeam2
        self.pointsOverallDefense1 = pointsOverallDefense1
        self.pointsOverallMidfield1 = pointsOverallMidfield1
        self.pointsOverallForward1 = pointsOverallForward1
        self.pointsOverallDefense2 = pointsOverallDefense2
        self.pointsOverallMidfield2 = pointsOverallMidfield2
        self.pointsOverallForward2 = pointsOverallForward2
        self.pointsAttack1 = pointsAttack1
        self.pointsDefense1 = pointsDefense1
        self.pointsAttack2 = pointsAttack2
        self.pointsDefense2 = pointsDefense2
        self.team1 = team1
        self.team2 = team2
        pointsZones1,pointsZones2,pointsAttackDefense1,pointsAttackDefense2,totalTeam1,totalTeam2,winTeam1 = self.additionalCalculations()
        
        self.tableTeams = QTableWidget()
        self.tableTeams.setRowCount(2)
        self.tableTeams.setColumnCount(12)
        self.header = self.tableTeams.horizontalHeader()
        self.labelOverall = QLabel("Los dos equipos con sus correspondientes jugadores y puntuaciones totales de cada uno de ellos")
        self.completeGraphic = QRadioButton("Gráfico completo",self)
        self.completeGraphic.setChecked(True)
        self.completeGraphic.clicked.connect(self.completeGraphicConnect)
        self.zoneGraphic = QRadioButton("Gráfico de zonas (defensa, medio, ataque)",self)
        self.zoneGraphic.clicked.connect(self.zoneGraphicConnect)
        self.attackVSdefenseGraphic = QRadioButton("Gráfico de ataque vs. defensa",self)
        self.attackVSdefenseGraphic.clicked.connect(self.attackVSdefenseGraphicConnect)
        self.playerGraphic = QRadioButton("Gráfico de cada jugador",self)
        self.playerGraphic.clicked.connect(self.playerGraphicConnect)
        
        item = QTableWidgetItem(self.team1)
        item.setFlags(item.flags() ^ Qt.ItemIsEditable)
        self.tableTeams.setItem(0,0, QTableWidgetItem(item))
        item = QTableWidgetItem(self.team2)
        item.setFlags(item.flags() ^ Qt.ItemIsEditable)
        self.tableTeams.setItem(1,0, QTableWidgetItem(item))
        self.header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        for column,player in enumerate(self.mainTeam1):
            item = QTableWidgetItem(player)
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.tableTeams.setItem(0,column+1, item)
            self.header.setSectionResizeMode(column+1, QHeaderView.ResizeToContents)
        for column,player in enumerate(self.mainTeam2):
            item = QTableWidgetItem(player) 
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.tableTeams.setItem(1,column+1, item)
            self.header.setSectionResizeMode(column+1, QHeaderView.ResizeToContents)

        
        self.textEdit = QTextEdit("")
        self.textEdit.append("Puntuaciones de equipo como conjunto (30% del total): ")
        self.textEdit.append("    -" + self.team1+" " + str(round(((self.pointsOverallMainTeam1/(self.pointsOverallMainTeam1+SCOREADJUSTMENT))*100)*0.3,2))  +" puntos y " + self.team2 +  " {} puntos.".format(round(((self.pointsOverallMainTeam2/(SCOREADJUSTMENT+self.pointsOverallMainTeam2))*100)*0.3,2)))
        self.textEdit.append("")
        self.textEdit.append("Puntuaciones de cada zona del campo (20% del total): ")
        self.textEdit.append("    -Puntos brutos sin ponderar:")
        self.textEdit.append("        -Zona de defensa: " + self.team1 + " "+ str(round(self.pointsOverallDefense1,2))  +" puntos y " + self.team2 + " {}  puntos.".format(round(self.pointsOverallDefense2,2)))
        self.textEdit.append("        -Zona del centro del campo: " + self.team1 + " "+ str(round(self.pointsOverallMidfield1,2))  +" puntos y " + self.team2 + " {}  puntos.".format(round(self.pointsOverallMidfield2,2)))
        self.textEdit.append("        -Zona delantera: " + self.team1 + " "+ str(round(self.pointsOverallForward1,2))  +" puntos y " + self.team2 + " {}  puntos.".format(round(self.pointsOverallForward2,2)))
        self.textEdit.append("    -Ponderado sobre el 20%")
        self.textEdit.append("        -Puntos totales: " + self.team1 + " " + str(round(((pointsZones1/(pointsZones1+SCOREADJUSTMENT)*100))*0.2,2)) + " puntos y " + self.team2 + " {}  puntos.".format(round(((pointsZones2/(SCOREADJUSTMENT+pointsZones2)*100))*0.2,2)))
        self.textEdit.append("")
        self.textEdit.append("Puntuaciones de ataque y defensa (30% del total):")
        self.textEdit.append("    -Puntos brutos sin ponderar:")
        self.textEdit.append("        -Ataque: " + self.team1 + " "+ str(round(self.pointsAttack1,2)) +" puntos y " + self.team2 + " {} puntos.".format(round(self.pointsAttack2,2)))
        self.textEdit.append("        -Defensa: " + self.team1 + " "+ str(round(self.pointsDefense1,2)) +" puntos y "  + self.team2 + " {} puntos.".format(round(self.pointsDefense2,2)))
        self.textEdit.append("    -Ponderado sobre el 30%:")
        self.textEdit.append("        -Puntos totales: " + self.team1 + " "+ str(round(((pointsAttackDefense1/(pointsAttackDefense1+SCOREADJUSTMENT)*100))*0.3,2)) +" puntos y "  + self.team2 + " {} puntos.".format(round(((pointsAttackDefense2/(SCOREADJUSTMENT+pointsAttackDefense2)*100))*0.3,2)))
        self.textEdit.append("")
        self.textEdit.append("Puntuaciones individuales de cada jugador totales (20% del total):")
        self.textEdit.append("    -" + self.team1+" "+ str(round(((self.pointsVSPlayers1/(self.pointsVSPlayers1+SCOREADJUSTMENT)*100))*0.2,2)) +" puntos y " + self.team2 +  " {} puntos.".format(round(((self.pointsVSPlayers2/(SCOREADJUSTMENT+self.pointsVSPlayers2)*100))*0.2,2)))
        self.textEdit.append("")
        self.textEdit.append("Nota final (100% del total):")
        self.textEdit.append("    -" + self.team1 + " consigue un total de "+ str(round(totalTeam1,2)) + " puntos y " + self.team2 + " consigue un total de " + str(round(totalTeam2,2)) +" puntos.")
        if winTeam1 == True:
            self.textEdit.append("    -Al tener más puntos tiene más posibilidades de ganar el " + self.team1 + ".")
        else:
            self.textEdit.append("    -Al tener más puntos tiene más posibilidades de ganar el " + self.team2 + ".")
        self.textEdit.setReadOnly(True)
        
        self.figure = plt.figure() 
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        self.layoutVertical = QVBoxLayout()
        self.layoutRadioButtonHorizontal = QHBoxLayout()
        self.layoutVertical.addWidget(self.labelOverall)
        self.layoutVertical.addWidget(self.tableTeams,1)
        self.layoutVertical.addWidget(self.textEdit,2)
        self.layoutVertical.addWidget(self.canvas,2)
        self.layoutVertical.addWidget(self.toolbar)

        self.layoutRadioButtonHorizontal.addWidget(self.completeGraphic)
        self.layoutRadioButtonHorizontal.addWidget(self.zoneGraphic)
        self.layoutRadioButtonHorizontal.addWidget(self.attackVSdefenseGraphic)
        self.layoutRadioButtonHorizontal.addWidget(self.playerGraphic)

        self.layoutVertical.addLayout(self.layoutRadioButtonHorizontal)
        self.setLayout(self.layoutVertical) 
        
        self.completeGraphicConnect() #Dibujamos un gráfico por defecto
        
    def completeGraphicConnect(self):
        self.canvas.figure.clear() #elimina el dibujo anterior para que pueda ser dibujado otro gráfico
        self.plotOverall()

    def zoneGraphicConnect(self):
        self.canvas.figure.clear()
        self.plotZones()
        
    def attackVSdefenseGraphicConnect(self):    
        self.canvas.figure.clear()
        self.plotAttackVSDefense()
        
    def playerGraphicConnect(self):
        self.canvas.figure.clear()
        self.plotPlayers()
    
    def plotOverall(self):#dibujamos el primer gráfico
        pointsZones1,pointsZones2,pointsAttackDefense1,pointsAttackDefense2,totalTeam1,totalTeam2,winTeam1 = self.additionalCalculations()
        
        bars1 = [((self.pointsOverallMainTeam1/(self.pointsOverallMainTeam1+SCOREADJUSTMENT))*100)*0.3,((self.pointsOverallMainTeam2/(SCOREADJUSTMENT+self.pointsOverallMainTeam2))*100)*0.3] #se calcula sobre 100 la puntuación para que no salgan números muy grandes y se multiplica por la ponderancia de cada división
        bars2 = [((pointsZones1/(pointsZones1+SCOREADJUSTMENT)*100))*0.2,((pointsZones2/(SCOREADJUSTMENT+pointsZones2)*100))*0.2]
        bars3 = [((pointsAttackDefense1/(pointsAttackDefense1+SCOREADJUSTMENT)*100))*0.3,((pointsAttackDefense2/(SCOREADJUSTMENT+pointsAttackDefense2)*100))*0.3]
        bars4 = [((self.pointsVSPlayers1/(self.pointsVSPlayers1+SCOREADJUSTMENT)*100))*0.2,((self.pointsVSPlayers2/(SCOREADJUSTMENT+self.pointsVSPlayers2)*100))*0.2]
         
        p1 = plt.bar([0,1], bars1, color='r', edgecolor='white', width=0.3)
        p2 = plt.bar([0,1], bars2, bottom=bars1, color='g', edgecolor='white', width=0.3)
        p3 = plt.bar([0,1], bars3, bottom=np.array(bars1)+np.array(bars2), color='b', edgecolor='white', width=0.3)
        p4 = plt.bar([0,1], bars4, bottom=np.array(bars1)+np.array(bars2)+np.array(bars3), color='y', edgecolor='white', width=0.3)
        
        
        plt.legend((p1[0], p2[0],p3[0],p4[0]), ("Puntos de equipo como conjunto", "Puntos de cada zona del campo","Puntos de ataque y defensa","Puntos individuales de cada jugador totales"),loc="upper center") 

        plt.xticks([0,1], [self.team1,self.team2], fontweight='bold')
        plt.ylabel('Puntuación')
        
        self.canvas.draw() 

    def plotZones(self):#dibujamos el segundo gráfico
        bars1 = [(self.pointsOverallDefense1/(self.pointsOverallDefense1+SCOREADJUSTMENT))*100,(self.pointsOverallDefense2/(SCOREADJUSTMENT+self.pointsOverallDefense2))*100] #se calcula sobre 100 la puntuación para que no salgan números muy grandes, en este caso no se multiplica por la ponderancia ya que solo vemos los de un apartado
        bars2 = [(self.pointsOverallMidfield1/(self.pointsOverallMidfield1+SCOREADJUSTMENT))*100,(self.pointsOverallMidfield2/(SCOREADJUSTMENT+self.pointsOverallMidfield2))*100]
        bars3 = [(self.pointsOverallForward1/(self.pointsOverallForward1+SCOREADJUSTMENT))*100,(self.pointsOverallForward2/(SCOREADJUSTMENT+self.pointsOverallForward2))*100]
        
        p1 = plt.bar([0,1], bars1, color='r', edgecolor='white', width=0.3)
        p2 = plt.bar([0,1], bars2, bottom=bars1, color='g', edgecolor='white', width=0.3)
        p3 = plt.bar([0,1], bars3, bottom=np.array(bars1)+np.array(bars2), color='b', edgecolor='white', width=0.3)
        
        plt.legend((p1[0], p2[0],p3[0]), ("Puntos de la zona de defensa", "Puntos de la zona del centro de campo","Puntos de la zona de ataque"),loc="upper center") 

        plt.xticks([0,1], [self.team1,self.team2], fontweight='bold')
        plt.ylabel('Puntuación')
        
        self.canvas.draw()
        
    def plotAttackVSDefense(self):#dibujamos el tercer gráfico
        bars1 = [(self.pointsDefense1/(self.pointsDefense1+SCOREADJUSTMENT))*100,(self.pointsDefense2/(SCOREADJUSTMENT+self.pointsDefense2))*100] #se calcula sobre 100 la puntuación para que no salgan números muy grandes, en este caso no se multiplica por la ponderancia ya que solo vemos los de un apartado
        bars2 = [(self.pointsAttack1/(self.pointsAttack1+SCOREADJUSTMENT))*100,(self.pointsAttack2/(SCOREADJUSTMENT+self.pointsAttack2))*100]
        
        p1 = plt.bar([0,1], bars1, color='r', edgecolor='white', width=0.3)
        p2 = plt.bar([0,1], bars2, bottom=bars1, color='g', edgecolor='white', width=0.3)
        
        plt.legend((p1[0], p2[0]), ("Puntos de defensa", "Puntos de ataque"),loc="upper center") 

        plt.xticks([0,1], [self.team1,self.team2], fontweight='bold')
        plt.ylabel('Puntuación')
        
        self.canvas.draw()
        
    def plotPlayers(self):#dibujamos el cuarto gráfico
        team1 = []
        team2 = []
        labels = []
        
        for player1 in self.mainTeam1:
            for player2 in self.mainTeam2:
                if "-" in player1.split(",")[1]:
                    position1 = player1.split(",")[1].split("-")[1]
                else:
                    position1 = player1.split(",")[1].replace(" ","")
                if "-" in player2.split(",")[1]:
                    position2 = player2.split(",")[1].split("-")[1]
                else:
                    position2 = player2.split(",")[1].replace(" ","")
                    
                if position1 == position2:
                    team1.append(int(player1.split(",")[2]))
                    team2.append(int(player2.split(",")[2]))
                    labels.append(position1)
        
        width = 0.2
        p1 = plt.bar(np.arange(len(labels)) + width/2, team1, color = 'b', width = 0.2)
        p2 = plt.bar(np.arange(len(labels)) - width/2, team2, color = 'g', width = 0.2)

        plt.legend((p1[0], p2[0]), (self.team1, self.team2),loc="upper center") 

        plt.xticks(np.arange(len(labels)), labels, fontweight='bold')
        plt.ylabel('Puntuación')

        self.canvas.draw()
        
    def additionalCalculations(self):
        winTeam1 = False
        
        pointsZones1 = self.pointsOverallDefense1 + self.pointsOverallMidfield1 + self.pointsOverallForward1
        pointsZones2 = self.pointsOverallDefense2 + self.pointsOverallMidfield2 + self.pointsOverallForward2
        
        pointsAttackDefense1 = self.pointsDefense1 - self.pointsAttack2
        pointsAttackDefense2 = self.pointsDefense2 - self.pointsAttack1
        
        if pointsAttackDefense1 < 0:
            pointsAttackDefense1 = 0
            
        if pointsAttackDefense2 < 0:
            pointsAttackDefense2 = 0
        
        totalTeam1 = (((self.pointsOverallMainTeam1/(self.pointsOverallMainTeam1+SCOREADJUSTMENT))*100)*0.3) + (((pointsZones1/(pointsZones1+SCOREADJUSTMENT)*100))*0.2) + (((pointsAttackDefense1/(pointsAttackDefense1+SCOREADJUSTMENT)*100))*0.3) + (((self.pointsVSPlayers1/(self.pointsVSPlayers1+SCOREADJUSTMENT)*100))*0.2)
        totalTeam2 = (((self.pointsOverallMainTeam2/(SCOREADJUSTMENT+self.pointsOverallMainTeam2))*100)*0.3) + (((pointsZones2/(SCOREADJUSTMENT+pointsZones2)*100))*0.2) + (((pointsAttackDefense2/(SCOREADJUSTMENT+pointsAttackDefense2)*100))*0.3) + (((self.pointsVSPlayers2/(SCOREADJUSTMENT+self.pointsVSPlayers2)*100))*0.2)
        
        if totalTeam1 > totalTeam2:
            winTeam1 = True
       
        return pointsZones1,pointsZones2,pointsAttackDefense1,pointsAttackDefense2,totalTeam1,totalTeam2,winTeam1

 
if __name__ == '__main__':
    with open("settings.conf") as fp:
        for i, line in enumerate(fp):     
            if i == 0:
                mainTeam1 = line.split(";")
                mainTeam1.pop()#Quitamos el salto de línea
            elif i == 1:
                mainTeam2 = line.split(";")
                mainTeam2.pop()
            elif i == 2:
                pointsVSPlayers1 = int(line) 
            elif i == 3:
                pointsVSPlayers2 = int(line)
            elif i == 4:
                pointsOverallMainTeam1 = float(line)
            elif i == 5:
                pointsOverallMainTeam2 = float(line)
            elif i == 6:
                pointsOverallDefense1 = float(line)
            elif i == 7:
                pointsOverallDefense2 = float(line)
            elif i == 8:
                pointsOverallMidfield1 = float(line)
            elif i == 9:
                pointsOverallMidfield2 = float(line)
            elif i == 10:
                pointsOverallForward1 = float(line)
            elif i == 11:
                pointsOverallForward2 = float(line)
            elif i == 12:
                pointsAttack1 = float(line)
            elif i == 13:
                pointsAttack2 = float(line)
            elif i == 14:
                pointsDefense1 = float(line)
            elif i == 15:
                pointsDefense2 = float(line)
            elif i == 16:
                team1 = line
                team1 = team1[0:-1]
            elif i == 17:
                team2 = line
                team2 = team2[0:-1]
      
    #Ventana
    app = QApplication(sys.argv) 
    mainWindow = Window(mainTeam1,mainTeam2,pointsVSPlayers1,pointsVSPlayers2,pointsOverallMainTeam1,pointsOverallMainTeam2,pointsOverallDefense1,pointsOverallMidfield1,pointsOverallForward1,pointsOverallDefense2,pointsOverallMidfield2,pointsOverallForward2,pointsAttack1,pointsDefense1,pointsAttack2,pointsDefense2,team1,team2)
    mainWindow.show() 
    sys.exit(app.exec_()) 
  
