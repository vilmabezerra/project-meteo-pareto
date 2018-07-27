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
	GET /climate - List all table climate's rows
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

	# List all rows of climate
	else:
		#Get filter sent through URL
		date = request.args.get('date', default = None, type = datetime.date)
		rainfall = request.args.get('rainfall', default = None, type = float)
		temperature = request.args.get('temperature', default = None, type = int)

		#No filter added
		if ((date == None) and (rainfall == None) and (temperature == None)):
			rows = database.selectAllFromClimate()

		#With filter
		else:
			#TODO

		# Return JSON results
		if(rows != None):
			return jsonify(rows)
		else:
			return jsonify({"message": "None climate was added yet"})


"""
	GET /climate/<id> - List one row 
	DELETE /climate/<id> - Delete one row
"""
@app.route('/climate/<id>', methods=['GET', 'DELETE'])
def climateIDReq(id):
	
	if request.method == 'GET':
		row = database.selectRowFromClimate(id)
		if(row != None):
			return jsonify(row)
		else:
			return jsonify({"message": "There is no such row"})

	else:
		response = database.deleteRowFromClimate(id)
		if (response):
			return jsonify({"message": "Climate deleted"})
		else:
			return jsonify({"message": "Could not deleted Climate"})

"""
	GET /climate/predict - climate prediction for today
"""
@app.route('/climate/predict')
def climatePredictReq():
	#TODO


if __name__ == '__main__':
	app.run()