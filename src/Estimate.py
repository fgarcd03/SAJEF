#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Estimate:
    
    def __init__(self,conexion,team1,team2):
        self.conexion = conexion
        self.team1 = team1
        self.team2 = team2

        
        self.createMainTeam(self.conexion,self.team1,self.team2)
        
        
    def createMainTeam(self,conexion,team1,team2):#Táctica 4-3-3
        mainTeam1 = maintTeam2 = []
        
        players1 = conexion.query("MATCH (p)-[r:PLAYS]->(c) WHERE c.id='{team}' RETURN DISTINCT p.name,p.overall,r.teamPosition".format(team=team1)) #obtenemos todos los jugadores y sus correspondientes posiciones en los equipos
        players2 = conexion.query("MATCH (p)-[r:PLAYS]->(c) WHERE c.id='{team}' RETURN DISTINCT p.name,p.overall,r.teamPosition".format(team=team2))
        players1 = [player.replace("'", "") for player in players1] #limpiamos de comillas la lista de strings
        players2 = [player.replace("'", "") for player in players2]
        
        mainTeam1 = self.filterTeam(players1)
        mainTeam2 = self.filterTeam(players2)
        print(mainTeam1)
        print("-------")
        print(mainTeam2)
        if len(mainTeam1) != 11:
            print("ERROR DE TAMAÑO DEL EQUIPO 1")
        if len(mainTeam2) != 11:
            print("ERROR DE TAMAÑO DEL EQUIPO 2")
        
        
        
        
    def filterTeam(self,players):
        GK = LBaLWB = RBaRWB = CM = LCM = RCM = ST = LW = RW = CDM = CAM = CF = LCB = RCB = ""
        mainTeam = []
        
        for player in players:
            player = self.removeLastOccur(self.removeLastOccur(player, " "), " ")#Llamamos dos veces para que se eliminen los dos espacios
            overall = player.split(',')[1] #cojemos el substring que almacena el overall del jugador
            pos = player.split(',')[-1] #cojemos el substring que almacena la posición del jugador
            
            if pos == "GK":
                if (len(GK) > 0 and overall > GK.split(',')[1]) or len(GK) == 0: #Si había algo guardado y el overall es mayor, lo guardamos en su lugar, y si no había nada pues lo guardamos sin más
                    GK = player
            if pos == "LB" or pos == "LWB":
                if (len(LBaLWB) > 0 and overall > LBaLWB.split(',')[1]) or len(LBaLWB) == 0:
                    LBaLWB = player
            if pos == "RB" or pos == "RWB":
                if (len(RBaRWB) > 0 and overall > RBaRWB.split(',')[1]) or len(RBaRWB) == 0:
                    RBaRWB = player
            if pos == "CM":
                if (len(CM) > 0 and overall > CM.split(',')[1]) or len(CM) == 0:
                    CM = player
            if pos == "LCM":
                if (len(LCM) > 0 and overall > LCM.split(',')[1]) or len(LCM) == 0:
                    LCM = player
            if pos == "RCM":
                if (len(RCM) > 0 and overall > RCM.split(',')[1]) or len(RCM) == 0:
                    RCM = player
            if pos == "ST":
                if (len(ST) > 0 and overall > ST.split(',')[1]) or len(ST) == 0:
                    ST = player
            if pos == "LW":
                if (len(LW) > 0 and overall > LW.split(',')[1]) or len(LW) == 0:
                    LW = player
            if pos == "RW":
                if (len(RW) > 0 and overall > RW.split(',')[1]) or len(RW) == 0:
                    RW = player
            if pos == "CDM":
                if (len(CDM) > 0 and overall > CDM.split(',')[1]) or len(CDM) == 0:
                    CDM = player
            if pos == "CAM":
                if (len(CAM) > 0 and overall > CAM.split(',')[1]) or len(CAM) == 0:
                    CAM = player
            if pos == "CF":
                if (len(CF) > 0 and overall > CF.split(',')[1]) or len(CF) == 0:
                    CF = player
            if pos == "LCB":
                if (len(LCB) > 0 and overall > LCB.split(',')[1]) or len(LCB) == 0:
                    LCB = player
            if pos == "RCB":
                if (len(RCB) > 0 and overall > RCB.split(',')[1]) or len(RCB) == 0:
                    RCB = player
        
        mainTeam.extend([GK,LCB,RCB,LBaLWB,RBaRWB,CDM,CM,LCM,RCM,CAM,CF,ST,LW,RW])
        mainTeam = [i for i in mainTeam if i] #quitamos huecos vacíos de posiciones que no se usa
        
        return mainTeam
    
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