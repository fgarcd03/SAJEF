#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import statistics as st

class Estimate:
    
    def __init__(self,conexion,team1,team2,mainTeam2):
        self.conexion = conexion
        self.team1 = team1
        self.team2 = team2
        self.mainTeam2 = mainTeam2
        
        self.createMainTeam1()#El equipo 2 no creamos mainTeam porque ya lo hace el usuario

        self.mainTeam1 = self.overallCalculation(self.mainTeam1)
        self.mainTeam2 = self.overallCalculation(self.mainTeam2)
        
        if len(self.mainTeam1) != 11 or len(self.mainTeam2) != 11:

            print("Error, tamaño de equipo incorrecto")
            print("Tamaño de equipo 1: " + str(len(self.mainTeam1)))
            print("Tamaño de equipo 2: " + str(len(self.mainTeam2)))
        else:
            #Hacer todo lo demás
            bonusDefense1, bonusMidfield1, bonusForward1 = self.checkUnbalance(self.mainTeam1)
            bonusDefense2, bonusMidfield2, bonusForward2 = self.checkUnbalance(self.mainTeam2)
            bonusDefense2 = bonusMidfield2 = bonusForward2 = 0 #lo pongo a cero de momento para que no influya
            pointsVSPlayers1,pointsVSPlayer2 = self.pointsPlayerVSPlayer(self.mainTeam1[:],self.mainTeam2[:])#[:] es para pasarle una copia ya que las dos listas se modifican dentro de la función y afectaria a esas mismas lista fuera de ella
            pointsOverallMainTeam1,pointsOverallMainTeam2 = self.overallMainTeam()
            pointsOverallDefense1,pointsOverallMidfield1, pointsOverallForward1 = self.pointsOverallZone(self.mainTeam1)
            pointsOverallDefense2,pointsOverallMidfield2, pointsOverallForward2 = self.pointsOverallZone(self.mainTeam2)
            pointsAttack1,pointsDefense1,pointsAttack2,pointsDefense2 = self.pointsAttackVSDefense(pointsOverallDefense1,pointsOverallMidfield1, pointsOverallForward1,pointsOverallDefense2,pointsOverallMidfield2, pointsOverallForward2)
            
            
            
            file = open("settings.txt", "w") #abre un archivo de texto, lo crea si no existe y vamos escribiendo todos los datos que hemos recogido
            #sumamos aquí los bonos
            self.fileWrite(file,self.mainTeam1)
            self.fileWrite(file,self.mainTeam2)
            self.fileWrite(file,pointsVSPlayers1)
            self.fileWrite(file,pointsVSPlayer2)
            self.fileWrite(file,pointsOverallMainTeam1 + (pointsOverallMainTeam1*bonusDefense1/100) + (pointsOverallMainTeam1*bonusMidfield1/100) + (pointsOverallMainTeam1*bonusForward1/100))#lo que esta entre paréntesis es el porcentaje que sumamos
            self.fileWrite(file,pointsOverallMainTeam2 + (pointsOverallMainTeam2*bonusDefense2/100) + (pointsOverallMainTeam2*bonusMidfield2/100) + (pointsOverallMainTeam2*bonusForward2/100))
            self.fileWrite(file,pointsOverallDefense1[-1] + (pointsOverallDefense1[-1]*bonusDefense1/100))
            self.fileWrite(file,pointsOverallDefense2[-1] + (pointsOverallDefense2[-1]*bonusDefense2/100))
            self.fileWrite(file,pointsOverallMidfield1[-1] + (pointsOverallMidfield1[-1]*bonusMidfield1/100))
            self.fileWrite(file,pointsOverallMidfield2[-1] + (pointsOverallMidfield2[-1]*bonusMidfield2/100))
            self.fileWrite(file,pointsOverallForward1[-1]+ (pointsOverallForward1[-1]*bonusForward1/100))
            self.fileWrite(file,pointsOverallForward2[-1] + (pointsOverallForward2[-1]*bonusForward2/100))
            self.fileWrite(file,pointsAttack1 + (pointsAttack1*bonusMidfield1/100) + (pointsAttack1*bonusForward1/100))
            self.fileWrite(file,pointsAttack2 + (pointsAttack2*bonusMidfield2/100) + (pointsAttack2*bonusForward2/100))
            self.fileWrite(file,pointsDefense1 + (pointsDefense1*bonusDefense1/100) + (pointsDefense1*bonusMidfield1/100))
            self.fileWrite(file,pointsDefense2 + (pointsDefense2*bonusDefense2/100) + (pointsDefense2*bonusMidfield2/100))
            self.fileWrite(file,team1)
            self.fileWrite(file,team2)

            file.close()
            
            os.system("python3 ResultsWindow.py &")

    def fileWrite(self,file,listOrInt):
        if isinstance(listOrInt, int) or isinstance(listOrInt, float) or isinstance(listOrInt, str):# si es int, float o cadena entra aquí si no será una lista
            file.write("{}\n".format(listOrInt))
        else:#añadimos cada list o int a una nueva linea del archivo
            for item in listOrInt:
                file.write("%s;" % item)
            file.write("\n")  
            
    def createMainTeam1(self):#modificar para que en realidad el equipo 1 coja el equipo de manera mas conveniente
        players1 = self.conexion.query("MATCH (p)-[r:PLAYS]->(c) WHERE c.id='{team}' RETURN DISTINCT p.name,r.teamPosition".format(team=self.team1)) #obtenemos todos los jugadores y sus correspondientes posiciones en los equipos
        players1 = [player.replace("'","") for player in players1] #limpiamos de comillas la lista de strings,corchetes y espacios
        players1 = [player[1:-1] for player in players1]

        self.mainTeam1 = self.filterTeam(players1)

        
    def overallCalculation(self,mainTeam):#aquí calculamos los puntos totales de cada jugador en el enfrentamiento
        mainTeamReturn = [] #hacemos una nueva lista para meter los jugadores con el overall
        for player in mainTeam:
    
            if "GK" in player:
                self.overallCalculationAux(mainTeamReturn, "GK", player)

            if "LCB" in player or "RCB" in player or "CB" in player:
                self.overallCalculationAux(mainTeamReturn, "CBaLCBaRCB", player)

            if "LB" in player or "LWB" in player or "RB" in player or "RWB" in player:
                self.overallCalculationAux(mainTeamReturn, "LBaLWBaRBaRWB", player)
            
            if "CDM" in player or "RDM" in player or "LDM" in player:
                self.overallCalculationAux(mainTeamReturn, "CDMaLDMaRDM", player)
        
            if "CM" in player and "LCM" not in player and "RCM" not in player:#los not in son para evitar que algunos jugadores entrer en mas de un if(porque coincide el término de bésqueda)
                self.overallCalculationAux(mainTeamReturn, "CM", player)
        
            if "LCM" in player or "RCM" in player or "LM" in player or "RM" in player:
                self.overallCalculationAux(mainTeamReturn, "LMaLCMaRMaRCM", player)
    
            if "CAM" in player or "LAM" in player or "RAM" in player:
                self.overallCalculationAux(mainTeamReturn, "CAMaLAMaRAM", player)
                
            if "CF" in player or "LS" in player or "RS" in player:
                self.overallCalculationAux(mainTeamReturn, "CFaLSaRS", player)
                
            if "ST" in player:
                self.overallCalculationAux(mainTeamReturn, "ST", player)
                    
            if "LW" in player or "RW" in player and "LWB" not in player and "RWB" not in player:#los not in son para evitar que algunos jugadores entrer en mas de un if(porque coincide el término de bésqueda)
                self.overallCalculationAux(mainTeamReturn, "LWaRW", player)
            
        return mainTeamReturn
    
    def overallCalculationAux(self,mainTeamReturn,pid,player):#le pasamos la lista,p.id de la base de datos y el jugador de la base de datos
        statistics = grades = overall = 0
        
        if pid == "GK": #Si es portero tenemos que buscar de otras estadísticas
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
            if "." in statistic:#si existe un . en el string de la estadistica es que es float y es que estamos en la altura del portero y hay que tenerla en cuenta aparte   
                if float(statistic) > 180 and float(statistic) < 190:#si está mide entre 180 y 190 contamos la altura para la estadística
                    overall = overall + int(float(statistic))*int(float(grade))
            else:
                overall = overall + (int(statistic)*int(grade))
        
        if pid == "GK":
            overall = int(overall * 1.7) #aprovechamos para sumarle artificalmente puntuación para que se iguale la puntuación a la de los compañeros
        mainTeamReturn.append(player +"," + str(overall))
        #no hace falta devolver la lista porque no se pasa como copia
                        
    def overallMainTeam(self):
        points1 = points2 = 0
        for player1,player2 in zip(self.mainTeam1,self.mainTeam2):
            points1 = points1 + int(player1.split(",")[2])
            points2 = points2 + int(player2.split(",")[2])
        return points1,points2
                
    def pointsOverallZone(self,mainTeam):
        zoneDefense = []
        zoneMidfield = []
        zoneForward = [] #en la lista se almacena de cada zona la puntuacion de cada zona total junto a los jugadores
        pointsDefense =  pointsMidfield = pointsForward = 0
        
        for player in mainTeam:
            if "GK" in player or "LB" in player or "LWB" in player or "LCB" in player or "RCB" in player or "RB" in player or "RWB" in player or "CB" in player:
                pointsDefense = pointsDefense + int(player.split(",")[2])
                zoneDefense.append(player)        
            if "CDM" in player or "CM" in player or "LCM" in player or "RCM" in player or "CAM" in player or "LM" in player or "RM" in player or "RDM" in player or "LDM" in player or "LAM" in player or "RAM" in player:
                pointsMidfield = pointsMidfield + int(player.split(",")[2])
                zoneMidfield.append(player)
            if "CF" in player or "ST" in player or "LW" in player or "RW" in player or "LS" in player or "RS" in player and "LWB" not in player and "RWB" not in player:#los not in son para evitar que algunos jugadores entrer en mas de un if(porque coincide el término de bésqueda)
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
    

    def checkUnbalance(self,team):#esta función comprueba si el equipo esta demasiado desequilibrado, tanto para bien como para mal
            pointsPlayers = []
            bonusDefense = bonusMidfield = bonusForward = 0
            
            for player in team:#sacamos los puntos de los jugadores
                pointsPlayers.append(int(player.split(",")[2]))
            
            #usamos la regla de las tres sigmas o regla 68-95-99.7
            mu = st.mean(pointsPlayers) #la media
            sigma = st.stdev(pointsPlayers) #la desviación típica
            
            if st.stdev(pointsPlayers) > 10000: # si la desviación típica es alta es que está muy dispersados los datos, entonces los tratamos (normalmente sera cuando hay suplentes)
                for points,player in zip(pointsPlayers,team):#recorremos las dos listas a la vez
                    if points < mu-sigma:# si el jugador destaca para mal
                        if "GK" in player or "LB" in player or "LWB" in player or "LCB" in player or "RCB" in player or "RB" in player or "RWB" in player or "CB" in player:
                            bonusDefense = bonusDefense - 9.09 #el 9.09 sería el porcertanje, lo que representaría proporcionalmente un jugador sobre el 100%
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
    
    def filterTeam(self,players):#borrar cuando no la necesite
        mainTeam = []
        
        for player in players:
            if "SUB" not in player and "RES" not in player:#Si no es un suplente o vacio lo añadimos a la lista de titulares
                mainTeam.append(player)
                
        return mainTeam
    
