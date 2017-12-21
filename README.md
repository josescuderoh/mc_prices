# MatchCars Prices REST API

REST API providing functionality for returning price information for the
MatchCars platform.

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
    "car_id" : "", - Required
    "kilometers" : "", - Required
    "year_model": "",  - Required
    "state" : "",
    "month": "",  - from RUNT
    "year" : ""  - from RUNT
}
```

which will return the following object:

{
  "adjusted_max_price" : "",
  "adjusted_min_price" : "",
  "predicted_price" : "",
  "status" : ""
}

where the "status" field can take the following values:
OK: car was found, is valid and has a price
NOT_VALID: car is not valid
NOT_FOUND: car was not found
ERROR: generic error
