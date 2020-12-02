#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# importing various libraries 
import sys 
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 
 
import matplotlib.pyplot as plt 
import numpy as np

   
# main window 
# which inherits QDialog 
class Window(QDialog): 
       
    # constructor 
    def __init__(self,mainTeam1,mainTeam2,pointsVSPlayers1,pointsVSPlayer2,pointsOverallMainTeam1,pointsOverallMainTeam2,pointsOverallDefense1,pointsOverallMidfield1,pointsOverallForward1,pointsOverallDefense2,pointsOverallMidfield2,pointsOverallForward2,pointsAttack1,pointsDefense1,pointsAttack2,pointsDefense2,team1,team2,parent=None): 
        super(Window, self).__init__(parent) 
        self.mainTeam1 = mainTeam1
        self.mainTeam2 = mainTeam2
        self.pointsVSPlayers1 = pointsVSPlayers1
        self.pointsVSPlayer2 = pointsVSPlayer2
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
        
        #ploteamos el grafico
        self.plot(team1,team2)
        
        # creating a Vertical Box layout 
        layout = QVBoxLayout() 
 
        # adding canvas to the layout 
        layout.addWidget(self.canvas) 
 
        # setting layout to the main window 
        self.setLayout(layout) 
   
    
    def plot(self,team1,team2): 
           
        # Values of each group
        bars1 = [12, 28]
        bars2 = [28, 7]
        bars3 = [25, 3]
         
        # Heights of bars1 + bars2
        bars = np.add(bars1, bars2).tolist()
         
        # The position of the bars on the x-axis
        r = [0,1]
         
        # Names of group and bar width
        names = [team1,team2]
        barWidth = 0.5
        
        # Create brown bars
        plt.bar(r, bars1, color='#7f6d5f', edgecolor='white', width=barWidth)
        # Create green bars (middle), on top of the firs ones
        plt.bar(r, bars2, bottom=bars1, color='#557f2d', edgecolor='white', width=barWidth)
        # Create green bars (top)
        plt.bar(r, bars3, bottom=bars, color='#2d7f5e', edgecolor='white', width=barWidth)
         
        # Custom X axis
        plt.xticks(r, names, fontweight='bold')
        plt.xlabel("group")
        plt.ylabel('Undamped')
        
        #plt.subplot(2, 1, 1)

       

   
        # refresh canvas 
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
                pointsVSPlayer2 = int(line)
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
    main = Window(mainTeam1,mainTeam2,pointsVSPlayers1,pointsVSPlayer2,pointsOverallMainTeam1,pointsOverallMainTeam2,pointsOverallDefense1,pointsOverallMidfield1,pointsOverallForward1,pointsOverallDefense2,pointsOverallMidfield2,pointsOverallForward2,pointsAttack1,pointsDefense1,pointsAttack2,pointsDefense2,team1,team2) 
       
    # showing the window 
    main.show() 
   
    # loop 
    sys.exit(app.exec_()) 
  