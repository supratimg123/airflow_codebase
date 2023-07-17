import logging,json,requests,os
from datetime import timedelta,datetime
from airflow import DAG
import yaml
import urllib, shutil, subprocess
from airflow.executors.local_executor import LocalExecutor
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

from graph_main.config import *
from graph_main.src.graph_app import graph_processing

def create_dag(dag_id,d,schedule_interval,default_args,catchup):

    def start(**kwargs):
        print("Hello World")
        print("This is start of DAG: {}".format(str(dag_id)))
    
    def process_graph(**kwargs):
        print("Graph Processing Starts")
        data= kwargs["data"]
        print(data)
        response = graph_processing(data)
        print(response)
    
    def end(**kwargs):
        print("Hello World")
        print("This is end of DAG: {}".format(str(dag_id)))
    
    dag=DAG(dag_id,
                default_args= default_args,
                schedule_interval= schedule_interval,
                )
    with dag:
        opr_start = PythonOperator(
                    task_id = 'start',
                    python_callable= start,
                    op_kwargs={},
                    provide_context= True)
        
        opr_graph_process = PythonOperator(
                    task_id = 'graph_process',
                    python_callable = process_graph,
                    op_kwargs={"data":d},
                    provide_context=True)
        
        opr_end = PythonOperator(
                    task_id = 'end',
                    python_callable= end,
                    provide_context= True)
        opr_start >> opr_graph_process >> opr_end
    return dag


default_arg={'owner' : 'airflow','start_date': datetime(2020, 1, 10, 10, 30, 00),
        'end_date':datetime(2020, 1, 10, 10, 30, 00),
        'concurrency': 16,
        'retries': 5,
        'retry_delay': timedelta (seconds = 30)}

####write your input here####
d={
"dag_id":"brand4567",
"query_type":"brands",
"branch_name":["brand"],
"input_list":["mrf"]
}
#############################
dag_id=d["dag_id"]
dag= create_dag(dag_id,d,schedule_interval='@once',default_args=default_arg,catchup=False)
globals()[dag_id]=dag