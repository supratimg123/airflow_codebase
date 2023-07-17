# airflow_codebase
Create a virtual environment. <br>
Go to location of "requirements.txt" and install dependencies. <br>
Check for an folder "airflow" created at "/home/user/". otherwise locate it. Copy "graph_main" folder within "home/user/airflow/dags/". copy "dag.py" outside "graph_main". <br>
Install neo4j desktop from the website of neo4j. Create a new project there and copy all nodes from "bat_brands.docx", paste in neo4j browser and run. Our db is ready. <br>
There are two types of input one for the brand name and other for player name. Give any name of bat or brand which you want to query from the graph database nodes. <br>
Activate virtual env and open three terminal. From the airflow folder location open the airflow webserver and airflow scheduler. From the third one run dag.py from proper location. Before that write the json input inside "dag.py". <br>
Open webserver from browser using "http://localhost:8080/" and reset to check dag run. Open "graph_processing" task log to check the output. <br>
bat_brands.docx - Information of nodes with relationship. <br>
config.py and config.yaml - specifying parameters for neo4j db connection. <br>
graph_app.py - main service code. <br>
graph_query.py - python code for quering Neo4j graph and will return the matched output. <br>
requirements.txt - python libraries and other dependencies. <br>
input.txt - for details of input structure. <br>
