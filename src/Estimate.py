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
        GK = LB = RB = CM = LM = RM = ST = LW = RW = ""
        CB = 0
        
        players1 = conexion.query("MATCH (p)-[r:PLAYS]->(c) WHERE c.id='{team}' RETURN DISTINCT p.name,p.overall,r.teamPosition".format(team=team1)) #obtenemos todos los jugadores y sus correspondientes posiciones en los equipos
        players2 = conexion.query("MATCH (p)-[r:PLAYS]->(c) WHERE c.id='{team}' RETURN DISTINCT p.name,p.overall,r.teamPosition".format(team=team2))
        players1 = [player.replace("'", "") for player in players1] #limpiamos de comillas la lista de strings
        players2 = [player.replace("'", "") for player in players2]
        
        
        for player in players1:
            player = self.removeLastOccur(self.removeLastOccur(player, " "), " ")#Llamamos dos veces para que se eliminen los dos espacios
            overall = player.split(',')[1] #cojemos el substring que almacena el overall del jugador
            pos = player.split(',')[-1] #cojemos el substring que almacena la posición del jugador
            
            if pos == "GK":
                if (len(GK) > 0 and overall > GK.split(',')[1]) or len(GK) == 0: #Si había algo guardado y el overall es mayor, lo guardamos en su lugar, y si no había nada pues lo guardamos sin más
                    GK = player
            if pos == "LB":
                if (len(LB) > 0 and overall > LB.split(',')[1]) or len(LB) == 0: #Si había algo guardado y el overall es mayor, lo guardamos en su lugar, y si no había nada pues lo guardamos sin más
                    LB = player
            if pos == "RB":
                if (len(RB) > 0 and overall > RB.split(',')[1]) or len(RB) == 0: #Si había algo guardado y el overall es mayor, lo guardamos en su lugar, y si no había nada pues lo guardamos sin más
                    RB = player
            if pos == "CM":
                if (len(CM) > 0 and overall > CM.split(',')[1]) or len(CM) == 0: #Si había algo guardado y el overall es mayor, lo guardamos en su lugar, y si no había nada pues lo guardamos sin más
                    CM = player
            if pos == "LM":
                if (len(LM) > 0 and overall > LM.split(',')[1]) or len(LM) == 0: #Si había algo guardado y el overall es mayor, lo guardamos en su lugar, y si no había nada pues lo guardamos sin más
                    LM = player
            if pos == "RM":
                if (len(RM) > 0 and overall > RM.split(',')[1]) or len(RM) == 0: #Si había algo guardado y el overall es mayor, lo guardamos en su lugar, y si no había nada pues lo guardamos sin más
                    RM = player
            if pos == "ST":
                if (len(ST) > 0 and overall > ST.split(',')[1]) or len(ST) == 0: #Si había algo guardado y el overall es mayor, lo guardamos en su lugar, y si no había nada pues lo guardamos sin más
                    ST = player
            if pos == "LW":
                if (len(LW) > 0 and overall > LW.split(',')[1]) or len(LW) == 0: #Si había algo guardado y el overall es mayor, lo guardamos en su lugar, y si no había nada pues lo guardamos sin más
                    LW = player
            if pos == "RW":
                if (len(RW) > 0 and overall > RW.split(',')[1]) or len(RW) == 0: #Si había algo guardado y el overall es mayor, lo guardamos en su lugar, y si no había nada pues lo guardamos sin más
                    RW = player
        
        mainTeam1.extend([GK,LB,RB,CM,LM,RM,ST,LW,RW])
        print(mainTeam1)

        
        
    
        
    
    
    
    
    
    
    
    
    
    
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