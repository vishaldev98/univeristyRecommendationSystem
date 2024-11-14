import os
import joblib
import warnings
import pandas as pd

warnings.filterwarnings('ignore')


def perform_university_prediction_australia(data_frame):
    """
    Predicts the university based on given data for Australia model.

    Args:
        data_frame (pd.DataFrame): Input DataFrame containing the student's information.

    Returns:
        str: Predicted university name or None if there was an error.
    """
    try:
        # Import `read_excel` here to avoid circular import issues
        from base.com.controller.australia_class_name import read_excel

        # Validate input DataFrame
        if data_frame is None or data_frame.empty:
            raise ValueError("Input data frame is empty or invalid.")

        # Convert DataFrame to numpy array
        x_test = data_frame.to_numpy()

        # Define the model path (Adjust path if necessary)
        model_path = 'C:/Users/LIKHIT/Documents/SLU/PSD/Universityrecommendation/base/static/adminResources/models/Model_AUS.sav'

        # Check if the model file exists
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at '{model_path}'")

        # Load the model
        model_dump = joblib.load(model_path)
        print(f"Model loaded successfully from: {model_path}")

        # Perform prediction
        prediction = model_dump.predict(x_test)
        print(f"Predicted University ID(s): {prediction}")

        # Handle multiple predictions, if applicable
        predicted_universities = []
        for university_id in prediction:
            university_name = read_excel(university_id)
            if university_name is None:
                raise ValueError(f"University ID {university_id} not found in the dataset.")

            # Format the university name
            university_name = university_name.replace("_", " ")
            predicted_universities.append(university_name)

        # Display all predictions or single result
        result = ", ".join(predicted_universities)
        print(f"Predicted University(ies): {result}")
        return result

    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        return None
    except ValueError as e:
        print(f"Error: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None


# Sample data to test the function
sample_data = pd.DataFrame(
    [[320, 7.5, 3.5, 100, 2020, 2, 6, 1, 1]],
    columns=['GRE', 'IELTS', 'GPA', 'TOEFL', 'PassOutYear', 'WorkExp', 'InternshipMonth', 'ResearchPaper',
             'ConferenceAttend']
)

# Call the function with sample data
university_name = perform_university_prediction_australia(sample_data)
print("Predicted University:", university_name)
