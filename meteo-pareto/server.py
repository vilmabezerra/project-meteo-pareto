from flask import Flask, jsonify
from flask import request
import database
import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
	return jsonify({"message": "Hello World!"})

"""
	POST /climate - Add row to table climate 
	GET /climate - List all table climate's rows according to filters applied
"""
@app.route('/climate', methods=['GET', 'POST'])
def climateReq():
	# Adding row to climate
	if request.method == 'POST':
		if (request.is_json):
			content = request.get_json()
			print (content)

			response = database.insertIntoClimate(content['date'],content['rainfall'], content['temperature'])
			if (response):
				return jsonify({"message": "Climate added"})
			else:
				return jsonify({"message": "Something wrong with JSON file"})
		else:
			return jsonify({"message": "It is not a JSON file"})

	# List all rows of climate according to filters
	else:
		#Get filters sent through URL
		date = request.args.get('date', default = None, type = str)
		rainfall = request.args.get('rainfall', default = None, type = float)
		temperature = request.args.get('temperature', default = None, type = int)
		month = request.args.get('month', default = None, type = int)
		year = request.args.get('year', default = None, type = int)

		#Check date filter appplied
		try:
			if (date == None):
				pass
			else:
				datetime.datetime.strptime(date, '%d-%m-%Y')
		except:
			return jsonify({"message":"Date filter should have 'DD-MM-YYYY' format"})

		#Get rows from database
		rows = database.selectAllFromClimate(date, rainfall, temperature, month, year)

		# Return rows as JSON
		return jsonify(rows)
		


"""
	GET /climate/<id> - List one row 
	DELETE /climate/<id> - Delete one row
"""
@app.route('/climate/<id>', methods=['GET', 'DELETE'])
def climateIDReq(id):
	
	if request.method == 'GET':
		row = database.selectRowFromClimate(id)

		#Return row as JSON
		return jsonify(row)

	else:
		response = database.deleteRowFromClimate(id)
		if (response):
			return jsonify({"message": "Climate successfully deleted"})
		else:
			return jsonify({"message": "Could not delete Climate"})


"""
	GET /climate/predict - climate prediction for today
"""
@app.route('/climate/predict')
def climatePredictReq():
	#Get rows from database
	rows = database.selectRowsToPredict()

	# Return rows as JSON
	if(rows != None):
		#TODO
		pass
	else:
		return jsonify({"message": "Unable to predict. No entry from the last 30 days was added yet."})
	


if __name__ == '__main__':
	app.run()