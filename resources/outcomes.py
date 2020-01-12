from flask import request
from flask_restful import Resource

from models import Ethnicity, StopType, USAState, data_frame_from_input, outcomes_for_data_frame

from .outcomes_schema import OutcomeSchema


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
