#!/usr/bin/env python3

import os

class Estimate:
    
    def __init__(self,conexion,team1,team2):
        self.conexion = conexion
        self.team1 = team1
        self.team2 = team2
     
        mainTeam1,mainTeam2 = self.createMainTeam(self.conexion,self.team1,self.team2)

        mainTeam1 = self.overallCalculation(mainTeam1)
        mainTeam2 = self.overallCalculation(mainTeam2)

        if (len(mainTeam1) or len(mainTeam2)) != 11:
            print("Error, tamaño de equipo incorrecto")
        else:
            #Hacer todo lo demás
            pointsVSPlayers1,pointsVSPlayer2 = self.pointsPlayerVSPlayer(mainTeam1[:],mainTeam2[:])#[:] es para pasarle una copia ya que las dos listas se modifican dentro de la función y afectaria a esas mismas lista fuera de ella
            pointsOverallMainTeam1,pointsOverallMainTeam2 = self.overallMainTeam(mainTeam1,mainTeam2)
            pointsOverallDefense1,pointsOverallMidfield1, pointsOverallForward1 = self.pointsOverallZone(mainTeam1)
            pointsOverallDefense2,pointsOverallMidfield2, pointsOverallForward2 = self.pointsOverallZone(mainTeam2)
            pointsAttack1,pointsDefense1,pointsAttack2,pointsDefense2 = self.pointsAttackVSDefense(pointsOverallDefense1,pointsOverallMidfield1, pointsOverallForward1,pointsOverallDefense2,pointsOverallMidfield2, pointsOverallForward2)
            
            
            file = open("settings.txt", "w") #abre un archivo de texto, lo crea si no existe
            self.fileWrite(file,mainTeam1)
            self.fileWrite(file,mainTeam2)
            self.fileWrite(file,pointsVSPlayers1)
            self.fileWrite(file,pointsVSPlayer2)
            self.fileWrite(file,pointsOverallMainTeam1)
            self.fileWrite(file,pointsOverallMainTeam2)
            self.fileWrite(file,pointsOverallDefense1)
            self.fileWrite(file,pointsOverallMidfield1)
            self.fileWrite(file,pointsOverallForward1)
            self.fileWrite(file,pointsOverallDefense2)
            self.fileWrite(file,pointsOverallMidfield2)
            self.fileWrite(file,pointsOverallForward2)
            self.fileWrite(file,pointsAttack1)
            self.fileWrite(file,pointsDefense1)
            self.fileWrite(file,pointsAttack2)
            self.fileWrite(file,pointsDefense2)
            self.fileWrite(file,team1)
            self.fileWrite(file,team2)

            
            file.close()
            
            os.system("python3 ResultsWindow.py")
                      

    def fileWrite(self,file,listOrInt):
        if isinstance(listOrInt, int) or isinstance(listOrInt, float) or isinstance(listOrInt, str):# si es int, float o cadena entra aquí si no será una lista
            file.write("{}\n".format(listOrInt))
        else:#añadimos cada list o int a una nueva linea del archivo
            for item in listOrInt:
                file.write("%s;" % item)
            file.write("\n")  
            
    def createMainTeam(self,conexion,team1,team2):
        players1 = conexion.query("MATCH (p)-[r:PLAYS]->(c) WHERE c.id='{team}' RETURN DISTINCT p.name,r.teamPosition".format(team=team1)) #obtenemos todos los jugadores y sus correspondientes posiciones en los equipos
        players2 = conexion.query("MATCH (p)-[r:PLAYS]->(c) WHERE c.id='{team}' RETURN DISTINCT p.name,r.teamPosition".format(team=team2))
        players1 = [player.replace("'","") for player in players1] #limpiamos de comillas la lista de strings,corchetes y espacios
        players1 = [player[1:-1] for player in players1]
        players2 = [player.replace("'", "") for player in players2]
        players2= [player[1:-1] for player in players2]

        mainTeam1 = self.filterTeam(players1)
        mainTeam2 = self.filterTeam(players2)
        return mainTeam1,mainTeam2
        
    def overallCalculation(self,mainTeam):#aquí calculamos los puntos totales de cada jugador en el enfrentamiento
        mainTeamReturn = [] #hacemos una nueva lista para meter los jugadores con el overall
        for player in mainTeam:
            statistics = grades = overall = 0
            if(player.split(",")[1] == " GK"):#ojo hay que poner el espacio porque es lo que contiene el String

                statistics = self.conexion.query("MATCH (p:Player) WHERE p.name='{player1}' RETURN  p.height_cm,p.gkDiving,p.gkHandling,p.gkKicking,p.gkReflexes,p.gkSpeed,p.gkPositioning,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityComposure,p.mentalityVision,p.attackingVolleys,p.movementAgility,p.movementReactions,p.mentalityInterceptions".format(player1=(player.split(",")[0])))
                grades = self.conexion.query("MATCH (p:Position) WHERE p.id='GK' RETURN p.height_cm,p.gkDiving,p.gkHandling,p.gkKicking,p.gkReflexes,p.gkSpeed,p.gkPositioning,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityComposure,p.mentalityVision,p.attackingVolleys,p.movementAgility,p.movementReactions,p.mentalityInterceptions")
                statistics = statistics[0].replace(",","")[1:-1]
                statistics = statistics.split(" ")
                grades = grades[0].replace(",","")[1:-1]
                grades = grades.split(" ")

                height = False
                for statistic,grade in zip(statistics,grades):
                    if height == False:
                        height = True
                        if int(float(statistic)) > 180 and int(float(statistic)) < 190: # si la altura del portero esta entre 1,8 y 1,9 m lo contamos para el overall
                            overall = int(float(statistic))*int(float(grade))
                    else:
                        
                        overall = overall + (int(statistic)*int(grade))
                mainTeamReturn.append(player +"," + str(overall))
                
            if(player.split(",")[1] == " LCB" or player.split(",")[1] == " RCB"):#ojo hay que poner el espacio porque es lo que contiene el String

                statistics = self.conexion.query("MATCH (p:Player) WHERE p.name='{player1}' RETURN  p.shooting,p.dribbling,p.defending,p.attackingCrossing,p.attackingFinishing,p.attackingHeadingAccuracy,p.attackingShortPassing,p.attackingVolleys,p.skillLongPassing,p.skillBallControl,p.movementAcceleration,p.movementSprintSpeed,p.movementAgility,p.movementReactions,p.movementBalance,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityInterceptions,p.mentalityVision,p.mentalityComposure,p.defendingMarking,p.defendingSlidingTackle,p.defendingStandingTackle".format(player1=(player.split(",")[0])))
                grades = self.conexion.query("MATCH (p:Position) WHERE p.id='LCBaRCB' RETURN p.shooting,p.dribbling,p.defending,p.attackingCrossing,p.attackingFinishing,p.attackingHeadingAccuracy,p.attackingShortPassing,p.attackingVolleys,p.skillLongPassing,p.skillBallControl,p.movementAcceleration,p.movementSprintSpeed,p.movementAgility,p.movementReactions,p.movementBalance,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityInterceptions,p.mentalityVision,p.mentalityComposure,p.defendingMarking,p.defendingSlidingTackle,p.defendingStandingTackle")
                statistics = statistics[0].replace(",","")[1:-1]
                statistics = statistics.split(" ")
                grades = grades[0].replace(",","")[1:-1]
                grades = grades.split(" ")
                
                for statistic,grade in zip(statistics,grades):
                    overall = overall + (int(statistic)*int(grade))
                    
                mainTeamReturn.append(player +"," + str(overall))
            
            if(player.split(",")[1] == " LB" or player.split(",")[1] == " LWB" or player.split(",")[1] == " RB" or player.split(",")[1] == " RWB"):#ojo hay que poner el espacio porque es lo que contiene el String

                statistics = self.conexion.query("MATCH (p:Player) WHERE p.name='{player1}' RETURN  p.shooting,p.dribbling,p.defending,p.attackingCrossing,p.attackingFinishing,p.attackingHeadingAccuracy,p.attackingShortPassing,p.attackingVolleys,p.skillLongPassing,p.skillBallControl,p.movementAcceleration,p.movementSprintSpeed,p.movementAgility,p.movementReactions,p.movementBalance,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityInterceptions,p.mentalityVision,p.mentalityComposure,p.defendingMarking,p.defendingSlidingTackle,p.defendingStandingTackle".format(player1=(player.split(",")[0])))
                grades = self.conexion.query("MATCH (p:Position) WHERE p.id='LBaLWBaRBaRWB' RETURN p.shooting,p.dribbling,p.defending,p.attackingCrossing,p.attackingFinishing,p.attackingHeadingAccuracy,p.attackingShortPassing,p.attackingVolleys,p.skillLongPassing,p.skillBallControl,p.movementAcceleration,p.movementSprintSpeed,p.movementAgility,p.movementReactions,p.movementBalance,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityInterceptions,p.mentalityVision,p.mentalityComposure,p.defendingMarking,p.defendingSlidingTackle,p.defendingStandingTackle")
                statistics = statistics[0].replace(",","")[1:-1]
                statistics = statistics.split(" ")
                grades = grades[0].replace(",","")[1:-1]
                grades = grades.split(" ")
                
                for statistic,grade in zip(statistics,grades):
                    overall = overall + (int(statistic)*int(grade))
                    
                mainTeamReturn.append(player +"," + str(overall))
            
            if player.split(",")[1] == " CDM":
               
                statistics = self.conexion.query("MATCH (p:Player) WHERE p.name='{player1}' RETURN  p.shooting,p.dribbling,p.defending,p.attackingCrossing,p.attackingFinishing,p.attackingHeadingAccuracy,p.attackingShortPassing,p.attackingVolleys,p.skillLongPassing,p.skillBallControl,p.movementAcceleration,p.movementSprintSpeed,p.movementAgility,p.movementReactions,p.movementBalance,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityInterceptions,p.mentalityVision,p.mentalityComposure,p.defendingMarking,p.defendingSlidingTackle,p.defendingStandingTackle".format(player1=(player.split(",")[0])))
                grades = self.conexion.query("MATCH (p:Position) WHERE p.id='CDM' RETURN p.shooting,p.dribbling,p.defending,p.attackingCrossing,p.attackingFinishing,p.attackingHeadingAccuracy,p.attackingShortPassing,p.attackingVolleys,p.skillLongPassing,p.skillBallControl,p.movementAcceleration,p.movementSprintSpeed,p.movementAgility,p.movementReactions,p.movementBalance,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityInterceptions,p.mentalityVision,p.mentalityComposure,p.defendingMarking,p.defendingSlidingTackle,p.defendingStandingTackle")
                statistics = statistics[0].replace(",","")[1:-1]
                statistics = statistics.split(" ")
                grades = grades[0].replace(",","")[1:-1]
                grades = grades.split(" ")
                
                for statistic,grade in zip(statistics,grades):
                    overall = overall + (int(statistic)*int(grade))
                    
                mainTeamReturn.append(player +"," + str(overall))
            
            if player.split(",")[1] == " CM":
               
                statistics = self.conexion.query("MATCH (p:Player) WHERE p.name='{player1}' RETURN  p.shooting,p.dribbling,p.defending,p.attackingCrossing,p.attackingFinishing,p.attackingHeadingAccuracy,p.attackingShortPassing,p.attackingVolleys,p.skillLongPassing,p.skillBallControl,p.movementAcceleration,p.movementSprintSpeed,p.movementAgility,p.movementReactions,p.movementBalance,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityInterceptions,p.mentalityVision,p.mentalityComposure,p.defendingMarking,p.defendingSlidingTackle,p.defendingStandingTackle".format(player1=(player.split(",")[0])))
                grades = self.conexion.query("MATCH (p:Position) WHERE p.id='CM' RETURN p.shooting,p.dribbling,p.defending,p.attackingCrossing,p.attackingFinishing,p.attackingHeadingAccuracy,p.attackingShortPassing,p.attackingVolleys,p.skillLongPassing,p.skillBallControl,p.movementAcceleration,p.movementSprintSpeed,p.movementAgility,p.movementReactions,p.movementBalance,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityInterceptions,p.mentalityVision,p.mentalityComposure,p.defendingMarking,p.defendingSlidingTackle,p.defendingStandingTackle")
                statistics = statistics[0].replace(",","")[1:-1]
                statistics = statistics.split(" ")
                grades = grades[0].replace(",","")[1:-1]
                grades = grades.split(" ")
                
                for statistic,grade in zip(statistics,grades):
                    overall = overall + (int(statistic)*int(grade))
                    
                mainTeamReturn.append(player +"," + str(overall))
            
            if(player.split(",")[1] == " LCM" or player.split(",")[1] == " RCM"):

                statistics = self.conexion.query("MATCH (p:Player) WHERE p.name='{player1}' RETURN  p.shooting,p.dribbling,p.defending,p.attackingCrossing,p.attackingFinishing,p.attackingHeadingAccuracy,p.attackingShortPassing,p.attackingVolleys,p.skillLongPassing,p.skillBallControl,p.movementAcceleration,p.movementSprintSpeed,p.movementAgility,p.movementReactions,p.movementBalance,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityInterceptions,p.mentalityVision,p.mentalityComposure,p.defendingMarking,p.defendingSlidingTackle,p.defendingStandingTackle".format(player1=(player.split(",")[0])))
                grades = self.conexion.query("MATCH (p:Position) WHERE p.id='LCMaRCM' RETURN p.shooting,p.dribbling,p.defending,p.attackingCrossing,p.attackingFinishing,p.attackingHeadingAccuracy,p.attackingShortPassing,p.attackingVolleys,p.skillLongPassing,p.skillBallControl,p.movementAcceleration,p.movementSprintSpeed,p.movementAgility,p.movementReactions,p.movementBalance,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityInterceptions,p.mentalityVision,p.mentalityComposure,p.defendingMarking,p.defendingSlidingTackle,p.defendingStandingTackle")
                statistics = statistics[0].replace(",","")[1:-1]
                statistics = statistics.split(" ")
                grades = grades[0].replace(",","")[1:-1]
                grades = grades.split(" ")
                
                for statistic,grade in zip(statistics,grades):
                    overall = overall + (int(statistic)*int(grade))
                    
                mainTeamReturn.append(player +"," + str(overall))
            
            if player.split(",")[1] == " CAM":
               
                statistics = self.conexion.query("MATCH (p:Player) WHERE p.name='{player1}' RETURN  p.shooting,p.dribbling,p.defending,p.attackingCrossing,p.attackingFinishing,p.attackingHeadingAccuracy,p.attackingShortPassing,p.attackingVolleys,p.skillLongPassing,p.skillBallControl,p.movementAcceleration,p.movementSprintSpeed,p.movementAgility,p.movementReactions,p.movementBalance,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityInterceptions,p.mentalityVision,p.mentalityComposure,p.defendingMarking,p.defendingSlidingTackle,p.defendingStandingTackle".format(player1=(player.split(",")[0])))
                grades = self.conexion.query("MATCH (p:Position) WHERE p.id='CAM' RETURN p.shooting,p.dribbling,p.defending,p.attackingCrossing,p.attackingFinishing,p.attackingHeadingAccuracy,p.attackingShortPassing,p.attackingVolleys,p.skillLongPassing,p.skillBallControl,p.movementAcceleration,p.movementSprintSpeed,p.movementAgility,p.movementReactions,p.movementBalance,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityInterceptions,p.mentalityVision,p.mentalityComposure,p.defendingMarking,p.defendingSlidingTackle,p.defendingStandingTackle")
                statistics = statistics[0].replace(",","")[1:-1]
                statistics = statistics.split(" ")
                grades = grades[0].replace(",","")[1:-1]
                grades = grades.split(" ")
                
                for statistic,grade in zip(statistics,grades):
                    overall = overall + (int(statistic)*int(grade))
                
                mainTeamReturn.append(player +"," + str(overall))
                
            if player.split(",")[1] == " CF":
               
                statistics = self.conexion.query("MATCH (p:Player) WHERE p.name='{player1}' RETURN  p.shooting,p.dribbling,p.defending,p.attackingCrossing,p.attackingFinishing,p.attackingHeadingAccuracy,p.attackingShortPassing,p.attackingVolleys,p.skillLongPassing,p.skillBallControl,p.movementAcceleration,p.movementSprintSpeed,p.movementAgility,p.movementReactions,p.movementBalance,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityInterceptions,p.mentalityVision,p.mentalityComposure,p.defendingMarking,p.defendingSlidingTackle,p.defendingStandingTackle".format(player1=(player.split(",")[0])))
                grades = self.conexion.query("MATCH (p:Position) WHERE p.id='CF' RETURN p.shooting,p.dribbling,p.defending,p.attackingCrossing,p.attackingFinishing,p.attackingHeadingAccuracy,p.attackingShortPassing,p.attackingVolleys,p.skillLongPassing,p.skillBallControl,p.movementAcceleration,p.movementSprintSpeed,p.movementAgility,p.movementReactions,p.movementBalance,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityInterceptions,p.mentalityVision,p.mentalityComposure,p.defendingMarking,p.defendingSlidingTackle,p.defendingStandingTackle")
                statistics = statistics[0].replace(",","")[1:-1]
                statistics = statistics.split(" ")
                grades = grades[0].replace(",","")[1:-1]
                grades = grades.split(" ")
                
                for statistic,grade in zip(statistics,grades):
                    overall = overall + (int(statistic)*int(grade))
                    
                mainTeamReturn.append(player +"," + str(overall))
            
            if player.split(",")[1] == " ST":
               
                statistics = self.conexion.query("MATCH (p:Player) WHERE p.name='{player1}' RETURN  p.shooting,p.dribbling,p.defending,p.attackingCrossing,p.attackingFinishing,p.attackingHeadingAccuracy,p.attackingShortPassing,p.attackingVolleys,p.skillLongPassing,p.skillBallControl,p.movementAcceleration,p.movementSprintSpeed,p.movementAgility,p.movementReactions,p.movementBalance,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityInterceptions,p.mentalityVision,p.mentalityComposure,p.defendingMarking,p.defendingSlidingTackle,p.defendingStandingTackle".format(player1=(player.split(",")[0])))
                grades = self.conexion.query("MATCH (p:Position) WHERE p.id='ST' RETURN p.shooting,p.dribbling,p.defending,p.attackingCrossing,p.attackingFinishing,p.attackingHeadingAccuracy,p.attackingShortPassing,p.attackingVolleys,p.skillLongPassing,p.skillBallControl,p.movementAcceleration,p.movementSprintSpeed,p.movementAgility,p.movementReactions,p.movementBalance,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityInterceptions,p.mentalityVision,p.mentalityComposure,p.defendingMarking,p.defendingSlidingTackle,p.defendingStandingTackle")
                statistics = statistics[0].replace(",","")[1:-1]
                statistics = statistics.split(" ")
                grades = grades[0].replace(",","")[1:-1]
                grades = grades.split(" ")
                
                for statistic,grade in zip(statistics,grades):
                    overall = overall + (int(statistic)*int(grade))
                    
                mainTeamReturn.append(player +"," + str(overall))
                    
            if(player.split(",")[1] == " LW" or player.split(",")[1] == " RW"):
               
                statistics = self.conexion.query("MATCH (p:Player) WHERE p.name='{player1}' RETURN  p.shooting,p.dribbling,p.defending,p.attackingCrossing,p.attackingFinishing,p.attackingHeadingAccuracy,p.attackingShortPassing,p.attackingVolleys,p.skillLongPassing,p.skillBallControl,p.movementAcceleration,p.movementSprintSpeed,p.movementAgility,p.movementReactions,p.movementBalance,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityInterceptions,p.mentalityVision,p.mentalityComposure,p.defendingMarking,p.defendingSlidingTackle,p.defendingStandingTackle".format(player1=(player.split(",")[0])))
                grades = self.conexion.query("MATCH (p:Position) WHERE p.id='LWaRW' RETURN p.shooting,p.dribbling,p.defending,p.attackingCrossing,p.attackingFinishing,p.attackingHeadingAccuracy,p.attackingShortPassing,p.attackingVolleys,p.skillLongPassing,p.skillBallControl,p.movementAcceleration,p.movementSprintSpeed,p.movementAgility,p.movementReactions,p.movementBalance,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityInterceptions,p.mentalityVision,p.mentalityComposure,p.defendingMarking,p.defendingSlidingTackle,p.defendingStandingTackle")
                statistics = statistics[0].replace(",","")[1:-1]
                statistics = statistics.split(" ")
                grades = grades[0].replace(",","")[1:-1]
                grades = grades.split(" ")
                
                for statistic,grade in zip(statistics,grades):
                    overall = overall + (int(statistic)*int(grade))
                    
                mainTeamReturn.append(player +"," + str(overall))
                
        return mainTeamReturn
                        
    def overallMainTeam(self,mainTeam1,mainTeam2):
        points1 = points2 = 0
        for player1,player2 in zip(mainTeam1,mainTeam2):
            points1 = points1 + int(player1.split(",")[2])
            points2 = points2 + int(player2.split(",")[2])
        return points1,points2
                
    def pointsOverallZone(self,mainTeam):
        zoneDefense = []
        zoneMidfield = [] 
        zoneForward = [] #en la lista se almacena de cada zona la puntuacion de cada zona total junto a los jugadores
        pointsDefense =  pointsMidfield = pointsForward = 0
        
        for player in mainTeam:
            if player.split(",")[1] == " GK" or player.split(",")[1] == " LB" or player.split(",")[1] == " LWB" or player.split(",")[1] == " LCB" or player.split(",")[1] == " RCB"  or player.split(",")[1] == " RB" or player.split(",")[1] == " RWB":
                pointsDefense = pointsDefense + int(player.split(",")[2])
                zoneDefense.append(player)        
            if player.split(",")[1] == " CDM" or player.split(",")[1] == " CM" or player.split(",")[1] == " LCM" or player.split(",")[1] == " RCM" or player.split(",")[1] == " CAM":
                pointsMidfield = pointsMidfield + int(player.split(",")[2])
                zoneMidfield.append(player)
            if player.split(",")[1] == " CF" or player.split(",")[1] == " ST" or player.split(",")[1] == " LW" or player.split(",")[1] == " RW":
                pointsForward = pointsForward + int(player.split(",")[2])
                zoneForward.append(player)
        
        pointsDefense = pointsDefense/len(zoneDefense)#en este caso calculamos la media, no el total, ya que no tiene porque haber el mismo número de jugadores en cada zona
        pointsMidfield = pointsMidfield/len(zoneMidfield)
        pointsForward = pointsForward/len(zoneForward)
        
        zoneDefense.append(pointsDefense) #añadimos la media a la propia lista
        zoneMidfield.append(pointsMidfield)
        zoneForward.append(pointsForward)
        
        return zoneDefense,zoneMidfield,zoneForward
    
    def pointsAttackVSDefense(self,pointsOverallDefense1,pointsOverallMidfield1, pointsOverallForward1,pointsOverallDefense2,pointsOverallMidfield2, pointsOverallForward2):
        
        pointsAttack1 = (pointsOverallMidfield1[-1] + pointsOverallForward1[-1])/(len(pointsOverallMidfield1)+len(pointsOverallForward1)-2) #para calcular los puntos de ataque sumamos la media de la delantera y el medio y hacemos la media
        pointsDefense1 = (pointsOverallMidfield1[-1] + pointsOverallDefense1[-1])/(len(pointsOverallMidfield1)+len(pointsOverallDefense1)-2) #el -2 esta puesto porque al final de la lista esta la media almacenada
        pointsAttack2 = (pointsOverallMidfield2[-1] + pointsOverallForward2[-1])/(len(pointsOverallMidfield2)+len(pointsOverallForward2)-2)
        pointsDefense2 = (pointsOverallMidfield2[-1] + pointsOverallDefense2[-1])/(len(pointsOverallMidfield2)+len(pointsOverallDefense2)-2)
        
        return pointsAttack1,pointsDefense1,pointsAttack2,pointsDefense2
    
    def pointsPlayerVSPlayer(self,mainTeam1,mainTeam2): #comparamos posición por posición y se restan, el que tenga mas puntos se lleva la diferencia para el equipo, si no existe la posición cuenta como si fuera cero
        pointsVS1 = pointsVS2 = 0
        listaAux1 = listaAux2 = [] #usada para saber cuales posiciones no coinciden
        for player1 in mainTeam1:
            for player2 in mainTeam2:
                if player1.split(",")[1] == player2.split(",")[1]:#si coincide la misma posición
                    if int(player1.split(",")[2]) > int(player2.split(",")[2]):#restamos los puntos de cada posición y lo sumamos al total del que ha ganado
                        pointsVS1 = pointsVS1 + (int(player1.split(",")[2]) - int(player2.split(",")[2]))
                    elif int(player1.split(",")[2]) < int(player2.split(",")[2]):# si tiene los mismo puntos(no suma ni resta)
                        pointsVS2 = pointsVS2 + (int(player2.split(",")[2]) - int(player1.split(",")[2]))
                    
                    listaAux1.append(player1)
                    listaAux2.append(player2)
                    break
                
        for player1 in listaAux1:
            if player1 in mainTeam1:#vamos quitando los jugadores comparados
                mainTeam1.remove(player1)
        
        for player2 in listaAux2:
            if player2 in mainTeam2:#vamos quitando los jugadores comparados
                mainTeam2.remove(player2)
                
        #Si hay posiciones que no se repiten en los equipos, añadimos los puntos totales de los jugadores
        for player1 in mainTeam1:
            pointsVS1 = pointsVS1 + int(player1.split(",")[2])
        for player2 in mainTeam2:
            pointsVS2 = pointsVS2 + int(player2.split(",")[2])
            
        return pointsVS1,pointsVS2
    def filterTeam(self,players):
        mainTeam = []
        
        for player in players:
            pos = player.split(',')[-1] #cojemos el substring que almacena la posición del jugador
            if pos != " SUB" and pos != " RES" and pos != " " and pos != "" and pos != None:#Si no es un suplente o vacio lo añadimos a la lista de titulares
                mainTeam.append(player)
                
        return mainTeam
    