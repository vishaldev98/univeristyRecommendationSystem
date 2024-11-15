import pytest
from flask import Flask
from base import app

# Test for /user/load_prediction
def test_user_load_prediction_authenticated():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['login_username'] = 'testuser'  # Mock login
        response = client.get('/user/load_prediction')
        assert b"Add Prediction" in response.data  # Check if prediction form is displayed

def test_user_load_prediction_not_authenticated():
    with app.test_client() as client:
        response = client.get('/user/load_prediction')
        assert b"Logout" in response.data  # Ensure logout is triggered

# Test for /user/insert_prediction
def test_user_insert_prediction_valid_data():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['login_username'] = 'testuser'  # Mock login
        response = client.post('/user/insert_prediction', data={
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
        })
        assert response.status_code == 302  # Redirection to '/user/view_prediction'
        assert '/user/view_prediction' in response.location  # Check redirection

# Test for /user/view_prediction
def test_user_view_prediction_authenticated():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['login_username'] = 'testuser'  # Mock login
        response = client.get('/user/view_prediction')
        assert b"View Your Predictions" in response.data  # Ensure predictions page is displayed
        assert b"Prediction for USA" in response.data  # Check if predictions for USA are displayed

def test_user_view_prediction_not_authenticated():
    with app.test_client() as client:
        response = client.get('/user/view_prediction')
        assert b"Logout" in response.data  # Ensure logout is triggered

# Test for invalid session handling
def test_invalid_session_handling():
    with app.test_client() as client:
        response = client.get('/user/load_prediction')
        assert b"Logout" in response.data  # Ensure logout occurs when no session is active

# Test database insertion (ensure that prediction data is inserted into DB)
def test_database_insertion():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['login_username'] = 'testuser'  # Mock login
        client.post('/user/insert_prediction', data={
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
        })
        # You can add a query to the DB or mock the DAO layer to check if the data was inserted correctly
        # For example: check if the data exists in the mock DB or assert on specific conditions

