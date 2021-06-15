#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
        
        if self.combinatoricsTeam2:#si usamos combinatoria en el equipo 2 llamamos al método para que cree el equipo pero si no, no llamamos porque ya esta echo el equipo
            self.mainTeam2 = self.createMainTeam(self.mainTeam2,self.team2,self.combinatoricsTeam2)
        
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
            
            pointsVSPlayers1,pointsVSPlayer2 = self.pointsPlayerVSPlayer(self.mainTeam1[:],self.mainTeam2[:])#[:] es para pasarle una copia ya que las dos listas se modifican dentro de la función y afectaría a esas mismas lista fuera de ella
            pointsOverallMainTeam1,pointsOverallMainTeam2 = self.overallMainTeam()
            pointsOverallDefense1,pointsOverallMidfield1, pointsOverallForward1 = self.pointsOverallZone(self.mainTeam1)
            pointsOverallDefense2,pointsOverallMidfield2, pointsOverallForward2 = self.pointsOverallZone(self.mainTeam2)
            
            pointsOverallDefense1[-1] = pointsOverallDefense1[-1] + (pointsOverallDefense1[-1]*bonusDefense1/100) #para estas puntuaciones le sumamos las bonificaciones aquí en vez de en la escritura del fichero, así vamos arrastrando los cambios a otros datos
            pointsOverallDefense2[-1] = pointsOverallDefense2[-1] + (pointsOverallDefense2[-1]*bonusDefense2/100)
            pointsOverallMidfield1[-1] = pointsOverallMidfield1[-1] + (pointsOverallMidfield1[-1]*bonusMidfield1/100)
            pointsOverallMidfield2[-1] = pointsOverallMidfield2[-1] + (pointsOverallMidfield2[-1]*bonusMidfield2/100)
            pointsOverallForward1[-1] = pointsOverallForward1[-1]+ (pointsOverallForward1[-1]*bonusForward1/100)
            pointsOverallForward2[-1] = pointsOverallForward2[-1] + (pointsOverallForward2[-1]*bonusForward2/100)
            
            pointsAttack1,pointsDefense1,pointsAttack2,pointsDefense2 = self.pointsAttackVSDefense(pointsOverallDefense1,pointsOverallMidfield1, pointsOverallForward1,pointsOverallDefense2,pointsOverallMidfield2, pointsOverallForward2)
            
            
            file = open("settings.conf", "w") #abre un archivo de texto, lo crea si no existe y vamos escribiendo todos los datos que hemos recogido
            #sumamos aquí los bonos
            self.fileWrite(file,self.mainTeam1)
            self.fileWrite(file,self.mainTeam2)
            self.fileWrite(file,pointsVSPlayers1)
            self.fileWrite(file,pointsVSPlayer2)
            self.fileWrite(file,pointsOverallMainTeam1 + (pointsOverallMainTeam1*bonusDefense1/100) + (pointsOverallMainTeam1*bonusMidfield1/100) + (pointsOverallMainTeam1*bonusForward1/100))#lo que esta entre paréntesis es el porcentaje que sumamos
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
        if isinstance(listOrInt, int) or isinstance(listOrInt, float) or isinstance(listOrInt, str):# si es int, float o cadena entra aquí si no será una lista
            file.write("{}\n".format(listOrInt))
        else:#añadimos cada list o int a una nueva linea del archivo
            for item in listOrInt:
                file.write("%s;" % item)
            file.write("\n")  
    
    def createMainTeam(self,mainTeam,team,combinatorics):#modificar para que en realidad el equipo 1 coja el equipo de manera mas conveniente
        #aux = [] #para meter los jugadores y posiciones junto a su puntuación total
        defense = []
        midfield = []
        forward = []
        defenseCombined = [] #estas listas almacenan las combinaciones de jugadores, es decir jugador a con b, a con c, b con c,etc
        midfieldCombined = []
        forwardCombined = []
        combined = []
        grades = []
        statistics = []
        positionsDefense = ["LB","LWB","LCB","RCB","RB","RWB","CB"]
        positionsMidfield = ["CDM","CM","LCM","RCM","CAM","LM","RM","RDM","LDM","LAM","RAM"]
        positionsForward = ["CF","ST","LW","RW","LS","RS"]
        
        players = self.conexion.query("MATCH (p)-[r:PLAYS]->(c) WHERE c.id='{}' RETURN DISTINCT p.name,r.teamPosition".format(team)) #obtenemos todos los jugadores y sus correspondientes posiciones en los equipos
        players = [player.replace("'","") for player in players] #limpiamos de comillas la lista de strings,corchetes y espacios
        players = [player[1:-1] for player in players]
        
        if combinatorics:
            grades,statistics = self.dataCache(players)
        
            #Para elegir el equipo: el portero será el titular, con 4 defensas, 3 centrocanpistas y 3 delanteros
            #Recorremos con un for los jugadores
            for player in players:
                if player.split(",")[1] == " GK": #Si es portero titular lo añadimos sin mas
                    mainTeam.append(player)
                #El resto de jugadores los metemos en una lista según sea defensa,medio o ataque
                if "LB" in player or "LWB" in player or "LCB" in player or "RCB" in player or "RB" in player or "RWB" in player or "CB" in player:
                    defense.append(player)        
                if "CDM" in player or "CM" in player or "LCM" in player or "RCM" in player or "CAM" in player or "LM" in player or "RM" in player or "RDM" in player or "LDM" in player or "LAM" in player or "RAM" in player:
                    midfield.append(player)
                if "CF" in player or "ST" in player or "LW" in player or "RW" in player or "LS" in player or "RS" in player and "LWB" not in player and "RWB" not in player:#los not in son para evitar que algunos jugadores entren en más de un if(porque coincide el término de búsqueda)
                    forward.append(player)
            
            defense = [i.replace(i.split(",")[1],'') for i in defense] #quitamos la posición de los jugadores ya que ya sabemos si son defensa,medio, o ataque
            defense = [i.replace(",",'') for i in defense] #quitamos la coma del final de los nombres
            midfield = [i.replace(i.split(",")[1],'') for i in midfield]
            midfield = [i.replace(",",'') for i in midfield]
            forward = [i.replace(i.split(",")[1],'') for i in forward]
            forward = [i.replace(",",'') for i in forward]
            
            #Primero hacemos combinatoria de los jugadores
            defenseCombined = list(it.combinations(defense, 4)) #hacemos la combinatoria de todos los jugadores de esa zona y cojemos 4
            defenseCombined = list(set(defenseCombined)) #quitamos los repetidos si los hubiera convirtiendo a set y lo convertimos otra vez a lista
            midfieldCombined = list(it.combinations(midfield, 3))
            midfieldCombined = list(set(midfieldCombined))
            forwardCombined = list(it.combinations(forward, 3))
            forwardCombined = list(set(forwardCombined))
            
            #ahora recorremos la lista anteriores para probar las puntuaciones
            defense = self.createMainTeamAux2(defenseCombined,positionsDefense,grades,statistics)
            midfield = self.createMainTeamAux2(midfieldCombined,positionsMidfield,grades,statistics)
            forward = self.createMainTeamAux2(forwardCombined,positionsForward,grades,statistics)
            
            mainTeam.extend(defense)
            mainTeam.extend(midfield)
            mainTeam.extend(forward)
            
            return mainTeam
        else:#si no hacemos la combinatoria, simplemente quitamos los suplentes y devolvemos
            return self.filterTeam(players) #en caso de que no quiera hacer la combinatoria y facer el equipo sin más, descomentar esta línea y comentar lo que hay quedabo y en la línea de justo más arriba
    def createMainTeamAux(self,player,grades,statistics):#le pasamos la lista, el jugador de la base de datos
        overall = 0
        oneGrade = []
        oneStatistics = []
        player = list(player) #convertimos la tupla a lista para que sea editable
        #hacemos los cambios pertinentes para adaptarlos a la base de datos(CM,ST y GK no hace falta)
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
            
        for i in range(len(grades)):#obtenemos la lista correcta de notas de la posición indicada
            if grades[i][0] == player[0]:
                oneGrade = grades[i]
        
        for i in range(len(statistics)):#obtenemos la lista correcta de la estadística del jugador
            if statistics[i][0].split(",")[0] == player[1]: #comparamos si tiene el mismo nombre
                oneStatistics = statistics[i]
        
        oneGrade = oneGrade[1:] #quitamos el primer elemento que incluye la posición
        oneGrade = ''.join(oneGrade) #convertimos a string
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
            combined = [list(zip(x,players)) for x in it.permutations(positions,len(players))] #ahora hacemos combinatoria de cada grupo de jugadores que obtenemos con las posiciones posibles
            for combination in combined:
                for player in combination:#para cada combinación de jugadores y posiciones tenemos que calcular la puntuación
                    points = self.createMainTeamAux(player[:],grades,statistics) #importante!, le enviamos una copia
                    aux.append(points) #metemos en una lista auxiliar
                if sum(aux) > total: #si la suma de todas las puntuaciones es mayor que el total, guardamos el total y la lista
                    positionsReturn.clear()
                    total = sum(aux)
                    for player in combination:
                        positionsReturn.append(player[1] + ", " + player[0])
        return positionsReturn
    
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
        
            if "CM" in player and "LCM" not in player and "RCM" not in player:#los not in son para evitar que algunos jugadores entren en mas de un if(porque coincide el término de búsqueda)
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
            overall = int(overall * 1.7) #aprovechamos para sumarle artificialmente puntuación para que se iguale la puntuación a la de los compañeros
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
            if "CF" in player or "ST" in player or "LW" in player or "RW" in player or "LS" in player or "RS" in player and "LWB" not in player and "RWB" not in player:#los not in son para evitar que algunos jugadores entren en mas de un if(porque coincide el término de búsqueda)
                pointsForward = pointsForward + int(player.split(",")[2])
                zoneForward.append(player)
        
        zoneDefense.append(pointsDefense) #añadimos la puntuación a la propia lista
        zoneMidfield.append(pointsMidfield)
        zoneForward.append(pointsForward)
        
        return zoneDefense,zoneMidfield,zoneForward
    
    def pointsAttackVSDefense(self,pointsOverallDefense1,pointsOverallMidfield1, pointsOverallForward1,pointsOverallDefense2,pointsOverallMidfield2, pointsOverallForward2):
        
        pointsAttack1 = (pointsOverallMidfield1[-1]/2 + pointsOverallForward1[-1]) #/2 para que el centro del campo valga menos
        pointsDefense1 = (pointsOverallMidfield1[-1]/2 + pointsOverallDefense1[-1])
        pointsAttack2 = (pointsOverallMidfield2[-1]/2 + pointsOverallForward2[-1])
        pointsDefense2 = (pointsOverallMidfield2[-1]/2 + pointsOverallDefense2[-1])

        return pointsAttack1,pointsDefense1,pointsAttack2,pointsDefense2
    
    def pointsPlayerVSPlayer(self,mainTeam1,mainTeam2): #comparamos posición por posición y se restan, el que tenga mas puntos se lleva la diferencia para el equipo, si no existe la posición cuenta como si fuera cero
        pointsVS1 = pointsVS2 = 0
        listaAux1 = [] #usada para saber cuales posiciones no coinciden
        listaAux2 = [] #no cambiar a listaAux1 = listaAux2 si no no funcionará
       
        for player1 in self.mainTeam1:
            for player2 in self.mainTeam2:
                if "-" in player1.split(",")[1]:#si hay un "-" es que es suplente, entonces separamos la posición de manera diferente pero aseguramos que se compare
                    position1 = player1.split(",")[1].split("-")[1]
                else:#no es suplente
                    position1 = player1.split(",")[1].replace(" ","") #quitamos el espacio del principio
                if "-" in player2.split(",")[1]:# el split no haría falta si no fuera por que hay jugadores que tienen guiones en el nombre -.-
                    position2 = player2.split(",")[1].split("-")[1]
                else:
                    position2 = player2.split(",")[1].replace(" ","") #quitamos el espacio del principio
                
                if position1 == position2: #si son las mismas posiciones
                    if int(player1.split(",")[2]) > int(player2.split(",")[2]):
                        pointsVS1 = pointsVS1 + int(player1.split(",")[2]) - int(player2.split(",")[2])#restamos los puntos de cada posición y lo sumamos al total del que ha ganado
                    elif int(player1.split(",")[2]) < int(player2.split(",")[2]):#el elif es necesario ya que si por casualidad tiene la misma puntuación en el caso de que haya un else, entraría aquí también
                        pointsVS2 = pointsVS2 + int(player2.split(",")[2]) - int(player1.split(",")[2])
                        
                    listaAux1.append(player1)
                    listaAux2.append(player2)
                    break #para que no siga en el bucle interior buscando ya que lo ha encontrado si esta aquí
        """De momento lo quitamos porque  creo que es mas justo asi
        for player1 in listaAux1:
            if player1 in mainTeam1:#vamos quitando los jugadores comparados
                mainTeam1.remove(player1)
        
        for player2 in listaAux2:
            if player2 in mainTeam2:#vamos quitando los jugadores comparados
                mainTeam2.remove(player2)

        
        #Si hay posiciones que no se repiten en los equipos, añadimos a los puntos totales de los jugadores
        for player1 in mainTeam1:
            pointsVS1 = pointsVS1 + int(player1.split(",")[2])
        for player2 in mainTeam2:
            pointsVS2 = pointsVS2 + int(player2.split(",")[2])
        """    
        return pointsVS1,pointsVS2
    

    def checkUnbalance(self,team):#esta función comprueba si el equipo esta demasiado desequilibrado, tanto para bien como para mal(no funciona del todo bien pero es bastante complicada de arreglar)
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
    
    def filterTeam(self,players):#borrar cuando no la necesite
        mainTeam = []
        
        for player in players:
            if "SUB" not in player and "RES" not in player:#Si no es un suplente o vacio lo añadimos a la lista de titulares
                mainTeam.append(player)
                
        return mainTeam
    
    def dataCache(self,players):#esta función sirve para cachear algunos datos de la base de datos y aliviar de consultas a la misma
        #aquí cacheamos las posiciones
        positions = [["CBaLCBaRCB"], #hacemos una matriz para meter los datos de forma
                     ["LBaLWBaRBaRWB"],
                     ["CDMaLDMaRDM"],
                     ["CM"],
                     ["LMaLCMaRMaRCM"],
                     ["CAMaLAMaRAM"],
                     ["CFaLSaRS"],
                     ["ST"],
                     ["LWaRW"]] #el portero no lo necesitamos
        
        for i in range(len(positions)):
            query = self.conexion.query("MATCH (p:Position) WHERE p.id='{pid}' RETURN p.shooting,p.dribbling,p.defending,p.attackingCrossing,p.attackingFinishing,p.attackingHeadingAccuracy,p.attackingShortPassing,p.attackingVolleys,p.skillLongPassing,p.skillBallControl,p.movementAcceleration,p.movementSprintSpeed,p.movementAgility,p.movementReactions,p.movementBalance,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityInterceptions,p.mentalityVision,p.mentalityComposure,p.defendingMarking,p.defendingSlidingTackle,p.defendingStandingTackle".format(pid=positions[i][0]))
            positions[i].extend(query)
        
        #aquí cacheamos los puntos de los jugadores
        players = np.array([players]).T.tolist() #convertimos la lista en una matriz vertical

        for i in range(len(players)):
            query = self.conexion.query("MATCH (p:Player) WHERE p.name='{player}' RETURN  p.shooting,p.dribbling,p.defending,p.attackingCrossing,p.attackingFinishing,p.attackingHeadingAccuracy,p.attackingShortPassing,p.attackingVolleys,p.skillLongPassing,p.skillBallControl,p.movementAcceleration,p.movementSprintSpeed,p.movementAgility,p.movementReactions,p.movementBalance,p.powerShotPower,p.powerJumping,p.powerStamina,p.mentalityInterceptions,p.mentalityVision,p.mentalityComposure,p.defendingMarking,p.defendingSlidingTackle,p.defendingStandingTackle".format(player=players[i][0].split(",")[0]))
            players[i].extend(query)
            
        return positions,players
