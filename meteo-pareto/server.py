from flask import Flask, jsonify
from flask import request
from flask import send_file
import database
import datetime

app = Flask(__name__)

@app.route('/')
def hello():
	return jsonify({"message": "Welcome!"})


@app.route('/climate', methods=['GET', 'POST'])
def climateReq():
	""" Handle requests to /climate URL """
	# POST /climate - Add row to table climate 
	if request.method == 'POST':

		if request.is_json:

			content = request.get_json()
			response = database.insertIntoClimate(content['date'],
				content['rainfall'], content['temperature'])

			if response:
				return jsonify({"message": "Climate added"})
			else:
				return jsonify({"message": "Something wrong with JSON file or Database Error"})
		else:
			return jsonify({"message": "It is not a JSON file"})


	# GET /climate - List all table climate's rows according to filters applied
	else:
		# Get filters sent through URL
		date = request.args.get('date', default = None, 
			type = str)
		rainfall = request.args.get('rainfall', default = None, 
			type = float)
		temperature = request.args.get('temperature', default = None, 
			type = int)
		month = request.args.get('month', default = None, 
			type = int)
		year = request.args.get('year', default = None, 
			type = int)

		# Check format of date filter in case it is appplied
		try:
			if (date != None):
				datetime.datetime.strptime(date, '%d-%m-%Y')
				
		except ValueError:
			return jsonify({"message":
				"Date filter should have 'DD-MM-YYYY' format"})

		# Get rows from database
		rows = database.selectAllFromClimate(date, 
			rainfall, temperature, month, year)

		# Return rows as JSON
		return jsonify(rows)
		

@app.route('/climate/<id>', methods=['GET', 'DELETE'])
def climateIDReq(id):
	""" Handle requests to /climate/<id> 

	Keyword arguments:
	id -- int

	"""
	# GET /climate/<id> - List one row 
	if request.method == 'GET':
		row = database.selectRowFromClimate(id)

		# Return row as JSON
		return jsonify(row)

	# DELETE /climate/<id> - Delete one row
	else:

		response = database.deleteRowFromClimate(id)

		if response:
			return jsonify({"message": "Climate successfully deleted"})
		else:
			return jsonify({"message": "Climate could not be deleted"})



@app.route('/climate/predict')
def climatePredictReq():
	""" Handle request to /climate/predict """

	#GET /climate/predict - today's climate prediction 


	# Define Temp and Rain Beta (0.7 or 0.8 are recommended)
	betaT = 0.8
	betaR = 0.85 

	#Get rows from database
	rows = database.selectRowsToPredict()

	# Return prediction in case there are at least a few entries from the last 30 days
	if len(rows) != 0:

		# Get temperature prediction
		tempPrediction = predict(rows, betaT, 'temperature')
		# Get rainfall prediction
		rainPrediction = predict(rows, betaR, 'rainfall')

		# Return JSON result
		return jsonify({"todays-temperature-prediction":tempPrediction,
			"todays-rainfall-prediction":rainPrediction})
	else:
		if rows != None:
			return jsonify({"message": 
				"Unable to predict. No entry from the last 30 days was added yet."})
		else:
			return jsonify({"message":"Database Error"})


@app.route('/climate/climateEntries.csv', methods=['GET'])
def climatesCSVReq():
	""" Handle requests to /climate/climateEntries.csv """

	# GET /climate/csv - Download CSV file with all rows listed

	database.putEntriesIntoCSV()

	path = 'climateEntries.csv'

	try:
		return send_file(path, as_attachment=True)
	except Exception as exc:
		return jsonify({"message":"File could not be downloaded: " 
			+ format(exc)})


def predict(rows, beta, attribute):
	""" Calculate prediction according to Exponential Moving Average method 
		
	Keyword arguments:
	rows -- list of dicts
	beta -- float
	attribute -- str

	"""
	
	today = datetime.date.today()
	totalWeights = 0
	totalWeighted = 0

	for row in rows:
		diff = (today - row['date']).days
		weight = beta**diff

		totalWeights += weight
		totalWeighted += weight*row[attribute]

	prediction = round(totalWeighted/totalWeights, 3)

	return prediction

if __name__ == '__main__':
	app.run(host='0.0.0.0', threaded=True)