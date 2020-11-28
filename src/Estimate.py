#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Estimate:
    
    def __init__(self,conexion,team1,team2):
        self.conexion = conexion
        self.team1 = team1
        self.team2 = team2

        
        mainTeam1,mainTeam2 = self.createMainTeam(self.conexion,self.team1,self.team2)
        self.overallCalculation(mainTeam1,mainTeam2)
        
    def createMainTeam(self,conexion,team1,team2):#Táctica 4-3-3
        players1 = conexion.query("MATCH (p)-[r:PLAYS]->(c) WHERE c.id='{team}' RETURN DISTINCT p.name,r.teamPosition".format(team=team1)) #obtenemos todos los jugadores y sus correspondientes posiciones en los equipos
        players2 = conexion.query("MATCH (p)-[r:PLAYS]->(c) WHERE c.id='{team}' RETURN DISTINCT p.name,r.teamPosition".format(team=team2))
        players1 = [player.replace("'","") for player in players1] #limpiamos de comillas la lista de strings,corchetes y espacios
        players1 = [player[1:-1] for player in players1]
        #players1 = [player.replace(" ", "") for player in players1]
        players2 = [player.replace("'", "") for player in players2]
        players2= [player[1:-1] for player in players2]
        #players2 = [player.replace(" ", "") for player in players2]

        mainTeam1 = self.filterTeam(players1)
        mainTeam2 = self.filterTeam(players2)
        print(mainTeam1)
        return mainTeam1,mainTeam2
        
    def overallCalculation(self,mainTeam1,mainTeam2):#aquí calculamos los puntos totales de cada jugador en el enfrentamiento
        """
        q1="MATCH (n) WHERE n.name='Lionel Andrés Messi Cuccittini' return properties(n)"
        nodes = self.conexion.query(q1)
        #results = [record for record in nodes.data()]
        print(nodes)
        print("-----------------")
        nodes = self.conexion.query("MATCH (n)-[r:PLAYS]->(c) WHERE n.name='Lionel Andrés Messi Cuccittini' RETURN n.movementSprintSpeed,n.overall")
        print(nodes)
        nodes = nodes[0].replace(" ","")
        nodes = nodes[1:-1].split(",")
        nodes = [int(node) for node in nodes]
        print(nodes)
        """
        for player in mainTeam1:
            statistic = grade = 0
            if(player.split(",")[1] == " GK"):#ojo hay que poner el espacio porque es lo que contiene el String
                print(player)
                print(player.split(",")[0])
                statistics = self.conexion.query("MATCH (p:Player) WHERE p.name='{player1}' RETURN  p.height_cm,p.gkDiving,p.gkHandling,p.gkKicking,p.gkReflexes,p.gkSpeed,p.gkPositioning,p.powerShotPower,p.powerJumping,p.powerStamina,p.powerLongShots,p.mentalityComposure,p.mentalityVision,p.attackingVolleys,p.movementAgility,p.movementReactions,p.mentalityInterceptions".format(player1=(player.split(",")[0])))
                grades = self.conexion.query("MATCH (p:Position) WHERE p.id='GK' RETURN p.height_cm,p.gkDiving,p.gkHandling,p.gkKicking,p.gkReflexes,p.gkSpeed,p.gkPositioning,p.powerShotPower,p.powerJumping,p.powerStamina,p.powerLongShots,p.mentalityComposure,p.mentalityVision,p.attackingVolleys,p.movementAgility,p.movementReactions,p.mentalityInterceptions")
                print(statistics)
                print(grades)
                
        
        
    def filterTeam(self,players):
        mainTeam = []
        
        for player in players:
            pos = player.split(',')[-1] #cojemos el substring que almacena la posición del jugador
            if pos != " SUB" and pos != " RES":#Si no es un suplente lo añadimos a la lista de titulares
                mainTeam.append(player)
        return mainTeam
    
    
    """
    #Borra la última ocurrencia de un char
    def removeLastOccur(self,string, char):
        string2 = ''
        length = len(string)
        i = 0
    
        while(i < length):
            if(string[i] == char):
                string2 = string[0 : i] + string[i + 1 : length]
            i = i + 1
        return string2
    """