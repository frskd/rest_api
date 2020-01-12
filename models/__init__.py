from enum import Enum

import pickle
from pandas import DataFrame

from .us_states import USAState
from .ethnicities import Ethnicity
from .stop_types import StopType


def load_pickled_data(filename):
    with open(filename, "rb") as file:
        data = pickle.load(file)
        return data


def data_frame_from_input(us_state, hour_of_day, age, ethnicity, stop_type):
    features = ['state', 'hour', 'night', 'subject_age',
                'subject_race', 'subject_sex', 'type']
    inputs = [[
        us_state.name,
        hour_of_day,  # int 0-23
        False,  # night or day? not supported.
        age,  # int: 10 - 110 years old, inclusive
        ethnicity.value,
        "m",  # gender. not supported
        stop_type.name  # pedestrian or not
    ]]

    return DataFrame(inputs, columns=features)


encoder = load_pickled_data("models/pkl_data/testing_encoder.pkl")
model = load_pickled_data("models/pkl_data/gs_model.pkl")


def outcomes_for_data_frame(data_frame, encoder=encoder, model=model):
    endcoded_data = encoder.transform(data_frame)
    model_result = model.predict_proba(endcoded_data)
    zipped_result = zip(model.classes_, model_result[0])
    return dict(zipped_result)
