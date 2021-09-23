
# The Home Automation Flask API

Welome to my crash-course in Flask API building. I've mostly spent time with
Django and have only cursory prior experience with Flask, and this is my first
time using the `flask_restful` module, but I had a great experience reading 
documentation and getting more familiar with these libraries in this project.

Using `flask_restful` was a fun deviation from the seemingly more traditional
method of using the `@app.route` decorator combined with defining functions 
and if/elif logic to handle different types of requests.

## Application Overview

This is a simple CRUD application providing API endpoints that allow users
to control home systems – in this example case, adding/removing/controlling
light fixtures and changing thermostat settings.

To run the application locally, do the following:

1. `pip install -r requirements.txt` in your virtual environment
2. Run `main.py` to run the Flask development server
3. In a separate console, run `tests.py` to ensure all calls work correctly.
4. All calls are logged in `user_actions.log`

All relevant code (except for tests) is found in `main.py`.

## API Endpoints

When running locally as instructed above, the root URL is:
`http://127.0.0.1:5000/`

### Home System Status Endpoint

**GET /home**

Get information on all home systems.

	No parameters.

**Returns**: A JSON object showing all light fixtures and their settings as well as the current thermostat settings/readings.

Sample Response
```
GET /home

{
	'fixtures': {
		'bathroom': {'installed': '2021-09-23 14:06', 'status': 'off'},
		'bedroom': {'installed': '2021-09-23 14:06', 'status': 'on'},
		'kitchen': {'installed': '2021-09-23 14:06', 'status': 'on'},
		'office': {'installed': '2021-09-23 14:06', 'status': 'off'}
	},
	'thermostat': {
		'current_temp': 75, 
		'status': 'off', 
		'temp_setting': 73
	}
}

```
### Light Fixture Endpoints

**GET /fixtures**

Get information on all fixtures or a specific fixture.

**Parameter**:  

	name (str) – The name of the fixture you want information on.
		       	 Optional. Will return all fixtures if not sent.  

**Raises**: 404 if no matching fixture to `name` param

**Returns**: A JSON object showing fixture information as requested.

Sample Response 1
```
GET /fixtures
{
	'fixtures': {
		'bathroom': {'installed': '2021-09-23 14:06', 'status': 'off'},
		'bedroom': {'installed': '2021-09-23 14:06', 'status': 'on'},
		'kitchen': {'installed': '2021-09-23 14:06', 'status': 'on'},
		'office': {'installed': '2021-09-23 14:06', 'status': 'off'}
}
```
Sample Response 2
```
GET /fixtures?name=kitchen
{
	'kitchen': {
		'installed': '2021-09-23 14:06', 
		'status': 'on'
	}
}
```
**POST /fixtures/\<name:str\>**

Add a new fixture to your home.

**Parameter**:

	status (str) – Optional. Default status is off. Send `on` to default to on.

**Raises**: 409 if fixture with `name` already exists  

**Returns**: A JSON object showing information on the added fixture.

Sample Response 1
```
POST /fixtures/bedroom
{
	'bedroom': {
		'installed': '2021-09-23 14:06', 
		'status': 'off'
	}
}
```
Sample Response 2
```
POST /fixtures/bedroom?status=on
{
	'bedroom': {
		'installed': '2021-09-23 14:06', 
		'status': 'on'
	}
}
```
**PATCH /fixtures/\<name:str\>**

Toggle the on/off status of the specified fixture.

	No parameters.

**Raises**: 404 if no matching fixture to `name`

**Returns**: A JSON object of the fixture with the `status` toggled.

Sample Response
```
PATCH /fixtures/bedroom # assuming bedroom `status` is `on`
{
	'bedroom': {
		'installed': '2021-09-23 14:06', 
		'status': 'off'
	}
}
```
**DELETE /fixtures/\<name:str\>**

Delete a fixture as specified.

	No parameters.

**Raises**: 404 if no matching fixture to `name`

**Returns**: A JSON object with a "successfully deleted" message.

Sample Response
```
DELETE /fixtures/bathroom
{
	'message': 'bathroom fixture deleted successfully'
}
```

### Thermostat Endpoints

**GET /thermostat**

Return current thermostat settings.

	No parameters.

**Returns**: A JSON object with current thermostat settings.

Sample Response
```
GET /thermostat
{
	'thermostat': {
		'current_temp': 75, 
		'status': 'on', 
		'temp_setting': 69
	}
}

```
**PATCH /thermostat**

Update thermostat status or current temperature setting.

**Parameters**:

	(Parameters are both optional, but no action will be taken from the 
	 request if at least one parameter is not sent.)

	status (str) – Accepts on or off.

	temp_setting (int) – Accepts 60-80 inclusive.

  
**Returns**: A JSON object with new thermostat settings.

Sample Response 1
```
GET /thermostat?status=off&temp_setting=73
	{
		'thermostat': {
			'current_temp': 75, 
			'status': 'off', 
			'temp_setting': 73
		}
	}
```
Sample Response 2
```
GET /thermostat?status=on
	{
		'thermostat': {
			'current_temp': 75, 
			'status': 'on', 
			'temp_setting': 73
		}
	}
```
Sample Response 3
```
GET /thermostat?temp_setting=74
	{
		'thermostat': {
			'current_temp': 75, 
			'status': 'on', 
			'temp_setting': 74
		}
	}
```