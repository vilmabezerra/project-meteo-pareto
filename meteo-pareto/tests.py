import unittest
import database
import server
import datetime

class ApiTests(unittest.TestCase):
	""" Unit Testing - Test Cases """

	def testPredict(self):
		""" Test function predict(), 
			which is implemented in server.py 
		"""

		now = datetime.datetime.now()
		oneDay = datetime.timedelta(days = 1)
    	
		dayAgo = now - oneDay
		twoDaysAgo = now - oneDay * 2
		threeDaysAgo = now - oneDay * 3

		rows = [{"id":1, 
					"date":datetime.date(dayAgo.year, 
						dayAgo.month, dayAgo.day), 
					"rainfall":102.0, "temperature":25},
				{"id":2, 
					"date":datetime.date(twoDaysAgo.year, 
						twoDaysAgo.month, twoDaysAgo.day),
					"rainfall":90.5, "temperature":27},
				{"id":3, 
					"date":datetime.date(threeDaysAgo.year, 
						threeDaysAgo.month, threeDaysAgo.day), 
					"rainfall":81.0, "temperature":29}]

		beta = 0.8
		attribute = "temperature"

		#In this case EMA is calculated as (0.8ˆ1×25 + 0.8^2×27 + 0.8^3×29)/
		#					  			   (0.8ˆ1 + 0.8^2 + 0.8^3)
		expecResult = round(26.7049180327868, 3)    	

		self.assertEqual(server.predict(rows, beta, attribute), expecResult)

	def testBuildQuery(self):
		""" Test function buildQueryFromFilters(), 
			which is implemented in database.py 
		"""

		date = '25-07-2018'
		rainfall = 90.0
		temperature = 27
		month = 6
		year = 2017

		conn = database.connectToDB()


		validQuery = ("SELECT * FROM climate WHERE"
		" date = to_date(%s, 'DD-MM-YYYY')"
		" AND temperature = (%s) AND rainfall = real '%s'"
		" AND EXTRACT(MONTH FROM date) = (%s)"
		" AND EXTRACT(YEAR FROM date) = (%s)")

		query, _ = database.buildQueryFromFilters(date, rainfall,
		 temperature, month, year)

		self.assertEqual(query.as_string(conn), validQuery)

		conn.close()


if __name__ == '__main__':
    unittest.main()