import warnings
import joblib
import pandas as pd
import numpy as np
import sklearn


# Check the scikit-learn version
print(f"scikit-learn version: {sklearn.__version__}")

# Mock function for read_data (replace this with your actual implementation)
def read_data(university_id):
    university_mapping = {1: "Harvard University", 2: "Stanford University", 3: "MIT"}
    return university_mapping.get(university_id, "Unknown University")

# Function to perform university prediction for USA
def perform_university_prediction_usa(data_frame):
    try:
        print(f"Input Data for Prediction: \n{data_frame}")
        print(f"Shape of Input Data: {data_frame.shape}")

        # Convert data frame to numpy array for model compatibility
        x_test = data_frame.values

        # Load the model
        model_path = 'C:/Users/LIKHIT/Documents/SLU/PSD/Universityrecommendation/base/static/adminResources/models/Model_AUS.sav'
        try:
            model_dump = joblib.load(model_path)
            print(f"Model loaded successfully from: {model_path}")
        except FileNotFoundError:
            print(f"Error: Model file not found at '{model_path}'.")
            return "Model file not found."
        except Exception as e:
            print(f"Error loading the model: {e}")  # Print the full error
            return f"Error loading model: {e}"  # Return the full error message

        # Make a prediction
        try:
            prediction = model_dump.predict(x_test)
            print(f"Prediction result (raw): {prediction}")
        except Exception as e:
            print(f"Error making prediction: {e}")
            return "Error making prediction."

        if isinstance(prediction, (list, np.ndarray)) and len(prediction) > 0:
            university_id = prediction[0]
            print(f"Predicted University ID: {university_id}")
        else:
            print("Prediction is empty or in an unexpected format.")
            return "No prediction available"

        try:
            university_name = read_data(university_id).replace("_", " ")
            print(f"Predicted University Name: {university_name}")
        except Exception as e:
            print(f"Error retrieving university name for ID {university_id}: {e}")
            return "Error retrieving university name."

        return university_name

    except ValueError as ve:
        print(f"Value Error: {ve}")
        return "Invalid input data format."
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred."

# Example test data frame with expected features
sample_data = pd.DataFrame([[ 7.5, 3.5, 100, 2020, 2, 6, 1, 1]],
                           columns=[ 'IELTS', 'GPA', 'TOEFL', 'PassOutYear',
                                    'WorkExp', 'InternshipMonth', 'ResearchPaper', 'ConferenceAttend'])

# Call the function with sample data
university_name = perform_university_prediction_usa(sample_data)
print("Predicted University:", university_name)
