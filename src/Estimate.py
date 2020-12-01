#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
            pointsOverallMainTeam1,pointsOverallMainTeam2 = self.overallMainTeam(mainTeam1,mainTeam2)
            pointsOverallDefense1,pointsOverallMidfield1, pointsOverallForward1 = self.pointsOverallZone(mainTeam1)
            pointsOverallDefense2,pointsOverallMidfield2, pointsOverallForward2 = self.pointsOverallZone(mainTeam2)

            
    def createMainTeam(self,conexion,team1,team2):#Táctica 4-3-3
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
        
        zoneDefense.append(pointsDefense) #añadimos los puntos totales tambien
        zoneMidfield.append(pointsMidfield)
        zoneForward.append(pointsForward)
        
        return zoneDefense,zoneMidfield,zoneForward
        
    def filterTeam(self,players):
        mainTeam = []
        
        for player in players:
            pos = player.split(',')[-1] #cojemos el substring que almacena la posición del jugador
            if pos != " SUB" and pos != " RES" and pos != " " and pos != "" and pos != None:#Si no es un suplente o vacio lo añadimos a la lista de titulares
                mainTeam.append(player)
                
        return mainTeam
    