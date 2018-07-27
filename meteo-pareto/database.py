import psycopg2
import pprint

# Connect to RDS Database using credentials given through dbcredentials.txt
def connectToDB():
	try:
		#Reading dbcredentials.txt to get db connection info
		cred_file = open("dbcredentials.txt","r")
		credentials = cred_file.readlines()
		
		host = credentials[0][5:-1]
		dbname = credentials[1][7:-1]
		user = credentials[2][5:-1]
		password = credentials[3][9:]

		#print ("dbname='"+dbname+"' user='"+user+"' host='"+host+"' password='"+password+"'")

		cred_file.close()

		#Connecting to RDS db
		conn = psycopg2.connect("dbname='"+dbname+"' user='"+user+"' host='"+host+"' password='"+password+"'")
		print("Yay!")

		return conn
	except:
	    print("I am unable to connect to the database")

	    return None

# Init database with a table climate
def initDatabase():
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
	except psycopg2.OperationalError as e:
		print("I can't CREATE TABLE climate\n").format(e)
		return

	conn.commit()

	cur.close()
	conn.close()

# CAREFUL! Drop table climate
def dropClimateTable():
	conn = connectToDB()
	cur = conn.cursor()

	try:
		cur.execute("DROP TABLE climate;")
		print(" Table climate was successfully dropped")
	except:
		print("I can't DROP TABLE climate")
		return

	conn.commit()

	cur.close()
	conn.close()


""" Insert row into table climate
	Argument: date ("DD/MM/YYYY"), rainfall (float), temp (int)
"""
def insertIntoClimate(datei, rainfall, temp):
	conn = connectToDB()
	cur = conn.cursor()

	try:
		cur.execute("INSERT INTO climate (date, rainfall, temperature) VALUES (to_date(%s, 'DD/MM/YYYY'),%s,%s)",
			(datei,
			rainfall,
			temp))
		print(" Insert into Table climate was successfully done")
		return true
	except psycopg2.OperationalError as e:
		print("I can't INSERT INTO climate\n").format(e)
		return false

	conn.commit()

	cur.close()
	conn.close()

# Select All rows from Table climate
def selectAllFromClimate():
	conn = connectToDB()
	cur = conn.cursor()

	try:
		cur.execute("SELECT * FROM climate")
		print(" Select all rows from Table climate was successfully done")
	except psycopg2.OperationalError as e:
		print("I can't SELECT FROM climate\n").format(e)
		return 

	rows = cur.fetchall()

	cur.close()
	conn.close()

	return adaptRowstoJson(rows)


""" Select specific row from Table Climate
	Argument: id (int)
"""
def selectRowFromClimate(cid):
	conn = connectToDB()
	cur = conn.cursor()

	try:
		cur.execute("SELECT * FROM climate WHERE id = (%s)", (cid,))
		print(" Select row from Table climate was successfully done")
	except psycopg2.OperationalError as e:
		print("I can't SELECT FROM climate\n").format(e)
		return

	rows = cur.fetchall()

	cur.close()
	conn.close()

	return adaptRowstoJson(rows)

""" Delete specific row from Table Climate
	Argument: id (int)
"""
def deleteRowFromClimate(cid):
	conn = connectToDB()
	cur = conn.cursor()

	try:
		cur.execute("DELETE FROM climate WHERE id = (%s)", (cid,))
		print(" Row from Table climate was successfully deleted")
		
	except psycopg2.OperationalError as e:
		print("I can't DELETE FROM climate\n").format(e)
		return False
	
	conn.commit()

	cur.close()
	conn.close()
	return True


"""
	Adapt rows from DB to be used as arguments of jsonify function

	Function used by selectAllFromClimate() and selectRowFromClimate()
"""
def adaptRowstoJson(rows):
	#Uncomment it in case you need to see the output
	print("\nRow: \n")
	pprint.pprint(rows)

	to_dict = lambda row: {"id":row[0],"date":row[1],"rainfall":row[2],"temperature":row[3]}

	return list(map(to_dict, rows))