# Project Meteo Pareto

API REST to store and manage climate data 

Python + Flask deployed to an EC2 and using a RDS database

## Documentation

There are a few avalable resquests to this API, which are described bellow. 
Each request has a JSON file as output that should contain a success 
or error message, or, in some cases, a list of entries.

### Requests

#### List all climate entries

The request used to get all entries in database should be

    GET  /climate 

#### List specific climate entries

Some filters (the ones listed bellow) are available in order to return only the entries
that are really necessary to the user.

Available Filters (Usage):
- Date (e.g. 24-05-2000)
- Rainfall (e.g. 90.0)
- Temperature (e.g. 31)
- Month (range: 1 - 12)
- Year (e.g. 2017)

As an example of a request with filters applied we have:

    GET  /climate?month=7&temperature=31&date=25-05-2000

#### Add climate entry

The request bellow should be used to add a new entry. 

    POST  /climate
    
This request should have as body a JSON file with format:

    {
	"date": "DD-MM-YYYY",
	"rainfall": 0.0,
	"temperature": 30
    }

Notice that rainfall and temperature can have different values.

#### View one specific climate entry

In order to view one specific entry, it should be used the following request.

    GET  /climate/<id>
  
Notice that the id should be an integer, which it is available when requesting 
to list database entries.

#### Delete climate entry

To delete an entry, the following request should be used.

    DELETE  /climate/<id>
  
#### View current day climate prediction

The following request returns a JSON file with current day's rainfall and temperature 
prediction according to an Exponential Moving Average from the last 30 days entries.

    GET  /climate/predict

Notice that, if there is no entry from the last 30 days, the prediction could not be done.

#### Download CSV file with all entries

The request bellow should be used to get a CSV file with all entries available in database

    GET /climate/csv
    
A file named climateEntries.csv should be downloaded

### Tips

- In order to manually test the functional requisites, Postman tool is advised

	Obs: Postman does not work with the requests that should download files
