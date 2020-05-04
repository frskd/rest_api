import os

from flask import Flask
from dotenv import load_dotenv
from flask_restful import Resource, Api
from flask_cors import CORS

from resources import Locations, Ethnicities, OutcomesList, Outcomes

load_dotenv()


app = Flask(__name__)
CORS(app)
api = Api(app)


api.add_resource(Locations, "/locations")
api.add_resource(Ethnicities, "/ethnicities")
api.add_resource(OutcomesList, "/outcomes")
api.add_resource(Outcomes, "/outcomes/<location>")

if __name__ == "__main__":
    debug = os.getenv("DEBUG") == "true"
    port = int(os.getenv("PORT")) if os.getenv("PORT") else 5000
    app.run(debug=debug, port=port)
