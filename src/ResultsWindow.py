#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys 
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout,QLineEdit,QLabel,QTextEdit,QPushButton,QRadioButton
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
        #self.showMaximized()
        
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
        
        self.completeGraphic = QRadioButton("Gráfico completo",self)
        self.completeGraphic.setChecked(True)
        self.completeGraphic.clicked.connect(self.completeGraphicConnect)
        self.zoneGraphic = QRadioButton("Gráfico de zonas(defensa,medio,ataque)",self)
        self.zoneGraphic.clicked.connect(self.zoneGraphicConnect)
        
        self.textEdit = QTextEdit("Datos recogidos de los dos equipos.") #hay inconsistencias en la creación de textos, hace lo que le da la gana
        self.textEdit.append("Primer equipo: {}, segundo equipo: {}.".format(self.team1, self.team2))
        self.textEdit.append("Puntuaciones de equipo como conjunto (30% de la nota):")
        self.textEdit.append("    -" + self.team1+":{} puntos y " + self.team2 +  ":{} puntos. ".format(round(((self.pointsOverallMainTeam1/(self.pointsOverallMainTeam1+self.pointsOverallMainTeam2))*100)*0.3,2),round(((self.pointsOverallMainTeam2/(self.pointsOverallMainTeam1+pointsOverallMainTeam2))*100)*0.3,2)))
        self.textEdit.append("Puntuaciones de cada zona del campo(20% de la nota):")
        self.textEdit.append("Puntuaciones de ataque y defensa(30% de la nota):")
        self.textEdit.append("    -Ataque (puntos brutos sin ponderar):" + self.team1 + ":{} puntos y " + self.team2 + ": {} puntos.".format(round(self.pointsAttack1,2),round(self.pointsAttack2,2)))
        self.textEdit.append("    -Defensa (puntos brutos sin ponderar):" + self.team1 + ":{} puntos y "  + self.team2 + ": {} puntos ".format(round(self.pointsDefense1,2),round(self.pointsDefense2)))
        self.textEdit.append("    -Que en total de ataque y defensa dan(ponderado):" + self.team1 + ":{} puntos y "  + self.team2 + ": {} puntos.")
        self.textEdit.append("Puntuaciones individuales de cada jugador totales (20% de la nota):")
        self.textEdit.append("    -" + self.team1+":{} puntos y " + self.team2 +  ":{} puntos.".format(round(((self.pointsVSPlayers1/(self.pointsVSPlayers1+self.pointsVSPlayers2)*100))*0.2,2),round(((self.pointsVSPlayers2/(self.pointsVSPlayers1+self.pointsVSPlayers2)*100))*0.2),2))
        self.textEdit.append("Nota total:")
        self.textEdit.append("    -" + self.team1 + " consigue un total de puntos de {} y tiene una probabilidad de ganar de:{}% y " + self.team2 + "consigue un total de puntos y tiene una probabilidad de: {}%")
        
        self.textEdit.setReadOnly(True)
        
        
        self.figure = plt.figure() 
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.textEdit)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.toolbar)

        self.layout.addWidget(self.completeGraphic)
        self.layout.addWidget(self.zoneGraphic)

        self.setLayout(self.layout) 
        
        self.completeGraphicConnect() #Dibujamos un gráfico por defecto
        
    def completeGraphicConnect(self):
        self.canvas.figure.clear() #elimia el dibujo anterior para que pueda ser dibujado otro grafico
        self.plotOverall(self.team1,self.team2,self.pointsVSPlayers1,self.pointsVSPlayers2,self.pointsOverallMainTeam1,self.pointsOverallMainTeam2,self.pointsOverallDefense1,self.pointsOverallMidfield1,self.pointsOverallForward1,self.pointsOverallDefense2,self.pointsOverallMidfield2,self.pointsOverallForward2,self.pointsAttack1,self.pointsDefense1,self.pointsAttack2,self.pointsDefense2)

    def zoneGraphicConnect(self):
        self.canvas.figure.clear()
        self.plotZones(self.team1,self.team2,self.pointsOverallDefense1,self.pointsOverallMidfield1,self.pointsOverallForward1,self.pointsOverallDefense2,self.pointsOverallMidfield2,self.pointsOverallForward2)

        
    def plotOverall(self,team1,team2,pointsVSPlayers1,pointsVSPlayers2,pointsOverallMainTeam1,pointsOverallMainTeam2,pointsOverallDefense1,pointsOverallMidfield1,pointsOverallForward1,pointsOverallDefense2,pointsOverallMidfield2,pointsOverallForward2,pointsAttack1,pointsDefense1,pointsAttack2,pointsDefense2): 
        
        pointsZones1 = (float(pointsOverallDefense1[-1]) + float(pointsOverallMidfield1[-1]) + float(pointsOverallForward1[-1]))
        pointsZones2 = (float(pointsOverallDefense2[-1]) + float(pointsOverallMidfield2[-1])+ float(pointsOverallForward2[-1]))
        
        pointsAttackDefense1 = pointsAttack1 + pointsDefense1
        pointsAttackDefense2 = pointsAttack2 + pointsDefense2
        
        # Values of each group
        bars1 = [((pointsOverallMainTeam1/(pointsOverallMainTeam1+pointsOverallMainTeam2))*100)*0.3,((pointsOverallMainTeam2/(pointsOverallMainTeam1+pointsOverallMainTeam2))*100)*0.3] #se calcula sobre 100 la puntuación para que no salgan números muy grandes y se multiplica por la ponderancia de cada división
        bars2 = [((pointsZones1/(pointsZones1+pointsZones2)*100))*0.2,((pointsZones2/(pointsZones1+pointsZones2)*100))*0.2]
        bars3 = [((pointsAttackDefense1/(pointsAttackDefense1+pointsAttackDefense2)*100))*0.3,((pointsAttackDefense2/(pointsAttackDefense1+pointsAttackDefense2)*100))*0.3]
        bars4 = [((pointsVSPlayers1/(pointsVSPlayers1+pointsVSPlayers2)*100))*0.2,((pointsVSPlayers2/(pointsVSPlayers1+pointsVSPlayers2)*100))*0.2]
         
        # Create bars
        p1 = plt.bar([0,1], bars1, color='r', edgecolor='white', width=0.3)
        p2 = plt.bar([0,1], bars2, bottom=bars1, color='g', edgecolor='white', width=0.3)
        p3 = plt.bar([0,1], bars3, bottom=np.array(bars1)+np.array(bars2), color='b', edgecolor='white', width=0.3)
        p4 = plt.bar([0,1], bars4, bottom=np.array(bars1)+np.array(bars2)+np.array(bars3), color='y', edgecolor='white', width=0.3)
        
        
        #Añadir bbox_to_anchor=(0.5, 1.15), ncol=2 al final de legend para que salga fuera del gráfico
        plt.legend((p1[0], p2[0],p3[0],p4[0]), ("Puntos de equipo como conjunto", "Puntos de cada zona del campo(defensa,medio,centro)","Puntos de ataque y defensa","Puntos individuales de cada jugador totales"),loc="upper center") 

        plt.xticks([0,1], [team1,team2], fontweight='bold')
        plt.ylabel('Puntuación')
        
        self.canvas.draw() 

    def plotZones(self,team1,team2,pointsOverallDefense1,pointsOverallMidfield1,pointsOverallForward1,pointsOverallDefense2,pointsOverallMidfield2,pointsOverallForward2):
    
        bars1 = [(float(pointsOverallDefense1[-1])/(float(pointsOverallDefense1[-1])+float(pointsOverallDefense2[-1])))*100,(float(pointsOverallDefense2[-1])/(float(pointsOverallDefense1[-1])+float(pointsOverallDefense2[-1])))*100] #se calcula sobre 100 la puntuación para que no salgan números muy grandes, en este caso no se multiplica por la ponderancia ya que solo vemos los de una  apartado
        bars2 = [(float(pointsOverallMidfield1[-1])/(float(pointsOverallMidfield1[-1])+float(pointsOverallMidfield2[-1])))*100,(float(pointsOverallMidfield2[-1])/(float(pointsOverallMidfield1[-1])+float(pointsOverallMidfield2[-1])))*100]
        bars3 = [(float(pointsOverallForward1[-1])/(float(pointsOverallForward1[-1])+float(pointsOverallForward2[-1])))*100,(float(pointsOverallForward2[-1])/(float(pointsOverallForward1[-1])+float(pointsOverallForward2[-1])))*100]
        
        p1 = plt.bar([0,1], bars1, color='r', edgecolor='white', width=0.3)
        p2 = plt.bar([0,1], bars2, bottom=bars1, color='g', edgecolor='white', width=0.3)
        p3 = plt.bar([0,1], bars3, bottom=np.array(bars1)+np.array(bars2), color='b', edgecolor='white', width=0.3)
        
        plt.legend((p1[0], p2[0],p3[0]), ("Puntos de la zona de defensa", "Puntos de la zona del centro de campo","Puntos de la zona de ataque"),loc="upper center") 

        plt.xticks([0,1], [team1,team2], fontweight='bold')
        plt.ylabel('Puntuación')
        
        self.canvas.draw()
        
    def plotPlayers(self,team1,team2,mainTeam1,mainTeam2):
        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        langs = ['C', 'C++', 'Java', 'Python', 'PHP']
        students = [23,17,35,29,12]
        ax.bar(langs,students)
        self.canvas.draw()

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
  