#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys 
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout
from PyQt5.QtGui import QIcon 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt 
import numpy as np

class Window(QDialog): 
       
    # constructor 
    def __init__(self,mainTeam1,mainTeam2,pointsVSPlayers1,pointsVSPlayers2,pointsOverallMainTeam1,pointsOverallMainTeam2,pointsOverallDefense1,pointsOverallMidfield1,pointsOverallForward1,pointsOverallDefense2,pointsOverallMidfield2,pointsOverallForward2,pointsAttack1,pointsDefense1,pointsAttack2,pointsDefense2,team1,team2,parent=None): 
        super(Window, self).__init__(parent)
        
        self.setWindowTitle("SAJEF-Resultados") 
        self.setWindowIcon(QIcon('../resources/iconmonstr-soccer-1-240.png'))
        
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
        
        # a figure instance to plot on 
        self.figure = plt.figure() 

        # this is the Canvas Widget that  
        # displays the 'figure'it takes the 
        # 'figure' instance as a parameter to __init__ 
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        #self.figure2 = plt.figure() 
        #self.canvas2 = FigureCanvas(self.figure2)
        
        #ploteamos el grafico
        self.plot(self.team1,self.team2,self.pointsVSPlayers1,self.pointsVSPlayers2,self.pointsOverallMainTeam1,self.pointsOverallMainTeam2,self.pointsOverallDefense1,self.pointsOverallMidfield1,self.pointsOverallForward1,self.pointsOverallDefense2,self.pointsOverallMidfield2,self.pointsOverallForward2,self.pointsAttack1,self.pointsDefense1,self.pointsAttack2,self.pointsDefense2)
        #self.plot2()
        # creating a Vertical Box layout 
        layout = QVBoxLayout() 
 
        # adding canvas to the layout 
        layout.addWidget(self.canvas)
        #layout.addWidget(self.canvas2)
        layout.addWidget(self.toolbar)
 
        # setting layout to the main window 
        self.setLayout(layout) 
   
    
    def plot(self,team1,team2,pointsVSPlayers1,pointsVSPlayers2,pointsOverallMainTeam1,pointsOverallMainTeam2,pointsOverallDefense1,pointsOverallMidfield1,pointsOverallForward1,pointsOverallDefense2,pointsOverallMidfield2,pointsOverallForward2,pointsAttack1,pointsDefense1,pointsAttack2,pointsDefense2): 
        
        pointsZones1 = (float(pointsOverallDefense1[-1]) + float(pointsOverallMidfield1[-1]) + float(pointsOverallForward1[-1]))
        pointsZones2 = (float(pointsOverallDefense2[-1]) + float(pointsOverallMidfield2[-1])+ float(pointsOverallForward2[-1]))
        
        pointsAttackDefense1 = pointsAttack1 + pointsDefense1
        pointsAttackDefense2 = pointsAttack2 + pointsDefense2
        
        # Values of each group
        bars1 = [((pointsOverallMainTeam1/(pointsOverallMainTeam1+pointsOverallMainTeam2))*100)*0.3,((pointsOverallMainTeam2/(pointsOverallMainTeam1+pointsOverallMainTeam2))*100)*0.3] #se calcula sobre 100 la puntuación para que no salgan números muy grandes y se multiplica por la ponderancia de cada división
        bars2 = [((pointsZones1/(pointsZones1+pointsZones2)*100))*0.2,((pointsZones2/(pointsZones1+pointsZones2)*100))*0.2]
        bars3 = [((pointsAttackDefense1/(pointsAttackDefense1+pointsAttackDefense2)*100))*0.3,((pointsAttackDefense2/(pointsAttackDefense1+pointsAttackDefense2)*100))*0.3]
        bars4 = [((pointsVSPlayers1/(pointsVSPlayers1+pointsVSPlayers2)*100))*0.2,((pointsVSPlayers2/(pointsVSPlayers1+pointsVSPlayers2)*100))*0.2]
         
        # The position of the bars on the x-axis
        r = [0,1]
        # Names of group
        names = [team1,team2]
        
        # Create brown bars
        p1 = plt.bar(r, bars1, color='r', edgecolor='white', width=0.5)
        p2 = plt.bar(r, bars2, bottom=bars1, color='g', edgecolor='white', width=0.5)
        p3 = plt.bar(r, bars3, bottom=np.array(bars1)+np.array(bars2), color='b', edgecolor='white', width=0.5)
        p4 = plt.bar(r, bars4, bottom=np.array(bars1)+np.array(bars2)+np.array(bars3), color='y', edgecolor='white', width=0.5)
        
        plt.legend((p1[0], p2[0],p3[0],p4[0]), ("Puntos de equipo como conjunto", "Puntos de cada zona del campo(defensa,medio,centro","Puntos de ataque y defensa","Puntos individuales de cada jugador totales")) 
        # Custom X axis
        plt.xticks(r, names, fontweight='bold')
        plt.xlabel("Equipos")
        plt.ylabel('Puntuación')
        
        #plt.subplot(2, 2, 1)
       

   
        # refresh canvas 
        self.canvas.draw() 
    def plot2(self):
        plt.plot([1, 2, 3, 4])
        #plt.subplot(2, 2, 2)
        plt.ylabel('some numbers')
        self.canvas2.draw()
    
      
    
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
            elif i == 17:
                team2 = line
      
    # creating apyqt5 application 
    app = QApplication(sys.argv) 
    # creating a window object 
    main = Window(mainTeam1,mainTeam2,pointsVSPlayers1,pointsVSPlayers2,pointsOverallMainTeam1,pointsOverallMainTeam2,pointsOverallDefense1,pointsOverallMidfield1,pointsOverallForward1,pointsOverallDefense2,pointsOverallMidfield2,pointsOverallForward2,pointsAttack1,pointsDefense1,pointsAttack2,pointsDefense2,team1,team2) 
       
    # showing the window 
    main.show() 
   
    # loop 
    sys.exit(app.exec_()) 
  