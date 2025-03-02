'''
If there is any issue with the database, you can reset it by running this script.

You can also initialise the database by running this script.
'''
import sqlite3
conn = sqlite3.connect('sessionresults.db')
cur = conn.cursor()
cur.execute ('DROP TABLE IF EXISTS Drivers;')
cur.execute ('DROP TABLE IF EXISTS Engines;')
cur.execute ('DROP TABLE IF EXISTS GPResults;')
cur.execute ('DROP TABLE IF EXISTS GrandsPrix;')
cur.execute ('DROP TABLE IF EXISTS Nationalities;')
cur.execute ('DROP TABLE IF EXISTS Teams;')


cur.execute('''
CREATE TABLE "Drivers" (
	"DriverID"	INTEGER NOT NULL,
	"DriverName"	TEXT NOT NULL UNIQUE,
	"DriverNationality"	INTEGER NOT NULL,
	PRIMARY KEY("DriverID" AUTOINCREMENT)
);''')

cur.execute('''            
CREATE TABLE "Engines" (
	"EngineID"	INTEGER NOT NULL UNIQUE,
	"EngineName"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("EngineID" AUTOINCREMENT)
);''')

cur.execute('''
CREATE TABLE "GPResults" (
	"Position"	INTEGER,
	"Driver"	INTEGER NOT NULL,
	"Team"	INTEGER NOT NULL,
	"Laps"	INTEGER NOT NULL,
	"Engine"	INTEGER NOT NULL,
	"TimeRet"	TEXT NOT NULL,
	"GrandPrix"	INTEGER NOT NULL,
	"Pts"	INTEGER NOT NULL,
	"Privateer"	INTEGER,
	"FL"	INTEGER
);''')

cur.execute('''            
CREATE TABLE "GrandsPrix" (
	"GPID"	INTEGER NOT NULL UNIQUE,
	"GrandPrix"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("GPID" AUTOINCREMENT)
);''')

cur.execute('''
CREATE TABLE "Nationalities" (
	"NationalityID"	INTEGER NOT NULL UNIQUE,
	"Nationality"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("NationalityID" AUTOINCREMENT)
);''')

cur.execute('''            
CREATE TABLE "Teams" (
	"TeamID"	INTEGER NOT NULL UNIQUE,
	"TeamName"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("TeamID" AUTOINCREMENT)
);''')

conn.commit()

print('Database reset/initialised.')