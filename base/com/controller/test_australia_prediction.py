import warnings

import joblib

from base.com.controller.australia_class_name import read_data

warnings.filterwarnings('ignore')


def perform_university_prediction_australia(data_frame):
    x_test = data_frame.values
    model_dump = joblib.load('base/static/adminResources/models/Model_AUS.sav')
    prediction = model_dump.predict(x_test)
    print(prediction)
    university_id = prediction.tolist()[0]
    print(university_id)
    univeristy_name = (read_data(university_id)).replace("_", " ")
    print(univeristy_name)
    return univeristy_name
