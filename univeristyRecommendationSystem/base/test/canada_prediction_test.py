import pytest
import pandas as pd
from unittest import mock
from base.com.controller.canada_prediction import perform_university_prediction_canada


def test_perform_university_prediction_canada(mocker):
    # Sample test data
    data_frame = pd.DataFrame([[320, 7.5, 3.5, 2022, 2, 6, 1, 1]],
                              columns=['GRE', 'IELTS', 'GPA', 'PassOutYear', 'WorkExp',
                                       'InternshipMonth', 'ResearchPaper', 'ConferenceAttend'])

    # Mock the model loading and prediction
    mock_model = mocker.MagicMock()
    mock_model.predict.return_value = [2]  # Simulate a prediction of university ID 2
    mocker.patch('joblib.load', return_value=mock_model)

    # Mock the read_data function to simulate university name retrieval
    mock_read_data = mocker.patch('base.com.controller.canada_class_name.read_data',
                                  return_value="University_of_Canada_Test")

    # Run the function
    result = perform_university_prediction_canada(data_frame)

    # Assertions
    mock_model.predict.assert_called_once_with(
        data_frame.values)  # Ensure the model's predict method is called with correct data
    mock_read_data.assert_called_once_with(2)  # Ensure read_data is called with the correct ID
    assert result == "University of Canada Test"  # Verify the returned university name is correctly formatted
