#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Conexión a la base de datos
from neo4j import GraphDatabase

class Neo4j:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()
    
    def query(self,query):
        with self.driver.session() as session:
            query_result = session.write_transaction(self._return_query,query)
            return query_result
    
    @staticmethod
    def _return_query(tx,query):
        result_query = tx.run(query)
        result = []
        
        for record in result_query:
            result.append(str(record.values()))
        return  result
