#!/usr/bin/python3
#Crowdtour
import pymysql

# Open database connection
connection = pymysql.connect(host='localhost',user='testhost',password='test',db='crowdtour')

# prepare a cursor object using cursor() method
cursor = connection.cursor()

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS MARKERS")

# Create table as per requirement
sql = """CREATE TABLE MARKERS (
   id  INT NOT NULL,
   name VARCHAR(20),
   address INT,  
   lat FLOAT,
   lng FLOAT,
   type VARCHAR(30) )"""

cursor.execute(sql)

# disconnect from server
connection.close()
