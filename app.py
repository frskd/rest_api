from flask import Flask
from flask_restful import Resource, Api

from models import USAState, Ethnicity, StopType, data_frame_from_input, outcomes_for_data_frame

app = Flask(__name__)
api = Api(app)


class Locations(Resource):
    def get(self):
        """
        Return a list of supported USA states: Array<{id: str, name: str}>
        """
        return [{"id": state.name, "name": state.value} for state in USAState]


class Ethnicities(Resource):
    def get(self):
        """
        Return a list of supported ethnicities: Array<{id: str, name: str}>
        """
        return [{"id": ethnicity.name, "name": ethnicity.value} for ethnicity in Ethnicity]

# GET /outcomes Return outcomes data for each supported USA state

# GET /outcomes/<str:locationId> Return outcomes data for a given state
# Query Params:
# hour_of_day: int - Between 0 and 23, inclusive (Defaults to 12)
# age: int - Between 10 and 110. (Defaults to 16)
# is_pedestrian_stop: bool - Vehicular or pedestrian stop. (Defaults to false)
# ethnicityId: int - Ethnicity Id. (Default to unspecified)


api.add_resource(Locations, "/locations")
api.add_resource(Ethnicities, "/ethnicities")

if __name__ == "__main__":
    app.run(debug=True)
    inputs = data_frame_from_input(
        USAState("arizona"), 12, 16, Ethnicity("black"), StopType(1))
    outcomes = outcomes_for_data_frame(inputs)
