#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Estimate:
    
    def __init__(self,conexion,team1,team2):
        self.conexion = conexion
        self.team1 = team1
        self.team2 = team2

        
        self.createMainTeam(self.conexion,self.team1,self.team2)
        
        
    def createMainTeam(self,conexion,team1,team2):#la lista de jugadores incluye en las posiciones pares los propios jugadores y las posiciones impares la posición en la que ocupan en el equipo
        players1 = conexion.query("MATCH (p)-[r:PLAYS]->(c) WHERE c.id='{team}' RETURN DISTINCT p.name,r.teamPosition".format(team=team1)) #obtenemos todos los jugadores y sus correspondientes posiciones en los equipos
        
        players2 = conexion.query("MATCH (p)-[r:PLAYS]->(c) WHERE c.id='{team}' RETURN DISTINCT p.name,r.teamPosition".format(team=team2))
        
        players1 = [player.replace("'", "") for player in players1] #limpiamos de comillas la lista los strings
        players2 = [player.replace("'", "") for player in players2]
        
        print(players1[1],players2[1])