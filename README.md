# Project Meteo Pareto

API REST to store and manage climate data 

Python + Flask deployed to AWS 

## Documentation

### List all climate entries

#### Request:

    GET  /climate 

### View one specific climate entry

#### Request:
    GET  /climate/<id>
  
### Add climate entry

#### Request:
    POST  /climate

### Delete climate entry

#### Request:
    DELETE  /climate/<id>
  
### View current day climate prediction

#### Request:
    GET  /climate/predict
