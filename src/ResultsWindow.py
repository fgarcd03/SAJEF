#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys 
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout,QTextEdit,QRadioButton
from PyQt5.QtGui import QIcon 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt 
import numpy as np

class Window(QDialog): 
       
    def __init__(self,mainTeam1,mainTeam2,pointsVSPlayers1,pointsVSPlayers2,pointsOverallMainTeam1,pointsOverallMainTeam2,pointsOverallDefense1,pointsOverallMidfield1,pointsOverallForward1,pointsOverallDefense2,pointsOverallMidfield2,pointsOverallForward2,pointsAttack1,pointsDefense1,pointsAttack2,pointsDefense2,team1,team2,parent=None): 
        super(Window, self).__init__(parent)
        
        self.setWindowTitle("SAJEF-Resultados") 
        self.setWindowIcon(QIcon('../resources/iconmonstr-soccer-1-240.png'))
        self.setMinimumSize(1000, 650)
        
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
        
        self.completeGraphic = QRadioButton("Gráfico completo",self)
        self.completeGraphic.setChecked(True)
        self.completeGraphic.clicked.connect(self.completeGraphicConnect)
        self.zoneGraphic = QRadioButton("Gráfico de zonas (defensa,medio,ataque)",self)
        self.zoneGraphic.clicked.connect(self.zoneGraphicConnect)
        self.playerGraphic = QRadioButton("Gráfico de cada jugador",self)
        self.playerGraphic.clicked.connect(self.playerGraphicConnect)
        
        self.textEdit = QTextEdit("·Datos recogidos de los dos equipos.")
        self.textEdit.append("·Primer equipo (jugador,posición,puntos individuales): " + self.team1 + " " + str(self.mainTeam1)) 
        self.textEdit.append("·Segundo equipo (jugador,posición,puntos individuales): " + self.team2 + " " + str(self.mainTeam2))
        self.textEdit.append("")
        self.textEdit.append("·Puntuaciones de equipo como conjunto (30% del total):")
        self.textEdit.append("    -" + self.team1+":" + str(round(((self.pointsOverallMainTeam1/(self.pointsOverallMainTeam1+self.pointsOverallMainTeam2))*100)*0.3,2))  +" puntos y " + self.team2 +  ":{} puntos.".format(round(((self.pointsOverallMainTeam2/(self.pointsOverallMainTeam1+self.pointsOverallMainTeam2))*100)*0.3,2)))
        self.textEdit.append("")
        self.textEdit.append("·Puntuaciones de cada zona del campo (20% del total):")
        self.textEdit.append("    -Zona de defensa (puntos brutos sin ponderar): " + self.team1 + ":"+ str(round(float(self.pointsOverallDefense1[-1]),2))  +" puntos y " + self.team2 + ":{}  puntos.".format(round(float(self.pointsOverallDefense2[-1]),2)))
        self.textEdit.append("    -Zona del centro del campo (puntos brutos sin ponderar): " + self.team1 + ":"+ str(round(float(self.pointsOverallMidfield1[-1]),2))  +" puntos y " + self.team2 + ":{}  puntos.".format(round(float(self.pointsOverallMidfield2[-1]),2)))
        self.textEdit.append("    -Zona delantera (puntos brutos sin ponderar): " + self.team1 + ":"+ str(round(float(self.pointsOverallForward1[-1]),2))  +" puntos y " + self.team2 + ":{}  puntos.".format(round(float(self.pointsOverallForward2[-1]),2)))
        self.textEdit.append("    -Con un total de puntos de (ponderado sobre el 20%): " + self.team1 + ":" + str(round(((pointsZones1/(pointsZones1+pointsZones2)*100))*0.2,2)) +"puntos y " + self.team2 + ":{}  puntos.".format(round(((pointsZones2/(pointsZones1+pointsZones2)*100))*0.2,2)))
        self.textEdit.append("")
        self.textEdit.append("·Puntuaciones de ataque y defensa (30% del total):" )
        self.textEdit.append("    -Ataque (puntos brutos sin ponderar):" + self.team1 + ":"+ str(round(self.pointsAttack1,2)) +" puntos y " + self.team2 + ": {} puntos.".format(round(self.pointsAttack2,2)))
        self.textEdit.append("    -Defensa (puntos brutos sin ponderar):" + self.team1 + ":"+ str(round(self.pointsDefense1,2)) +" puntos y "  + self.team2 + ": {} puntos.".format(round(self.pointsDefense2,2)))
        self.textEdit.append("    -Que en total de ataque y defensa dan (ponderado sobre el 30%):" + self.team1 + ":"+ str(round(((pointsAttackDefense1/(pointsAttackDefense1+pointsAttackDefense2)*100))*0.3,2)) +" puntos y "  + self.team2 + ": {} puntos.".format(round(((pointsAttackDefense2/(pointsAttackDefense1+pointsAttackDefense2)*100))*0.3,2)))
        self.textEdit.append("")
        self.textEdit.append("·Puntuaciones individuales de cada jugador totales (20% del total):")
        self.textEdit.append("    -" + self.team1+":"+ str(round(((self.pointsVSPlayers1/(self.pointsVSPlayers1+self.pointsVSPlayers2)*100))*0.2,2)) +" puntos y " + self.team2 +  ":{} puntos.".format(round(((self.pointsVSPlayers2/(self.pointsVSPlayers1+self.pointsVSPlayers2)*100))*0.2,2)))
        self.textEdit.append("")
        self.textEdit.append("·Nota total (100% del total):")
        self.textEdit.append("    -" + self.team1 + " consigue un total de puntos de: "+ str(round(totalTeam1,2)) + " y " + self.team2 + " consigue un total de puntos de: " + str(round(totalTeam2,2)) +".")
        if winTeam1 == True:
            self.textEdit.append("    -Por lo tanto al tener mas puntos tiene mas posibilidad de ganas el : " + self.team1 + ".")
        else:
            self.textEdit.append("    -Por lo tanto al tener mas puntos tiene mas posibilidad de ganas el : " + self.team2 + ".")
        self.textEdit.setReadOnly(True)
        
        
        self.figure = plt.figure() 
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.textEdit,3)
        self.layout.addWidget(self.canvas,2)
        self.layout.addWidget(self.toolbar)

        self.layout.addWidget(self.completeGraphic)
        self.layout.addWidget(self.zoneGraphic)
        self.layout.addWidget(self.playerGraphic)

        self.setLayout(self.layout) 
        
        self.completeGraphicConnect() #Dibujamos un gráfico por defecto
        
    def completeGraphicConnect(self):
        self.canvas.figure.clear() #elimia el dibujo anterior para que pueda ser dibujado otro grafico
        self.plotOverall()

    def zoneGraphicConnect(self):
        self.canvas.figure.clear()
        self.plotZones()
    
    def playerGraphicConnect(self):
        self.canvas.figure.clear()
        self.plotPlayers()
        
    def plotOverall(self): 
        pointsZones1,pointsZones2,pointsAttackDefense1,pointsAttackDefense2,totalTeam1,totalTeam2,winTeam1 = self.additionalCalculations()
        
        # Values of each group
        bars1 = [((self.pointsOverallMainTeam1/(self.pointsOverallMainTeam1+self.pointsOverallMainTeam2))*100)*0.3,((self.pointsOverallMainTeam2/(self.pointsOverallMainTeam1+self.pointsOverallMainTeam2))*100)*0.3] #se calcula sobre 100 la puntuación para que no salgan números muy grandes y se multiplica por la ponderancia de cada división
        bars2 = [((pointsZones1/(pointsZones1+pointsZones2)*100))*0.2,((pointsZones2/(pointsZones1+pointsZones2)*100))*0.2]
        bars3 = [((pointsAttackDefense1/(pointsAttackDefense1+pointsAttackDefense2)*100))*0.3,((pointsAttackDefense2/(pointsAttackDefense1+pointsAttackDefense2)*100))*0.3]
        bars4 = [((self.pointsVSPlayers1/(self.pointsVSPlayers1+self.pointsVSPlayers2)*100))*0.2,((self.pointsVSPlayers2/(self.pointsVSPlayers1+self.pointsVSPlayers2)*100))*0.2]
         
        # Create bars
        p1 = plt.bar([0,1], bars1, color='r', edgecolor='white', width=0.3)
        p2 = plt.bar([0,1], bars2, bottom=bars1, color='g', edgecolor='white', width=0.3)
        p3 = plt.bar([0,1], bars3, bottom=np.array(bars1)+np.array(bars2), color='b', edgecolor='white', width=0.3)
        p4 = plt.bar([0,1], bars4, bottom=np.array(bars1)+np.array(bars2)+np.array(bars3), color='y', edgecolor='white', width=0.3)
        
        
        #Añadir bbox_to_anchor=(0.5, 1.15), ncol=2 al final de legend para que salga fuera del gráfico
        plt.legend((p1[0], p2[0],p3[0],p4[0]), ("Puntos de equipo como conjunto", "Puntos de cada zona del campo","Puntos de ataque y defensa","Puntos individuales de cada jugador totales"),loc="upper center") 

        plt.xticks([0,1], [self.team1,self.team2], fontweight='bold')
        plt.ylabel('Puntuación')
        
        self.canvas.draw() 

    def plotZones(self):
    
        bars1 = [(float(self.pointsOverallDefense1[-1])/(float(self.pointsOverallDefense1[-1])+float(self.pointsOverallDefense2[-1])))*100,(float(self.pointsOverallDefense2[-1])/(float(self.pointsOverallDefense1[-1])+float(self.pointsOverallDefense2[-1])))*100] #se calcula sobre 100 la puntuación para que no salgan números muy grandes, en este caso no se multiplica por la ponderancia ya que solo vemos los de una  apartado
        bars2 = [(float(self.pointsOverallMidfield1[-1])/(float(self.pointsOverallMidfield1[-1])+float(self.pointsOverallMidfield2[-1])))*100,(float(self.pointsOverallMidfield2[-1])/(float(self.pointsOverallMidfield1[-1])+float(self.pointsOverallMidfield2[-1])))*100]
        bars3 = [(float(self.pointsOverallForward1[-1])/(float(self.pointsOverallForward1[-1])+float(self.pointsOverallForward2[-1])))*100,(float(self.pointsOverallForward2[-1])/(float(self.pointsOverallForward1[-1])+float(self.pointsOverallForward2[-1])))*100]
        
        p1 = plt.bar([0,1], bars1, color='r', edgecolor='white', width=0.3)
        p2 = plt.bar([0,1], bars2, bottom=bars1, color='g', edgecolor='white', width=0.3)
        p3 = plt.bar([0,1], bars3, bottom=np.array(bars1)+np.array(bars2), color='b', edgecolor='white', width=0.3)
        
        plt.legend((p1[0], p2[0],p3[0]), ("Puntos de la zona de defensa", "Puntos de la zona del centro de campo","Puntos de la zona de ataque"),loc="upper center") 

        plt.xticks([0,1], [self.team1,self.team2], fontweight='bold')
        plt.ylabel('Puntuación')
        
        self.canvas.draw()
        
    def plotPlayers(self):
        team1 = []
        team2 = []
        labels = []
        
        for player1 in self.mainTeam1:
            for player2 in self.mainTeam2:
                if player1.split(",")[1] == player2.split(",")[1]:#si coincide las posiciones las guardamos y sus puntuaciones
                    team1.append(int(player1.split(",")[2]))
                    team2.append(int(player2.split(",")[2]))
                    labels.append(player1.split(",")[1])
        
        
        width = 0.2
        p1 = plt.bar(np.arange(len(labels)) + width/2, team1, color = 'b', width = width)
        p2 = plt.bar(np.arange(len(labels)) - width/2, team2, color = 'g', width = width)

        plt.legend((p1[0], p2[0]), (self.team1, self.team2),loc="upper center") 

        plt.xticks(np.arange(len(labels)), labels, fontweight='bold')
        plt.ylabel('Puntuación')


        self.canvas.draw()
        
    def additionalCalculations(self):
        winTeam1 = False
        
        pointsZones1 = (float(self.pointsOverallDefense1[-1]) + float(self.pointsOverallMidfield1[-1]) + float(self.pointsOverallForward1[-1]))
        pointsZones2 = (float(self.pointsOverallDefense2[-1]) + float(self.pointsOverallMidfield2[-1])+ float(self.pointsOverallForward2[-1]))
        
        pointsAttackDefense1 = self.pointsAttack1 + self.pointsDefense1
        pointsAttackDefense2 = self.pointsAttack2 + self.pointsDefense2
        

        totalTeam1 = (((self.pointsOverallMainTeam1/(self.pointsOverallMainTeam1+self.pointsOverallMainTeam2))*100)*0.3) + (((pointsZones1/(pointsZones1+pointsZones2)*100))*0.2) + (((pointsAttackDefense1/(pointsAttackDefense1+pointsAttackDefense2)*100))*0.3) + (((self.pointsVSPlayers1/(self.pointsVSPlayers1+self.pointsVSPlayers2)*100))*0.2)
        totalTeam2 = (((self.pointsOverallMainTeam2/(self.pointsOverallMainTeam1+self.pointsOverallMainTeam2))*100)*0.3) + (((pointsZones2/(pointsZones1+pointsZones2)*100))*0.2) + (((pointsAttackDefense2/(pointsAttackDefense1+pointsAttackDefense2)*100))*0.3) + (((self.pointsVSPlayers2/(self.pointsVSPlayers1+self.pointsVSPlayers2)*100))*0.2)
        
        if totalTeam1 > totalTeam2:
            winTeam1 = True
       
        return pointsZones1,pointsZones2,pointsAttackDefense1,pointsAttackDefense2,totalTeam1,totalTeam2,winTeam1
    
if __name__ == '__main__':

    with open("settings.txt") as fp:
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
                pointsOverallMainTeam1 = int(line)
            elif i == 5:
                pointsOverallMainTeam2 = int(line)
            elif i == 6:
                pointsOverallDefense1 = line.split(";")
                pointsOverallDefense1.pop()
            elif i == 7:
                pointsOverallMidfield1 = line.split(";")
                pointsOverallMidfield1.pop()
            elif i == 8:
                pointsOverallForward1 = line.split(";")
                pointsOverallForward1.pop()
            elif i == 9:
                pointsOverallDefense2 = line.split(";")
                pointsOverallDefense2.pop()
            elif i == 10:
                pointsOverallMidfield2 = line.split(";")
                pointsOverallMidfield2.pop()
            elif i == 11:
                pointsOverallForward2 = line.split(";")
                pointsOverallForward2.pop()
            elif i == 12:
                pointsAttack1 = float(line)
            elif i == 13:
                pointsDefense1 = float(line)
            elif i == 14:
                pointsAttack2 = float(line)
            elif i == 15:
                pointsDefense2 = float(line)
            elif i == 16:
                team1 = line
                team1 = team1[0:-1]
            elif i == 17:
                team2 = line
                team2 = team2[0:-1]
      
    # creating apyqt5 application 
    app = QApplication(sys.argv) 
    # creating a window object 
    main = Window(mainTeam1,mainTeam2,pointsVSPlayers1,pointsVSPlayers2,pointsOverallMainTeam1,pointsOverallMainTeam2,pointsOverallDefense1,pointsOverallMidfield1,pointsOverallForward1,pointsOverallDefense2,pointsOverallMidfield2,pointsOverallForward2,pointsAttack1,pointsDefense1,pointsAttack2,pointsDefense2,team1,team2) 
       
    # showing the window 
    main.show() 
   
    # loop 
    sys.exit(app.exec_()) 
  