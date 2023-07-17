import sys
# sys.path.append("./config.yaml")
# from config import *

from neo4j import __version__ as neo4j_version
from neo4j import GraphDatabase
import pandas as pd
import copy,re,json
from graph_main.config import *
from graph_main.src.graph_query import *
 

def graph_processing(request_data):
    print(request_data)
    
    final_result=start_graph_process(request_data)
    print("after_graph_process:: ", final_result)
    return final_result   
    #return json.dumps({"graph_output":'{}'.format(final_result)})  
    # return{"status":200}

def preprocess(input_list):

   # PREPROCESSING OF INPUT STATEMENTS
    # Remove leading & trailing spaces
    pre_input = [inp.lower().strip() for inp in input_list]
    
    return pre_input

def start_graph_process(input):
    
    # Call the preprocessing function
    print("input:: ",input)
    pre_list= preprocess(input['input_list'])
    final_result=[]
    #print("\nINPUT LIST:\n",pre_list_without_empty_stmt)
    # Call the function for querying the graph
    if all(k in input for k in ("query_type","input_list")):
        pass
    else:
        print("One Or More Input Key Missing")
        return final_result
    
    data = query_graph(input['branch_name'][0], pre_list)
    if data==[]:
        print("NONE OF THE STATEMENTS ARE MAPPED TO GRAPH NODES")
    else:
        final_result=data
    return final_result



