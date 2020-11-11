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
            query_result = session.write_transaction(self._create_and_return_greeting,query)
            #print(query_result)
            return query_result
    
    @staticmethod
    def _create_and_return_greeting(tx,query):
        result_query = tx.run(query)
        
        result = set()
        for record in result_query:
            result.add(record)
            
        return  result #result.single()

"""
if __name__ == "__main__":
    conexion = Neo4j("bolt://localhost:11003", "neo4j", "SIBI20")
    conexion.query("MATCH (p)-[r:PLAYS]->(c) RETURN c.id")
    conexion.close()
"""
