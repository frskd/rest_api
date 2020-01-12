from models import USAState, Ethnicity, StopType, data_frame_from_input, outcomes_for_data_frame

inputs = data_frame_from_input(
    USAState("arizona"), 12, 16, Ethnicity("black"), StopType(1))
outcomes = outcomes_for_data_frame(inputs)
print(outcomes)

# GET /locations Return a list of supported USA states: id, state_name

# GET /ethnicities Returns a list of supported ethnicities:
# white, hispanic, not_listed, black, asian/pacific islander, unspecified

# GET /outcomes Return outcomes data for each supported USA state

# GET /outcomes/<str:locationId> Return outcomes data for a given state
# Query Params:
# hour_of_day: int - Between 0 and 23, inclusive (Defaults to 12)
# age: int - Between 10 and 110. (Defaults to 16)
# is_pedestrian_stop: bool - Vehicular or pedestrian stop. (Defaults to false)
# ethnicityId: int - Ethnicity Id. (Default to unspecified)
