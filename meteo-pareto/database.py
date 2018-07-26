import psycopg2

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