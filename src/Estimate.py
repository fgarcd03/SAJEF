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

    
        
        
        
        
    def filterTeam(self,players):
        mainTeam = []
        
        for player in players:
            player = self.removeLastOccur(self.removeLastOccur(player, " "), " ")#Llamamos dos veces para que se eliminen los dos espacios
            pos = player.split(',')[-1] #cojemos el substring que almacena la posición del jugador
            if pos != "SUB" and pos != "RES":#Si no es un suplente lo añadimos a la lista de titulares
                mainTeam.append(player)
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