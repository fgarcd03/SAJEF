#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Aquí se hacen la mayoría de los cálculos
import os
import statistics as st
import itertools as it
import numpy as np
import copy

class Estimate:
    
    def __init__(self,conexion,team1,team2,mainTeam2,combinatoricsTeam1,combinatoricsTeam2):
        self.conexion = conexion
        self.team1 = team1
        self.team2 = team2
        self.mainTeam1 = []
        self.mainTeam2 = mainTeam2
        self.combinatoricsTeam1 = combinatoricsTeam1
        self.combinatoricsTeam2 = combinatoricsTeam2
        
        self.mainTeam1 = self.createMainTeam(self.mainTeam1,self.team1,self.combinatoricsTeam1)
        
        if self.combinatoricsTeam2:#si usamos combinatoria en el equipo 2 llamamos al método para que cree el equipo pero si no, no llamamos porque ya está echo el equipo
            self.mainTeam2 = self.createMainTeam(self.mainTeam2,self.team2,self.combinatoricsTeam2)
        
        self.mainTeam1 = self.overallCalculation(self.mainTeam1)
        self.mainTeam2 = self.overallCalculation(self.mainTeam2)
        
        if len(self.mainTeam1) != 11 or len(self.mainTeam2) != 11:

            print("Error, tamaño de equipo incorrecto")
            print("Tamaño de equipo 1: " + str(len(self.mainTeam1)))
            print("Tamaño de equipo 2: " + str(len(self.mainTeam2)))
        else:

            bonusDefense1, bonusMidfield1, bonusForward1 = self.checkUnbalance(self.mainTeam1)
            bonusDefense2, bonusMidfield2, bonusForward2 = self.checkUnbalance(self.mainTeam2)
            
            pointsVSPlayers1,pointsVSPlayer2 = self.pointsPlayerVSPlayer(self.mainTeam1[:],self.mainTeam2[:])#[:] es para pasarle una copia ya que las dos listas se modifican dentro de la función y afectaría a esas mismas lista fuera de ella
            pointsOverallMainTeam1,pointsOverallMainTeam2 = self.overallMainTeam()
            pointsOverallDefense1,pointsOverallMidfield1, pointsOverallForward1 = self.pointsOverallZone(self.mainTeam1)
            pointsOverallDefense2,pointsOverallMidfield2, pointsOverallForward2 = self.pointsOverallZone(self.mainTeam2)
            
            pointsOverallDefense1[-1] = pointsOverallDefense1[-1] + (pointsOverallDefense1[-1]*bonusDefense1/100) #para estas puntuaciones le sumamos las bonificaciones aquí en vez de en la escritura del fichero, asi vamos arrastrando los cambios a otros datos
            pointsOverallDefense2[-1] = pointsOverallDefense2[-1] + (pointsOverallDefense2[-1]*bonusDefense2/100)
            pointsOverallMidfield1[-1] = pointsOverallMidfield1[-1] + (pointsOverallMidfield1[-1]*bonusMidfield1/100)
            pointsOverallMidfield2[-1] = pointsOverallMidfield2[-1] + (pointsOverallMidfield2[-1]*bonusMidfield2/100)
            pointsOverallForward1[-1] = pointsOverallForward1[-1]+ (pointsOverallForward1[-1]*bonusForward1/100)
            pointsOverallForward2[-1] = pointsOverallForward2[-1] + (pointsOverallForward2[-1]*bonusForward2/100)
            
            pointsAttack1,pointsDefense1,pointsAttack2,pointsDefense2 = self.pointsAttackVSDefense(pointsOverallDefense1,pointsOverallMidfield1, pointsOverallForward1,pointsOverallDefense2,pointsOverallMidfield2, pointsOverallForward2)
            
            
            file = open("settings.conf", "w") #abre un archivo de texto, lo crea si no existe y vamos escribiendo todos los datos que hemos recogido

            self.fileWrite(file,self.mainTeam1)
            self.fileWrite(file,self.mainTeam2)
            self.fileWrite(file,pointsVSPlayers1)
            self.fileWrite(file,pointsVSPlayer2)
            self.fileWrite(file,pointsOverallMainTeam1 + (pointsOverallMainTeam1*bonusDefense1/100) + (pointsOverallMainTeam1*bonusMidfield1/100) + (pointsOverallMainTeam1*bonusForward1/100))
            self.fileWrite(file,pointsOverallMainTeam2 + (pointsOverallMainTeam2*bonusDefense2/100) + (pointsOverallMainTeam2*bonusMidfield2/100) + (pointsOverallMainTeam2*bonusForward2/100))
            self.fileWrite(file,pointsOverallDefense1[-1])
            self.fileWrite(file,pointsOverallDefense2[-1])
            self.fileWrite(file,pointsOverallMidfield1[-1])
            self.fileWrite(file,pointsOverallMidfield2[-1])
            self.fileWrite(file,pointsOverallForward1[-1])
            self.fileWrite(file,pointsOverallForward2[-1])
            self.fileWrite(file,pointsAttack1)
            self.fileWrite(file,pointsAttack2)
            self.fileWrite(file,pointsDefense1)
            self.fileWrite(file,pointsDefense2)
            self.fileWrite(file,team1)
            self.fileWrite(file,team2)

            file.close()
            
            os.system("python3 {}/ResultsWindow.py &".format(os.path.dirname(os.path.realpath(__file__))))

    def fileWrite(self,file,listOrInt):
        if isinstance(listOrInt, int) or isinstance(listOrInt, float) or isinstance(listOrInt, str):
            file.write("{}\n".format(listOrInt))
        else:
            for item in listOrInt:
                file.write("%s;" % item)
            file.write("\n")  
    
    #Creamos el equipo titular con o sin combinatoria
    def createMainTeam(self,mainTeam,team,combinatorics):
        defense = []
        midfield = []
        forward = []
        defenseCombined = []
        midfieldCombined = []
        forwardCombined = []
        combined = []
        grades = []
        statistics = []
        positionsDefense = ["LB","LWB","LCB","RCB","RB","RWB","CB"]
        positionsMidfield = ["CDM","CM","LCM","RCM","CAM","LM","RM","RDM","LDM","LAM","RAM"]
        positionsForward = ["CF","ST","LW","RW","LS","RS"]
        
        players = self.conexion.query("MATCH (p)-[r:PLAYS]->(c) WHERE c.id='{}' RETURN DISTINCT p.name,r.teamPosition".format(team))
        players = [player.replace("'","") for player in players]
        players = [player[1:-1] for player in players]
        
        if combinatorics:#aquí hacemos la combinatoria
            grades,statistics = self.dataCache(players)
        
            #Para elegir el equipo: el portero será el que existe por defecto en la base de datos, con 4 defensas, 3 centrocampistas y 3 delanteros
            for player in players:
                if player.split(",")[1] == " GK":
                    mainTeam.append(player)

                if "LB" in player or "LWB" in player or "LCB" in player or "RCB" in player or "RB" in player or "RWB" in player or "CB" in player:
                    defense.append(player)        
                if "CDM" in player or "CM" in player or "LCM" in player or "RCM" in player or "CAM" in player or "LM" in player or "RM" in player or "RDM" in player or "LDM" in player or "LAM" in player or "RAM" in player:
                    midfield.append(player)
                if "CF" in player or "ST" in player or "LW" in player or "RW" in player or "LS" in player or "RS" in player and "LWB" not in player and "RWB" not in player:
                    forward.append(player)
            
            defense = [i.replace(i.split(",")[1],'') for i in defense]
            defense = [i.replace(",",'') for i in defense]
            midfield = [i.replace(i.split(",")[1],'') for i in midfield]
            midfield = [i.replace(",",'') for i in midfield]
            forward = [i.replace(i.split(",")[1],'') for i in forward]
            forward = [i.replace(",",'') for i in forward]
            
            defenseCombined = list(it.combinations(defense, 4)) #hacemos la combinatoria de todos los jugadores de esa zona y cojemos 4
            defenseCombined = list(set(defenseCombined))
            midfieldCombined = list(it.combinations(midfield, 3)) #3 en este caso
            midfieldCombined = list(set(midfieldCombined))
            forwardCombined = list(it.combinations(forward, 3)) #3 en este caso
            forwardCombined = list(set(forwardCombined))
            
            defense = self.createMainTeamAux2(defenseCombined,positionsDefense,grades,statistics)
            midfield = self.createMainTeamAux2(midfieldCombined,positionsMidfield,grades,statistics)
            forward = self.createMainTeamAux2(forwardCombined,positionsForward,grades,statistics)
            
            mainTeam.extend(defense)
            mainTeam.extend(midfield)
            mainTeam.extend(forward)
            
            return mainTeam
        else:#si no hacemos la combinatoria
            return self.filterTeam(players)
        
    def createMainTeamAux(self,player,grades,statistics):
        overall = 0
        oneGrade = []
        oneStatistics = []
        player = list(player)
        
        if player[0] == "CB" or player[0] == "RCB" or player[0] == "LCB":
            player[0] = "CBaLCBaRCB"
            
        if player[0] == "LB" or player[0] == "LWB" or player[0] == "RB" or player[0] == "RWB":
            player[0] = "LBaLWBaRBaRWB"
            
        if player[0] == "CDM" or player[0] == "LDM" or player[0] == "RDM":
            player[0] = "CDMaLDMaRDM"
        
        if player[0] == "LM"  or player[0] == "LCM" or player[0] == "RM" or player[0] == "RCM":
            player[0] = "LMaLCMaRMaRCM"
        
        if player[0] == "CAM" or player[0] == "LAM" or player[0] == "RAM":
            player[0] = "CAMaLAMaRAM"
        
        if player[0] == "CF" or player[0] == "LS" or player[0] == "RS":
            player[0] = "CFaLSaRS"
            
        if player[0] == "LW" or player[0] == "RW":
            player[0] = "LWaRW"
            
        for i in range(len(grades)):
            if grades[i][0] == player[0]:
                oneGrade = grades[i]
        
        for i in range(len(statistics)):
            if statistics[i][0].split(",")[0] == player[1]:
                oneStatistics = statistics[i]
        
        oneGrade = oneGrade[1:]
        oneGrade = ''.join(oneGrade)
        oneGrade = oneGrade.replace(",","")[1:-1]
        oneGrade = oneGrade.split(" ")
        oneStatistics = oneStatistics[1:]
        oneStatistics = ''.join(oneStatistics)
        oneStatistics = oneStatistics.replace(",","")[1:-1]
        oneStatistics = oneStatistics.split(" ")

        for statistic,grade in zip(oneStatistics,oneGrade):
            overall = overall + (int(statistic)*int(grade))
        
        return overall
    
    def createMainTeamAux2(self,playersGroup,positions,grades,statistics):
        total = 0
        aux = []
        positionsReturn = []
        for players in playersGroup:
            aux.clear()
            combined = [list(zip(x,players)) for x in it.permutations(positions,len(players))]
            for combination in combined:
                for player in combination:
                    points = self.createMainTeamAux(player[:],grades,statistics)
                    aux.append(points)
                if sum(aux) > total:
                    positionsReturn.clear()
                    total = sum(aux)
                    for player in combination:
                        positionsReturn.append(player[1] + ", " + player[0])
        return positionsReturn
    
    def overallCalculation(self,mainTeam):#aquí calculamos los puntos totales de cada jugador en el enfrentamiento
        mainTeamReturn = []
        for player in mainTeam:
    
            if "GK" in player:
                self.overallCalculationAux(mainTeamReturn, "GK", player)

            if "LCB" in player or "RCB" in player or "CB" in player:
                self.overallCalculationAux(mainTeamReturn, "CBaLCBaRCB", player)

            if "LB" in player or "LWB" in player or "RB" in player or "RWB" in player:
                self.overallCalculationAux(mainTeamReturn, "LBaLWBaRBaRWB", player)
            
            if "CDM" in player or "RDM" in player or "LDM" in player:
                self.overallCalculationAux(mainTeamReturn, "CDMaLDMaRDM", player)
        
            if "CM" in player and "LCM" not in player and "RCM" not in player:
                self.overallCalculationAux(mainTeamReturn, "CM", player)
        
            if "LCM" in player or "RCM" in player or "LM" in player or "RM" in player:
                self.overallCalculationAux(mainTeamReturn, "LMaLCMaRMaRCM", player)
    
            if "CAM" in player or "LAM" in player or "RAM" in player:
                self.overallCalculationAux(mainTeamReturn, "CAMaLAMaRAM", player)
                
            if "CF" in player or "LS" in player or "RS" in player:
                self.overallCalculationAux(mainTeamReturn, "CFaLSaRS", player)
                
            if "ST" in player:
                self.overallCalculationAux(mainTeamReturn, "ST", player)
                    
            if "LW" in player or "RW" in player and "LWB" not in player and "RWB" not in player:
                self.overallCalculationAux(mainTeamReturn, "LWaRW", player)
            
        return mainTeamReturn
    
    def overallCalculationAux(self,mainTeamReturn,pid,player):
        statistics = grades = overall = 0
        
        if pid == "GK": #Si es portero tenemos que buscar en otras estadísticas
            statistics = self.conexion.query("MATCH (p:Player) WHERE p.name='{player1}' RETURN  p.height_cm,p.gkDiving,p.gkHandling,p.gkKicking,p.gkReflexes,p.gkSpeed,p.gkPositioning,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityComposure,p.mentalityVision,p.attackingVolleys,p.movementAgility,p.movementReactions,p.mentalityInterceptions".format(player1=player.split(",")[0]))
            grades = self.conexion.query("MATCH (p:Position) WHERE p.id='GK' RETURN p.height_cm,p.gkDiving,p.gkHandling,p.gkKicking,p.gkReflexes,p.gkSpeed,p.gkPositioning,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityComposure,p.mentalityVision,p.attackingVolleys,p.movementAgility,p.movementReactions,p.mentalityInterceptions")
        else:
            statistics = self.conexion.query("MATCH (p:Player) WHERE p.name='{player1}' RETURN  p.shooting,p.dribbling,p.defending,p.attackingCrossing,p.attackingFinishing,p.attackingHeadingAccuracy,p.attackingShortPassing,p.attackingVolleys,p.skillLongPassing,p.skillBallControl,p.movementAcceleration,p.movementSprintSpeed,p.movementAgility,p.movementReactions,p.movementBalance,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityInterceptions,p.mentalityVision,p.mentalityComposure,p.defendingMarking,p.defendingSlidingTackle,p.defendingStandingTackle".format(player1=player.split(",")[0]))
            grades = self.conexion.query("MATCH (p:Position) WHERE p.id='{pid1}' RETURN p.shooting,p.dribbling,p.defending,p.attackingCrossing,p.attackingFinishing,p.attackingHeadingAccuracy,p.attackingShortPassing,p.attackingVolleys,p.skillLongPassing,p.skillBallControl,p.movementAcceleration,p.movementSprintSpeed,p.movementAgility,p.movementReactions,p.movementBalance,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityInterceptions,p.mentalityVision,p.mentalityComposure,p.defendingMarking,p.defendingSlidingTackle,p.defendingStandingTackle".format(pid1=pid))
        
        statistics = statistics[0].replace(",","")[1:-1]
        statistics = statistics.split(" ")
        grades = grades[0].replace(",","")[1:-1]
        grades = grades.split(" ")
        
        for statistic,grade in zip(statistics,grades):
            if "." in statistic: 
                if float(statistic) > 180 and float(statistic) < 190:
                    overall = overall + int(float(statistic))*int(float(grade))
            else:
                overall = overall + (int(statistic)*int(grade))
        
        if pid == "GK":
            overall = int(overall * 1.7) #sumamos arbitrariamente puntuación para que se iguale la puntuación a la de los compañeros
        mainTeamReturn.append(player +"," + str(overall))
                        
    def overallMainTeam(self):#calculamos la puntuación total del equipo
        points1 = points2 = 0
        for player1,player2 in zip(self.mainTeam1,self.mainTeam2):
            points1 = points1 + int(player1.split(",")[2])
            points2 = points2 + int(player2.split(",")[2])
        return points1,points2
                
    def pointsOverallZone(self,mainTeam):#calculamos la puntuación total de cada zona
        zoneDefense = []
        zoneMidfield = []
        zoneForward = []
        pointsDefense =  pointsMidfield = pointsForward = 0
        
        for player in mainTeam:
            if "GK" in player or "LB" in player or "LWB" in player or "LCB" in player or "RCB" in player or "RB" in player or "RWB" in player or "CB" in player:
                pointsDefense = pointsDefense + int(player.split(",")[2])
                zoneDefense.append(player)        
            if "CDM" in player or "CM" in player or "LCM" in player or "RCM" in player or "CAM" in player or "LM" in player or "RM" in player or "RDM" in player or "LDM" in player or "LAM" in player or "RAM" in player:
                pointsMidfield = pointsMidfield + int(player.split(",")[2])
                zoneMidfield.append(player)
            if "CF" in player or "ST" in player or "LW" in player or "RW" in player or "LS" in player or "RS" in player and "LWB" not in player and "RWB" not in player:
                pointsForward = pointsForward + int(player.split(",")[2])
                zoneForward.append(player)
        
        zoneDefense.append(pointsDefense)
        zoneMidfield.append(pointsMidfield)
        zoneForward.append(pointsForward)
        
        return zoneDefense,zoneMidfield,zoneForward
    
    def pointsAttackVSDefense(self,pointsOverallDefense1,pointsOverallMidfield1, pointsOverallForward1,pointsOverallDefense2,pointsOverallMidfield2, pointsOverallForward2):#calculamos los puntos de ataque y defensa
        
        pointsAttack1 = (pointsOverallMidfield1[-1]/2 + pointsOverallForward1[-1]) #/2 para que el centro del campo valga menos
        pointsDefense1 = (pointsOverallMidfield1[-1]/2 + pointsOverallDefense1[-1])
        pointsAttack2 = (pointsOverallMidfield2[-1]/2 + pointsOverallForward2[-1])
        pointsDefense2 = (pointsOverallMidfield2[-1]/2 + pointsOverallDefense2[-1])

        return pointsAttack1,pointsDefense1,pointsAttack2,pointsDefense2
    
    def pointsPlayerVSPlayer(self,mainTeam1,mainTeam2): #comparamos posición por posición
        pointsVS1 = pointsVS2 = 0
        listaAux1 = []
        listaAux2 = []
       
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
                    if int(player1.split(",")[2]) > int(player2.split(",")[2]):
                        pointsVS1 = pointsVS1 + int(player1.split(",")[2]) - int(player2.split(",")[2])
                    elif int(player1.split(",")[2]) < int(player2.split(",")[2]):
                        pointsVS2 = pointsVS2 + int(player2.split(",")[2]) - int(player1.split(",")[2])
                        
                    listaAux1.append(player1)
                    listaAux2.append(player2)
                    break
        
        return pointsVS1,pointsVS2
    

    def checkUnbalance(self,team):#esta función comprueba si el equipo esta demasiado desequilibrado, tanto para bien como para mal
            pointsPlayers = []
            bonusDefense = bonusMidfield = bonusForward = 0
            
            for player in team:
                pointsPlayers.append(int(player.split(",")[2]))
            
            #usamos la regla de las tres sigmas o regla 68-95-99.7
            mu = st.mean(pointsPlayers) #la media
            sigma = st.stdev(pointsPlayers) #la desviación típica
            
            if st.stdev(pointsPlayers) > 10000: # si la desviación típica es alta es que está muy dispersados los datos, entonces los tratamos (normalmente será cuando hay suplentes)
                for points,player in zip(pointsPlayers,team):
                    if points < mu-sigma:#si el jugador destaca para mal
                        if "GK" in player or "LB" in player or "LWB" in player or "LCB" in player or "RCB" in player or "RB" in player or "RWB" in player or "CB" in player:
                            bonusDefense = bonusDefense - 9.09 #el 9.09 sería el porcentaje, lo que representaría proporcionalmente un jugador sobre el 100%
                        if "CDM" in player or "CM" in player or "LCM" in player or "RCM" in player or "CAM" in player or "LM" in player or "RM" in player or "RDM" in player or "LDM" in player or "LAM" in player or "RAM" in player:
                            bonusMidfield = bonusMidfield - 9.09
                        if "CF" in player or "ST" in player or "LW" in player or "RW" in player or "LS" in player or "RS" in player and "LWB" not in player and "RWB" not in player:
                            bonusForward = bonusForward - 9.09
                            
                    if points > mu+sigma:#si el jugador destaca para bien
                        if "GK" in player or "LB" in player or "LWB" in player or "LCB" in player or "RCB" in player or "RB" in player or "RWB" in player or "CB" in player:
                            bonusDefense = bonusDefense + 9.09
                        if "CDM" in player or "CM" in player or "LCM" in player or "RCM" in player or "CAM" in player or "LM" in player or "RM" in player or "RDM" in player or "LDM" in player or "LAM" in player or "RAM" in player:
                            bonusMidfield = bonusMidfield + 9.09
                        if "CF" in player or "ST" in player or "LW" in player or "RW" in player or "LS" in player or "RS" in player and "LWB" not in player and "RWB" not in player:
                            bonusForward = bonusForward + 9.09
                    
                return bonusDefense, bonusMidfield, bonusForward
            else:
                return 0,0,0
    
    def filterTeam(self,players):#esta función sirve para quitar los suplentes y reservas
        mainTeam = []
        
        for player in players:
            if "SUB" not in player and "RES" not in player:
                mainTeam.append(player)
                
        return mainTeam
    
    def dataCache(self,players):#esta función sirve para cachear algunos datos de la base de datos y aliviar de consultas a la misma
        #aquí cacheamos las posiciones
        positions = [["CBaLCBaRCB"],
                     ["LBaLWBaRBaRWB"],
                     ["CDMaLDMaRDM"],
                     ["CM"],
                     ["LMaLCMaRMaRCM"],
                     ["CAMaLAMaRAM"],
                     ["CFaLSaRS"],
                     ["ST"],
                     ["LWaRW"]]
        
        for i in range(len(positions)):
            query = self.conexion.query("MATCH (p:Position) WHERE p.id='{pid}' RETURN p.shooting,p.dribbling,p.defending,p.attackingCrossing,p.attackingFinishing,p.attackingHeadingAccuracy,p.attackingShortPassing,p.attackingVolleys,p.skillLongPassing,p.skillBallControl,p.movementAcceleration,p.movementSprintSpeed,p.movementAgility,p.movementReactions,p.movementBalance,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityInterceptions,p.mentalityVision,p.mentalityComposure,p.defendingMarking,p.defendingSlidingTackle,p.defendingStandingTackle".format(pid=positions[i][0]))
            positions[i].extend(query)
        
        #aquí cacheamos los puntos de los jugadores
        players = np.array([players]).T.tolist()

        for i in range(len(players)):
            query = self.conexion.query("MATCH (p:Player) WHERE p.name='{player}' RETURN  p.shooting,p.dribbling,p.defending,p.attackingCrossing,p.attackingFinishing,p.attackingHeadingAccuracy,p.attackingShortPassing,p.attackingVolleys,p.skillLongPassing,p.skillBallControl,p.movementAcceleration,p.movementSprintSpeed,p.movementAgility,p.movementReactions,p.movementBalance,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityInterceptions,p.mentalityVision,p.mentalityComposure,p.defendingMarking,p.defendingSlidingTackle,p.defendingStandingTackle".format(player=players[i][0].split(",")[0]))
            players[i].extend(query)
            
        return positions,players
