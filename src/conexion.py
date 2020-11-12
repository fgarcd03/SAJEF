#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from neo4j import GraphDatabase

class Neo4j:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()
    
    def query(self,query):
        with self.driver.session() as session:
            query_result = session.write_transaction(self._return_query,query)
            #print(query_result)
            return query_result
    
    @staticmethod #Tiene que ser estático no se porque
    def _return_query(tx,query):
        result_query = tx.run(query)
        
        result = []
        for record in result_query:
            result.append(str(record.values())[2: -2: 1]) #Convertimos a cadena los valores y quitamos los corchetes y comillas simples
            
        return  result #result.single()