How to make it work !!

In the code produce_stats.py : 

Change parameters, username,password,port in the function "client = MongoClient()" 
to connect at MongoDB and access the databases.
In the line just after, "db= client.test", change "test" by the name of the DB


To run the code :

Connect to mongoDB :
open a terminal
Write : mongod (or sudo mongod if it breaks)

Open a second terminal, go to the folder where all the codes are !

Write : pip install -r requirement.txt
Write : python create_xlsx_graph.py

You will have to choose the company you want to focus on and the dates of start and end.

Wait until you have the hand again, the spreadsheet created should be in the folder where all the codes are, 
the graphs are on plotly on your account.

