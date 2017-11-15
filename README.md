# Fair Vehicle Sales Client


## This is a test API for interaction with Vehicle Sales.


### SETUP

* pip install -r requirements.txt
* python manage.py makemigrations
* python manage.py migrate
* ./manage.py runserver

Add username/password for authentication into the API. Two test users have already been added. Feel free to use their usernames (phaedraa, admin) when making requests.
* python manage.py createsuperuser
* admin, password123

## USE

A vehicle sale require's valid input data, including, a buyer json, price, vin, car_class json,
seller json. All car_class key, value pairs are required to create a valid car class. All
buyer and seller keys, value pairs are required to create valid buyers and sellers.
Buyer and seller types can be either 'dealer' OR 'individual'. A sale between can only
occur between a dealer and individual.

**If the buyer and/or seller already exist in our system, the id can passed in and all other fields,
left as empty strings. Otherwise, all other fields are required and the id should be an empty string.*

Example input json parameters:
```
data = {
    'buyer': {'ein': '553598', 'type': 'dealer', 'id': '', 'name': 'DealerABC'},
    'price': 989898.33,
    'vin': 'some_17_digit_vin',
    'car_class': {'make': 'Tesla', 'model': 'S3', 'year': '2017'},
    'seller': {'first_name': 'Alisia', 'last_name': 'Sanchez', 'ssn_last_4': '8932',
    'dob': '05/30/1967', 'license_no': '123ND5', 'type': 'individual',
    'id': ''},
}
```


Accepted calls (using python `requests` library) include the bellow:
*Note: internal 1K limits are placed on fetch all queries*

#### Create new Vehicle Sale (POST):
*Buyers/Sellers/Car Classes that don't yet exist in our system, will be automatically
created when providing the required and corresponding data. If they already exist, providing
their corresponding id's will allow for ensured retrieval*
```
res = requests.post(
    your_local_host/vehicle_sales/,
    data=json.dumps(data),
    headers={'Content-Type': 'application/json'},
    auth=(username, password))
    
```

Response will include a json of serialized vehicle sale data.

#### Query Vehicle Sales (GET):
*Query by car_class and/or buyer and/or seller. `data` should contain relevant information
on each single car class, buyer and seller.*
**Defualts to fetch all related sales data. If only 
latest sale data is desired, add 'latest', True key, value pair to
data input**
Example data:
```
data = {'buyer': {'id': 5}, 'seller': {'id': 3}}

res = requests.get(
    your_local_host/vehicle_sales/,
    data=json.dumps(data),
    headers={'Content-Type': 'application/json'},
    auth=(username, password))
```

Response will include a json of serialized vehicle sale data.

#### Get Vehicle Sales Data of Specific Car (by VIN) (GET):
*Query by car vehicle identification number: VIN*
*Data is optional. Defualts to fetch all related sales data. If only 
latest sale data is desired, add 'latest', True key, value pair to
data input*

```
res = requests.get(
    your_local_host/vehicle_sales/car/<some_vin>,
    data=json.dumps({'latest': True})
    headers={'Content-Type': 'application/json'},
    auth=(username, password))
```

Response will include a json of serialized vehicle sale data.

#### Get Vehicle Sales Data of Specific Sale (by id) (GET):
*Fetch data for specific vehicle sale*

```
res = requests.get(
    your_local_host/vehicle_sales/<some_sale_id>,
    headers={'Content-Type': 'application/json'},
    auth=(username, password))
  ```

Response will include a json of serialized vehicle sale data.

#### Update Vehicle Sales Data of Specific Sale (by id) (PUT):
*Update data for specific vehicle sale*

```
res = requests.put(
    your_local_host/vehicle_sales/<some_sale_id>,
    data=json.dumps({'price': 99999.99})
    headers={'Content-Type': 'application/json'},
    auth=(username, password))
```

Response will include a json of serialized vehicle sale data.

#### Delete Vehicle Sales Data of Specific Sale (by id) (PUT):
*Delete vehicle sale record*

```
res = requests.delete(
    your_local_host/vehicle_sales/<some_sale_id>,
    headers={'Content-Type': 'application/json'},
    auth=(username, password))
```

Response will include a success key with status 200.

## QUESTIONS
Security - How would you protect against outsiders from inserting/querying records?

** Require users be registered in addition to employing token authentication.

Scalability - Would anything change if your system had 100 million vehicle sale records? What if the API had to handle 10 searches per second?

**In the case of large database of records: Sharding the database to distribute the load in addition to elastic search, could enable much faster data retrieval. With multiple searches per second, query caching would be useful, in addition to in to adding a slave database for read-only purposes. For both, adding index on relevant columns such as car vin, could also improve inefficiencies.

Data Integrity - How would you handle erroneous sale records data (e.g. malformed VINs, invalid field values)?

**Validate data in the request, before creating or saving a record. Some of this can also be done on the object models themselves.

Auditability - How would you track the source of any incoming data as well as the source of any searches?

**The incoming API request contains a decent amount of information on the source of the request, such as: the remote address of the client, the address (URI) of the resource from which the Request-URI was obtained and, if a forwarded header exists, a list of all ip addresses from the client ip to the last proxy server. All of this data can be tracked and stored for the ability to analyze the source of incoming data and searches.
