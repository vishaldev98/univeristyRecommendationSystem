import pytest
from base import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_user_load_prediction(client, mocker):
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="user")
    response = client.get('/user/load_prediction')
    assert response.status_code == 200
    assert b'Add Prediction' in response.data  # Check for form in HTML response

def test_user_insert_prediction(client, mocker):
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="user")
    mocker.patch('base.com.dao.login_dao.LoginDAO.find_login_id', return_value=1)
    mocker.patch('base.com.dao.prediction_dao.PredictionDAO.insert_prediction')
    mock_prediction = mocker.patch('base.com.controller.test_usa_prediction.perform_university_prediction_usa', return_value="Mocked University")

    data = {
        "predictionGre": "320",
        "predictionIelts": "7.5",
        "predictionGpaScore": "3.5",
        "predictionToefl": "105",
        "predictionPassOutYear": "2022",
        "predictionWorkExperience": "2",
        "predictionInternshipMonth": "6",
        "predictionResearchPaper": "1",
        "predictionConferenceAttend": "1",
        "predictionCountry": "USA"
    }
    response = client.post('/user/insert_prediction', data=data)
    assert response.status_code == 302  # Check for redirect
    mock_prediction.assert_called_once()  # Ensure prediction function is called

def test_user_view_prediction(client, mocker):
    mocker.patch('base.com.controller.login_controller.admin_login_session', return_value="user")
    mocker.patch('base.com.dao.login_dao.LoginDAO.find_login_id', return_value=1)
    mock_view_prediction = mocker.patch('base.com.dao.prediction_dao.PredictionDAO.view_prediction')
    mock_view_prediction.return_value = []  # Dummy data

    response = client.get('/user/view_prediction')
    assert response.status_code == 200
    assert b'No Predictions Found' in response.data  # Adjust to match HTML text for empty predictions
