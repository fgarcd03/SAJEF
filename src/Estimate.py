#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import Conexion #archivo de la conexión con Neo4j para hacer consultas

class Estimate:
    
    def __init__(self,conexion,team1,team2):
        self.Conexion.conexion = Conexion.conexion
        self.team1 = team1
        self.team2 = team2

        
        self.createMainTeam(self.conexion,self.team1,self.team2)
        
        
    def createMainTeam(self,conexion,team1,team2):#la lista de jugadores incluye en las posiciones pares los propios jugadores y las posiciones impares la posición en la que ocupan en el equipo
        a = conexion.query("MATCH (p)-[r:PLAYS]->(c) WHERE c.id='{team}' RETURN DISTINCT p.name,r.teamPosition".format(team=team1))
        print(a)