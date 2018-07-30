import psycopg2
import pprint
import datetime
from psycopg2 import sql


def connectToDB():
""" Connect to RDS Database using credentials given through dbcredentials.txt """

	try:
		# Reading dbcredentials.txt to get db connection info
		cred_file = open("dbcredentials.txt","r")
		credentials = cred_file.readlines()
		
		host = credentials[0][5:-1]
		dbname = credentials[1][7:-1]
		user = credentials[2][5:-1]
		password = credentials[3][9:]

		# Uncomment in case you want to see the credentials in use
		#print ("dbname='"+dbname+"' user='"+user+
		#		"' host='"+host+"' password='"+password+"'")

		cred_file.close()

		# Connecting to RDS db
		conn = psycopg2.connect("dbname='"+dbname+"' user='"+user+
			"' host='"+host+"' password='"+password+"'")

		return conn

	except psycopg2.OperationalError:
	    print("Unable to connect to the database")

	    return None


def initDatabase():
""" Init database with a table climate """

	conn = connectToDB()
	cur = conn.cursor()

	try:
		cur.execute("CREATE TABLE climate("+
				"id SERIAL,"
				"date date,"+
				"rainfall real,"+
				"temperature int"

			");")
		print(" Table climate was successfully created")
	except psycopg2.OperationalError as exc:
		print("I can't CREATE TABLE climate\n").format(exc)
		return None

	conn.commit()

	cur.close()
	conn.close()


def dropClimateTable():
""" Drop table climate

	CAREFUL! 
"""
	conn = connectToDB()
	cur = conn.cursor()

	try:
		cur.execute("DROP TABLE climate;")
		print(" Table climate was successfully dropped")
	except psycopg2.OperationalError:
		print("I can't DROP TABLE climate")
		return None

	conn.commit()

	cur.close()
	conn.close()



def insertIntoClimate(datei, rainfall, temp):
""" Insert row into table climate

	Keyword argument: 
	datei -- str
	rainfall -- float 
	temp -- int 
"""
	conn = connectToDB()
	cur = conn.cursor()

	try:
		cur.execute("INSERT INTO climate (date, rainfall, temperature)"+
			" VALUES (to_date(%s, 'DD-MM-YYYY'),%s,%s)",
			(datei,
			rainfall,
			temp))
		print(" Insert into Table climate was successfully done")
		
	except psycopg2.OperationalError as exc:
		print("I can't INSERT INTO climate\n").format(exc)
		return False

	conn.commit()

	cur.close()
	conn.close()

	return True

def selectAllFromClimate(date, rainfall, temperature, month, year):
""" Select All rows from Table climate according to filters applied

Keyword arguments: 
date -- string or None 
rainfall -- float or None
temperature -- int or None
month -- int or None 
year -- int or None

"""
	conn = connectToDB()
	cur = conn.cursor()

	# Check filters and build query according to the ones apllied
	query, values = buildQueryFromFilters(date, rainfall, 
		temperature, month, year)


	# Uncomment this in case you need to see the final query
	#print(query.as_string(conn))

	try:
		cur.execute(query, values)
		print(" Select all rows from Table climate was successfully done")
	except psycopg2.OperationalError as exc:
		print("I can't SELECT FROM climate\n").format(exc)
		return None

	rows = cur.fetchall()

	cur.close()
	conn.close()

	return adaptRowstoDict(rows)


def selectRowFromClimate(cid):
""" Select specific row from Table Climate

Keyword argument: 
cid -- int

"""
	conn = connectToDB()
	cur = conn.cursor()

	try:

		cur.execute("SELECT * FROM climate WHERE id = (%s)", (cid,))

		print(" Select row from Table climate was successfully done")

	except psycopg2.OperationalError as exc:

		print("I can't SELECT FROM climate\n").format(exc)
		return None

	rows = cur.fetchall()

	cur.close()
	conn.close()

	return adaptRowstoDict(rows)


def selectRowsToPredict():
""" Select all rows from the last 30 days from Table Climate """

	conn = connectToDB()
	cur = conn.cursor()

	try:
		cur.execute("SELECT * FROM climate"+
			" WHERE date > current_date - interval '30' day;")

		print(" Select entries from the last 30 days was successfully done")

	except psycopg2.OperationalError as exc:

		print("I can't SELECT FROM climate\n").format(exc)
		return None

	rows = cur.fetchall()

	cur.close()
	conn.close()

	return adaptRowstoDict(rows)

def deleteRowFromClimate(cid):
""" Delete specific row from Table Climate
	
Keyword argument: 
cid -- int

"""
	conn = connectToDB()
	cur = conn.cursor()

	try:
		cur.execute("DELETE FROM climate WHERE id = (%s)", (cid,))
		print(" Row from Table climate was successfully deleted")
		
	except psycopg2.OperationalError as exc:
		print("I can't DELETE FROM climate\n").format(exc)
		return False
	
	conn.commit()

	cur.close()
	conn.close()

	return True


def adaptRowstoDict(rows):
""" Adapt rows from DB to be used as arguments of jsonify function

Function used by selectAllFromClimate(), selectRowFromClimate() and selectRowsToPredict()

"""

	# Uncomment it in case you need to see the output
	#print("\nRow: \n")
	#pprint.pprint(rows)

	to_dict = lambda row: {
		"id":row[0], "date":row[1].date(), "rainfall":row[2], 
		"temperature":row[3]
	}

	return list(map(to_dict, rows))


def buildQueryFromFilters(date, rainfall, temperature, month, year):
""" Construct query according to filters 

Keyword arguments: 
date -- string or None 
rainfall -- float or None 
temperature -- int or None
month -- int or None 
year -- int or None

"""
	# Main part of the query
	query = sql.SQL("SELECT * FROM climate")

	conditions = []
	values = []

	# Check if each filter is actually applied, 
	# if so, its respective part of the query is appended to the main part
	if date != None:
		clause = sql.SQL("date = to_date(%s, 'DD-MM-YYYY')")
		conditions.append(clause)
		values.append(date)
	if temperature != None:
		clause = sql.SQL("temperature = (%s)")
		conditions.append(clause)
		values.append(temperature)
	if rainfall != None:
		clause = sql.SQL("rainfall = (%s)")
		conditions.append(clause)
		values.append(rainfall)
	if month != None:
		clause = sql.SQL("EXTRACT(MONTH FROM date) = (%s)")
		conditions.append(clause)
		values.append(month)
	if year != None:
		clause = sql.SQL("EXTRACT(YEAR FROM date) = (%s)")
		conditions.append(clause)
		values.append(year)

	# Put all together
	if len(conditions) > 0:
		query = sql.SQL(" ").join([query, sql.SQL("WHERE")])

		conj = sql.SQL(" AND ").join(conditions)

		query = sql.SQL(" ").join([query, conj])

	return query, values
