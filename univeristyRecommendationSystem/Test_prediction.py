import pytest
from flask import Flask
from base import app, db  # Assuming db is your database instance

@pytest.fixture
def client():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['login_username'] = 'testuser'  # Mock login for authenticated tests
        yield client

# Test for /user/load_prediction
def test_user_load_prediction_authenticated(client):
    response = client.get('/user/load_prediction')
    assert b"Add Prediction" in response.data  # Check if prediction form is displayed

def test_user_load_prediction_not_authenticated():
    with app.test_client() as client:
        response = client.get('/user/load_prediction')
        assert b"Logout" in response.data  # Ensure logout is triggered

# Parameterized test for /user/insert_prediction
@pytest.mark.parametrize("data, expected_status", [
    ({
        'predictionGre': 320,
        'predictionIelts': 7.5,
        'predictionGpaScore': 3.8,
        'predictionToefl': 100,
        'predictionPassOutYear': 2024,
        'predictionWorkExperience': 2,
        'predictionInternshipMonth': 12,
        'predictionResearchPaper': 1,
        'predictionConferenceAttend': 1,
        'predictionCountry': 'USA'
    }, 302),
    ({
        'predictionGre': '',  # Invalid data
        'predictionIelts': 7.5,
        'predictionGpaScore': 3.8,
        'predictionToefl': 100,
        'predictionPassOutYear': 2024,
        'predictionWorkExperience': 2,
        'predictionInternshipMonth': 12,
        'predictionResearchPaper': 1,
        'predictionConferenceAttend': 1,
        'predictionCountry': 'USA'
    }, 400)  # Expecting a bad request status for invalid input
])
def test_user_insert_prediction(client, data, expected_status):
    response = client.post('/user/insert_prediction', data=data)
    assert response.status_code == expected_status

# Test for /user/view_prediction
def test_user_view_prediction_authenticated(client):
    response = client.get('/user/view_prediction')
    assert b"View Your Predictions" in response.data  
    assert b"Prediction for USA" in response.data  

def test_user_view_prediction_not_authenticated():
    with app.test_client() as client:
        response = client.get('/user/view_prediction')
        assert b"Logout" in response.data  

# Test for invalid session handling
def test_invalid_session_handling():
    with app.test_client() as client:
        response = client.get('/user/load_prediction')
        assert b"Logout" in response.data  

# Test database insertion (ensure that prediction data is inserted into DB)
def test_database_insertion(client):
    prediction_data = {
        'predictionGre': 320,
        'predictionIelts': 7.5,
        'predictionGpaScore': 3.8,
        'predictionToefl': 100,
        'predictionPassOutYear': 2024,
        'predictionWorkExperience': 2,
        'predictionInternshipMonth': 12,
        'predictionResearchPaper': 1,
        'predictionConferenceAttend': 1,
        'predictionCountry': 'USA'
    }
    
    # Insert prediction
    client.post('/user/insert_prediction', data=prediction_data)

    # Verify that the prediction was inserted into the database
    prediction = db.session.query(Prediction).filter_by(predictionCountry='USA').first()
    assert prediction is not None
    assert prediction.predictionGre == prediction_data['predictionGre']
    assert prediction.predictionIelts == prediction_data['predictionIelts']
