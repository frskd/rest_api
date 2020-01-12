from flask import request
from flask_restful import Resource

from models import Ethnicity


class Ethnicities(Resource):
    def get(self):
        """
        Return a list of supported ethnicities: Array<{id: str, name: str}>
        """
        return [{"id": ethnicity.name, "name": ethnicity.value} for ethnicity in Ethnicity]
