## MatchCars Prices REST API

REST API providing functionality for returning price information for the MatchCars platform.

In order to send a valid request, authentication should be provided by the REST API administrator. This feature is implemented for security purposes. The user should send a log in POST request to with the following json object:

```
url = http://ec2-54-86-137-40.compute-1.amazonaws.com/api/login/

{
    "username" : provided_username,
    "password": provided_password
}
```

This request will return an authentication token to be use as authorization header for all future requests. After logging in, it is possible to send POST requests with the following json object:
```
url = 'http://ec2-54-86-137-40.compute-1.amazonaws.com/api/price/'

{
    "car_id" : int, - Required
    "kilometers" : int, - Required
    "year_model": int,  - Required
    "state" : int, (1-5) - default to 4
    "month": int,  - from RUNT (if available)
    "year" : int  - from RUNT (if available)
}
```

which will return the following object:

```
{
  "adjusted_max_price" : "",
  "adjusted_min_price" : "",
  "predicted_price" : "",
  "status" : ""
}
```

where the "status" field can take the following values:
* OK: car was found, is valid and has a price
* NOT_VALID: car is not valid
* NOT_FOUND: car was not found
* ERROR: generic error

### Valify cars

As defined by MatchCars:

```
* Un vehículo con estado 1 o con un kilometraje que supere la sumatoria de kilometraje máximo respecto a un valor anual (actualmente 20000 km por año), no es valido para MC.
* Un vehículo con estado 2 es posible darle un precio, pero a este usuario no se le presentará una oferta por parte de MC.
* Cuando se presenta un precio, se toma un rango de porcentajes que depende del estado, entonces, si un carro con estado 2 se presenta, se le da al usuario como cota inferior el menor porcentaje que presenta la plataforma y como cota superior el porcentaje de estado regular, si uno de estado 3 se presenta, se le da al usuario como cota inferior el porcentaje regular que presenta la plataforma y como cota superior el porcentaje de estado bueno y así sucesivamente.
```
### Example

POST request with information with a car without RUNT and default state:

```python
#JSON object
car_data = {"car_id" : 20630,
             "kilometers" : 15000,
             "model_year": 2017}

#Response
{
     "status": "OK",
     "adjusted_max_price": 65190.0,
     "adjusted_min_price": 54120.0,
     "predicted_price": 61500.0
}

```

POST request with car information with RUNT and state:

```python
#JSON object
car_data = {"car_id" : 20630,
             "kilometers" : 15000,
             "model_year": 2017,
             "state" : 4,
             "month": 1,
             "year": 2017}

#Response
{
     "status": "OK",
     "adjusted_max_price": 65190.0,
     "adjusted_min_price": 54120.0,
     "predicted_price": 61500.0
}
```


Observations:

* The information marked as (from RUNT) can be passed as argument, a result on the price could be more accurate.
* It is not clear whether I should deliver null results or a price with NOT_VALID status when mileage is above the maximum or status is 1.
