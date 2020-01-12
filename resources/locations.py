from flask import request
from flask_restful import Resource

from models import USAState


class Locations(Resource):
    def get(self):
        """
        Return a list of supported USA states: Array<{id: str, name: str}>
        """
        return [{"id": state.name, "name": state.value} for state in USAState]
