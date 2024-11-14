import warnings
import joblib
import numpy as np

from base.com.controller.canada_class_name import read_data

warnings.filterwarnings('ignore')


def perform_university_prediction_canada(data_frame):
    try:
        # Ensure the data is in the correct shape for the model
        print(f"Input Data for Prediction: \n{data_frame}")
        print(f"Shape of Input Data: {data_frame.shape}")

        x_test = data_frame.values

        # Load the model
        try:
            model_dump = joblib.load('base/static/adminResources/models/Model_Canada.sav')
            print("Model loaded successfully.")
        except FileNotFoundError:
            print("Model file not found at the specified path.")
            return None

        # Make a prediction
        prediction = model_dump.predict(x_test)
        print(f"Prediction: {prediction}")

        # Ensure prediction is in the correct format
        if isinstance(prediction, list) or isinstance(prediction, np.ndarray):
            university_id = prediction.tolist()[0]
            print(f"Predicted University ID: {university_id}")
        else:
            print(f"Unexpected prediction format: {type(prediction)}")
            return None

        # Get the university name by calling read_data with the ID
        university_name = read_data(university_id).replace("_", " ")
        print(f"Predicted University Name: {university_name}")

        return university_name

    except FileNotFoundError:
        print("Model file not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
