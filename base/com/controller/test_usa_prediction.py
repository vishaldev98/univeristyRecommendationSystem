import joblib
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder


# Model loading function with error handling
def load_model(model_path):
    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            print(f"Model loaded successfully from: {model_path}")
            return model
        except Exception as e:
            print(f"Error loading model from {model_path}: {e}")
            return None
    else:
        print(f"Model file not found at {model_path}")
        return None


# Input data validation function
def check_input_data(data):
    if isinstance(data, pd.DataFrame):
        print("Input data is a DataFrame")
        print("Shape of data:", data.shape)
        print("Data types of columns:", data.dtypes)
    else:
        print("Input data is not a DataFrame.")

    # Check the number of features in the input data
    expected_features = 9  # The model expects 9 features
    if data.shape[1] != expected_features:
        print(f"Error: Expected {expected_features} features, but got {data.shape[1]} features.")
        return False
    return True


# Test the model on dummy data to ensure it's predicting correctly
def test_model_predictions(model, dummy_data):
    if model:
        try:
            prediction = model.predict(dummy_data)
            print(f"Test prediction result: {prediction}")
            return prediction
        except Exception as e:
            print(f"Error during prediction: {e}")
            return None
    else:
        print("No model loaded. Cannot perform prediction.")
        return None


# Verify the prediction output
def verify_prediction(prediction):
    if prediction is not None and len(prediction) > 0:
        print(f"Prediction successful: {prediction}")
        return prediction
    else:
        print("Prediction failed: Invalid output.")
        return None


# Example: Perform university prediction for USA
def perform_university_prediction_usa(data_frame):
    try:
        # Load the USA model
        model_path = 'C:/Users/LIKHIT/Documents/SLU/PSD/Universityrecommendation/base/static/adminResources/models/Model_USA.sav'
        model = load_model(model_path)

        if model is None:
            return "Error loading model."

        # Ensure input data is valid
        if not check_input_data(data_frame):
            return "Invalid input data."

        # Test the model with dummy data
        dummy_data = np.array([[320, 7.5, 3.5, 100, 2020, 2, 6, 1, 1]])  # Example dummy data
        test_model_predictions(model, dummy_data)

        # Make the prediction
        prediction = model.predict(data_frame)
        prediction = verify_prediction(prediction)

        if prediction is None:
            return "Error making prediction."

        # Convert numeric prediction back to university name
        # You should use the same LabelEncoder (`le1`) that was used during model training
        le1 = LabelEncoder()
        le1.fit(pd.read_excel(
            'C:/Users/LIKHIT/Documents/SLU/PSD/Universityrecommendation/base/static/adminResources/dataset/Dataset_USA.xlsx')[
                    'UNIVERSITY'].astype(str))

        university_name = le1.inverse_transform(prediction)  # Convert the numeric label to university name
        return university_name

    except Exception as e:
        print(f"Error in prediction: {e}")
        return "Error during prediction."


# Example usage of the function
if __name__ == "__main__":
    # Sample input data for USA model
    sample_data = pd.DataFrame([[320, 7.5, 3.5, 100, 2020, 2, 6, 1, 1]],  # Including all 9 features
                               columns=['GRE', 'IELTS', 'GPA', 'TOEFL', 'PassOutYear', 'WorkExp', 'InternshipMonth',
                                        'ResearchPaper', 'ConferenceAttend'])

    # Call the prediction function
    university_name = perform_university_prediction_usa(sample_data)
    print(f"Predicted University: {university_name}")
