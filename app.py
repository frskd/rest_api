from flask import Flask
from flask_restful import Resource, Api

from resources import Locations, Ethnicities, OutcomesList, Outcomes


app = Flask(__name__)
api = Api(app)


api.add_resource(Locations, "/locations")
api.add_resource(Ethnicities, "/ethnicities")
api.add_resource(OutcomesList, "/outcomes")
api.add_resource(Outcomes, "/outcomes/<location>")

if __name__ == "__main__":
    app.run(debug=True)
