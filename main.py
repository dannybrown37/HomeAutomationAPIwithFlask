import logging
import json
from flask import Flask, jsonify
from flask_restful import Api, Resource, abort, reqparse
from datetime import datetime



# Initialize app and API
app = Flask(__name__)
api = Api(app)


# Log user actions to file as configured 
handler = logging.FileHandler("user_actions.log")
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)


# Shorthand for calling later
now = datetime.now


# Functions to handle JSON reading and writing
def read_json_data(file_name="data.json"):
    with open(file_name, "r") as f:
        data = json.load(f)
    return data["fixtures"], data["thermostat"]


def write_json_data(fixtures, thermo):
    with open("data.json", "w") as f:
        json.dump({"fixtures": fixtures, "thermostat": thermo}, f, indent=4)


# Read in default data for initial run
fixtures, thermostat = read_json_data("default.json")



# # # API Endpoints # # #

class HomeSystem(Resource):
    
    def get(self):
        """ Use GET to see data for all systems currently in home. """
        app.logger.info(f"{now()} | Viewed home systems.")
        return jsonify({"fixtures": fixtures, "thermostat": thermostat})


class LightFixture(Resource):

    def get(self):
        """ Use to GET info on all fixtures or a particular fixture name. 
        
            Query param/JSON:
                name=fixture_name   -- GET specific fixture info
        """

        # Check JSON/query params for a particular fixture name
        args = fixture_get_args.parse_args()
        if args["name"]:
            name = args["name"]
            self.abort_if_no_matching_fixture(name)
            app.logger.info(f"{now()} | Viewed fixture '{name}'")
            return jsonify({name: fixtures[name]})
        
        # Otherwise return all fixtures
        app.logger.info(f"{now()} | Viewed all fixtures")
        return jsonify({"fixtures": fixtures})

    def post(self, name):
        """ Use to POST a new fixture to fixtures. 
        
            Query param/JSON:
                status=on -- to override default status of off
        """

        # Validate and log
        self.abort_if_fixture_already_exists(name)
        app.logger.info(f"{now()} | Added fixture '{name}'")

        # Handle optional query params/JSON
        args = fixture_post_args.parse_args()
        if args["status"] == "on":
            app.logger.info(f"{now()} | --> defaulted '{name}' to 'on'")

        # Add fixture to JSON structure
        fixtures[name] = {
            "status": "on" if args["status"] == "on" else "off", 
            "installed": now().strftime("%Y-%m-%d %H:%M")
        }

        # Output to JSON file (simulating a db save)
        write_json_data(fixtures, thermostat)

        return jsonify({name: fixtures[name]})

    def patch(self, name):
        """ Use PATCH to toggle the on/off status of a fixture. """
        
        # Validate
        self.abort_if_no_matching_fixture(name)
        
        # Toggle status from off->on or on->off
        status = fixtures[name]["status"]
        new = "on" if status == "off" else "off"
        fixtures[name]["status"] = new

        # Log action
        app.logger.info(f"{now()} | Toggled fixture '{name}' to '{new}'")
        
        # Output to JSON file (simulating a db save)
        write_json_data(fixtures, thermostat)

        return jsonify({name: fixtures[name]})
    
    def delete(self, name):
        """ Use to DELETE a fixture from fixtures. """

        # Validate then log
        self.abort_if_no_matching_fixture(name)
        app.logger.info(f"{now()} | Deleted fixture {name}")

        # Remove object
        del fixtures[name]

        # Output to JSON file (simulating a db save)
        write_json_data(fixtures, thermostat)
        
        return jsonify({"message": f"{name} fixture deleted successfully"})

    def abort_if_no_matching_fixture(self, fixture):
        """ Use to abort a connection with logging if fixture not found """
        msg = f"Failed to interact with non-existent fixture '{fixture}'"
        app.logger.info(f"{now()} | {msg}")
        if fixture not in fixtures:
            abort(404, message=f"{fixture} not in your fixtures")

    def abort_if_fixture_already_exists(self, fixture):
        """ Used to abort a connection with logging if fixture exists """
        msg = f"Failed to create duplicate fixture '{fixture}'"
        app.logger.info(f"{now()} | {msg}")
        if fixture in fixtures:
            abort(409, message=f"{fixture} already in your fixtures")


class Thermostat(Resource):

    def get(self):
        """ Use GET to return current thermostat readings. """
        app.logger.info(f"{now()} | Viewed thermostat readings.")
        return jsonify({"thermostat": thermostat})

    def patch(self):
        """ Use PATCH to change current thermostat settings.
        
            Query params/JSON:
                status = on/off (only)
                temp_setting = 60-80 inclusive (only)
        """

        args = thermostat_patch_args.parse_args()
        for arg, val in args.items():

            # Handle status changes
            if arg == "status": 

                # Make valid changes
                if val == "on" or val == "off":
                    thermostat["status"] = val
                    app.logger.info(f"{now()} | Turned thermostat '{val}'")

                # Log invalid change attempts but do not make changes
                elif val is not None:
                    msg = f"Sent invalid param '{val}' to 'status'"
                    app.logger.info(f"{now()} | {msg}")
                
            # Handle temp_setting change
            elif arg == "temp_setting":

                try:  # Avoid errors below, skip None values for this arg
                    int(val)
                except TypeError:
                    continue 

                # Make and log valid changes
                if 60 <= val <= 80:
                    thermostat["temp_setting"] = val
                    app.logger.info(f"{now()} | Set temp_setting to '{val}'")
                
                # Log invalid change attempts but do not make changes
                elif val is not None:
                    msg = f"Sent invalid param '{val}' to 'temp_setting'"
                    app.logger.info(f"{now()} | {msg}")

        # Output to JSON file (simulating a db save)
        write_json_data(fixtures, thermostat)

        # Return status of thermostat after changes (or non changes)
        return jsonify({"thermostat": thermostat})



# Request parser argument configurations
fixture_get_args = reqparse.RequestParser()
fixture_get_args.add_argument("name", type=str, help="Name of specific fixture")

fixture_post_args = reqparse.RequestParser()
fixture_post_args.add_argument("status", type=str, help="status=on")

thermostat_patch_args = reqparse.RequestParser()
thermostat_patch_args.add_argument("status", type=str, help="on/off")
thermostat_patch_args.add_argument("temp_setting", type=int, help="60 to 80")


# Add resources to API
api.add_resource(HomeSystem, "/home")
api.add_resource(LightFixture, "/fixtures", "/fixtures/<string:name>")
api.add_resource(Thermostat, "/thermostat")



if __name__ == "__main__":
    app.run(debug=True)