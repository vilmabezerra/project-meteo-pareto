# Project Meteo Pareto

API REST to store and manage climate data 

Python + Flask deployed to AWS 

## Documentation

### List all climate data

#### Request:

    GET/climate 

### View one specific climate data

#### Request:
    GET/climate/<id>
  
### Add climate data

#### Request:
    POST/climate

### Delete climate data

#### Request:
    DELETE/climate/<id>
  
### View current day climate prediction

#### Request:
    GET/climate/predict
