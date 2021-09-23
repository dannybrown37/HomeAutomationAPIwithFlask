import requests
from pprint import pprint


BASE = "http://127.0.0.1:5000/"


# GET all home system statuses
response = requests.get(BASE + "home")
pprint(response.json())

# POST three light fixtures
for fixture in ["kitchen", "bathroom", "office"]:
    response = requests.post(BASE + f"fixtures/{fixture}")
    pprint(response.json())

# GET request a specific fixture with JSON/query param
response = requests.get(BASE + "fixtures", json={"name": "office"})
pprint(response.json())

# GET request all fixture info
response = requests.get(BASE + "fixtures")
pprint(response.json())

# PATCH Toggle one of them on 
response = requests.patch(BASE + "fixtures/kitchen")
pprint(response.json())

# POST one more fixture including query params that default its status to on
response = requests.post(BASE + "fixtures/bedroom", json={"status": "on"})
pprint(response.json())

# GET requests on non-existing fixtures, 404 expected
response = requests.get(BASE + "fixtures", json={"name": "studio"})
print(response.status_code, response.json())

# GET home system statuses
response = requests.get(BASE + "home")
pprint(response.json())

# DELETE a light fixture, 
response = requests.delete(BASE + "fixtures/bathroom")
print(response.json())

# Attempt to DELETE a non-existent light fixture, 404 expected
response = requests.delete(BASE + "fixtures/studio")
print(response.status_code, response.json())

# GET all home systems again, last one is deleted now
response = requests.get(BASE + "home")
pprint(response.json())

# PATCH Toggle off a light fixture
response = requests.patch(BASE + "fixtures/kitchen")
pprint(response.json())

# GET initial thermostat status
response = requests.get(BASE + "thermostat")
pprint(response.json())

# PATCH thermostat status
json = {"status": "on", "temp_setting": 69}
response = requests.patch(BASE + "thermostat", json=json)
pprint(response.json())

# PATCH -- it's too cold, turn it up a bit but still leave it on
response = requests.patch(BASE + "thermostat", json={"temp_setting": 71})
pprint(response.json())

# PATCH -- make an invalid change to temperature setting
requests.patch(BASE + "thermostat", json={"temp_setting": 81})

# PATCH -- make an invalid change to thermostatus
requests.patch(BASE + "thermostat", json={"status": "onff"})

# GET results to ensure expected vals after changes and failed changes
response = requests.get(BASE + "thermostat")
pprint(response.json())