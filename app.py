import json
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from marshmallow import Schema, fields, pprint, ValidationError, validates

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


class OutcomeSchema(Schema):
    hour_of_day = fields.Integer(
        required=True)
    age = fields.Integer(required=True)
    is_pedestrian_stop = fields.Boolean(required=True)
    ethnicity = fields.String(required=True)
    location = fields.String()

    @validates("hour_of_day")
    def validate_hour_of_day(self, hour):
        if hour < 0:
            raise ValidationError(
                "Hour of day must be greater than or equal to 0")
        if hour > 23:
            raise ValidationError("Hour of day must be less than 24")

    @validates("age")
    def validate_age(self, age):
        if age < 10:
            raise ValidationError("Age must be greater than or equal to 10")
        if age > 110:
            raise ValidationError("Age must be less than 111")

    @validates("ethnicity")
    def validate_ethnicity(self, ethnicity):
        if not Ethnicity(ethnicity):
            raise ValidationError(
                f"Ethnicity must be one of: {' | '.join([e.value for e in Ethnicity])}")

    @validates("location")
    def validate_location(self, location):
        if not Locations(location):
            raise ValidationError(
                f"Location must be one of: {' | '.join([l.value for l in Locations])}")


class OutcomesList(Resource):

    def get(self):
        """
        Return outcomes data for each supported USA state
        """
        query_params = request.args
        query_json = OutcomeSchema().load(query_params)

        outcomes = []
        for state in USAState:
            data_frame = data_frame_from_input(
                state,
                query_json["hour_of_day"],
                query_json["age"],
                Ethnicity(query_json["ethnicity"]),
                StopType(
                    1) if query_json["is_pedestrian_stop"] else StopType(2)
            )
            outcomes_data = outcomes_for_data_frame(data_frame)
            outcomes_data["location"] = state.value
            outcomes.append(outcomes_data)

        return outcomes


class Outcomes(Resource):

    def get(self, location):
        """
        Return outcomes data for a given US state
        """
        query_params = request.args
        query_json = OutcomeSchema().load(query_params)

        data_frame = data_frame_from_input(
            USAState(location),
            query_json["hour_of_day"],
            query_json["age"],
            Ethnicity(query_json["ethnicity"]),
            StopType(
                1) if query_json["is_pedestrian_stop"] else StopType(2)
        )
        outcomes = outcomes_for_data_frame(data_frame)

        return outcomes


api.add_resource(Locations, "/locations")
api.add_resource(Ethnicities, "/ethnicities")
api.add_resource(OutcomesList, "/outcomes")
api.add_resource(Outcomes, "/outcomes/<location>")

if __name__ == "__main__":
    app.run(debug=True)
