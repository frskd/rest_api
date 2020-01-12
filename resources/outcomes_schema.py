from marshmallow import fields, validates, Schema

from models import Ethnicity, USAState


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
        if not USAState(location):
            raise ValidationError(
                f"Location must be one of: {' | '.join([l.value for l in USAState])}")
