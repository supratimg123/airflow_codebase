import sys
sys.path.append("./config.yaml")
from config import *

from neo4j import __version__ as neo4j_version
from neo4j import GraphDatabase
import pandas as pd
import re
from fuzzywuzzy import process
from collections import Counter

# Define a connection class to connect to the graph database.
class Neo4jConnection:
    def __init__(self, uri, user, pwd, acqn_timeout, conn_timeout):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__acqn_timeout = acqn_timeout
        self.__conn_timeout = conn_timeout
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd),
                                                 connection_acquisition_timeout=self.__acqn_timeout,
                                                 connection_timeout=self.__conn_timeout)
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def query(self, query, param, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.__driver.session(database=db) if db is not None else self.__driver.session()
            print("session",session)
            response = list(session.run(query,param))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response


# Create an instance of connection with the required parameters-
# the url,username,password,connection_acquisition_timeout and connection_timeout
''' 
Note: connection_acquisition_timeout-The maximum amount of time in seconds a session will wait 
when requesting a connection from the connection pool. 
Ensure that the value of this configuration is higher than the configured connection_timeout.
connection_timeout- The maximum amount of time in seconds to wait for a TCP connection to be established.
'''

# Create an instance of connection with the required parameters-the url,username and password
url = get_url()
username = get_username()
password = get_password()
acquisition_timeout = get_acqn_timeout()
conn_timeout = get_conn_timeout()
#print(url,type(url),username,type(username),password,type(password),acquisition_timeout,type(acquisition_timeout),conn_timeout,type(conn_timeout))
conn = Neo4jConnection(uri=url, user=username, pwd=password,
                       acqn_timeout=acquisition_timeout, conn_timeout=conn_timeout)

def query_graph(branchname, preprocessed_list):

    # Match the graph nodes based on node 'title' and the predefined rules
    if branchname == "person":
        query_string = '''
        MATCH (n:person)-[:PLAYED_WITH]->(brand:brands)
        WHERE n.title IN $inp_list
        RETURN labels(brand) as Labels,brand.title as brand_name,brand.built_by as Owner,brand.location as located
        ORDER BY id(brand)
        '''
        # Get the mapped statements
        for try_count in range(5):
            try:
                data =[dict(_) for _ in conn.query(query_string,{'inp_list':preprocessed_list})]
                print(data)
                break
            except:
                if try_count<4:
                    print('EXCEPTION........Connection is establishing....')
                    print(f'retrying {try_count+1}time, after 30 seconds.....')
                    time.sleep(30)
                elif try_count==4:
                    print(f"Couldn't Establish Connection......")
                    data=[]
    elif branchname=='brand':
        query_string = '''
        MATCH (n:brands)-[:PLAYED_BY]->(per:person)
        WHERE n.title IN $inp_list
        RETURN labels(per) as Labels,per.title as player_name,per.country as country
        ORDER BY id(per)
        '''
        # Get the mapped statements
        for try_count in range(5):
            try:
                data =[dict(_) for _ in conn.query(query_string,{'inp_list':preprocessed_list})]
                print(data)
                break
            except:
                if try_count<4:
                    print('EXCEPTION........Connection is establishing....')
                    print(f'retrying {try_count+1}time, after 30 seconds.....')
                    time.sleep(30)
                elif try_count==4:
                    print(f"Couldn't Establish Connection......")
                    data=[]
        
                

    conn.close()  # Close the connection
    return data