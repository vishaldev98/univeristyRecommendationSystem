import pytest
import pandas as pd
from unittest import mock
from base.com.controller.australia_prediction import perform_university_prediction_australia


# Test for perform_university_prediction_australia function
def test_perform_university_prediction_australia(mocker):
    # Sample test data
    data_frame = pd.DataFrame([[7.5, 105, 3.5, 2022, 2, 6, 1, 1]],
                              columns=['IELTS', 'TOFEL', 'GPA', 'PassOutYear', 'WorkExp',
                                       'InternshipMonth', 'ResearchPaper', 'ConferenceAttend'])

    # Mock the model loading
    mock_model = mocker.MagicMock()
    mock_model.predict.return_value = [1]  # Simulate a prediction of university ID 1
    mocker.patch('joblib.load', return_value=mock_model)

    # Mock read_data function
    mock_read_data = mocker.patch('base.com.controller.australia_class_name.read_data',
                                  return_value="University_of_Test")

    # Run the function
    result = perform_university_prediction_australia(data_frame)

    # Assertions
    mock_model.predict.assert_called_once()  # Ensure the model's predict method is called once
    mock_read_data.assert_called_once_with(1)  # Ensure read_data is called with the correct ID
    assert result == "University of Test"  # Verify the returned university name is correctly formatted
