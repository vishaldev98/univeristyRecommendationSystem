import pytest
from flask import url_for
from base import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_user_load_user(client, mocker):
    # Mock the CountryDAO to provide a list of countries
    mock_country_dao = mocker.patch('base.com.dao.country_dao.CountryDAO.view_country')
    mock_country_dao.return_value = []

    response = client.get('/user/load_user')
    assert response.status_code == 200
    assert b'Add User' in response.data  # Modify based on page content

def test_user_insert_user(client, mocker):
    # Mock DAOs
    mock_login_dao = mocker.patch('base.com.dao.login_dao.LoginDAO')
    mock_user_dao = mocker.patch('base.com.dao.user_dao.UserDAO')

    # Mock the login DAO to check existing users and handle insertion
    mock_login_dao_instance = mock_login_dao.return_value
    mock_login_dao_instance.view_login.return_value = []  # No existing users

    # Mock the email sending
    mock_smtp = mocker.patch('smtplib.SMTP')
    mock_server_instance = mock_smtp.return_value
    mock_server_instance.sendmail.return_value = None

    # Sample form data
    data = {
        'loginUsername': 'testuser@example.com',
        'userFirstname': 'Test',
        'userLastname': 'User',
        'userGender': 'Male',
        'userAddress': '123 Test St',
        'userCountryId': '1'
    }

    # Run the function
    response = client.post('/user/insert_user', data=data)

    # Assertions
    assert response.status_code == 302  # Should redirect on success
    assert mock_login_dao_instance.insert_login.called  # Check that login was inserted
    assert mock_user_dao.return_value.insert_user.called  # Check that user was inserted
    assert mock_smtp.called  # Check that email was sent

def test_user_insert_user_username_conflict(client, mocker):
    # Mock DAOs
    mock_login_dao = mocker.patch('base.com.dao.login_dao.LoginDAO')
    mock_user_dao = mocker.patch('base.com.dao.user_dao.UserDAO')

    # Mock login DAO to return an existing user with the same username
    mock_login_dao_instance = mock_login_dao.return_value
    mock_login_dao_instance.view_login.return_value = [{'login_username': 'testuser@example.com'}]

    # Sample form data with a conflicting username
    data = {
        'loginUsername': 'testuser@example.com',  # This username already exists
        'userFirstname': 'Test',
        'userLastname': 'User',
        'userGender': 'Male',
        'userAddress': '123 Test St',
        'userCountryId': '1'
    }

    response = client.post('/user/insert_user', data=data, follow_redirects=True)
    assert response.status_code == 200  # Page reloads with error message
    assert b"The username is already exists !" in response.data  # Modify based on error message content

def test_user_insert_user_email_failure(client, mocker):
    # Mock DAOs
    mock_login_dao = mocker.patch('base.com.dao.login_dao.LoginDAO')
    mock_user_dao = mocker.patch('base.com.dao.user_dao.UserDAO')

    # Mock the login DAO to check existing users and handle insertion
    mock_login_dao_instance = mock_login_dao.return_value
    mock_login_dao_instance.view_login.return_value = []  # No existing users

    # Mock email sending to simulate failure
    mock_smtp = mocker.patch('smtplib.SMTP')
    mock_server_instance = mock_smtp.return_value
    mock_server_instance.sendmail.side_effect = smtplib.SMTPException("Email failed")

    # Sample form data
    data = {
        'loginUsername': 'testuser@example.com',
        'userFirstname': 'Test',
        'userLastname': 'User',
        'userGender': 'Male',
        'userAddress': '123 Test St',
        'userCountryId': '1'
    }

    # Run the function
    response = client.post('/user/insert_user', data=data)

    # Assertions
    assert response.status_code == 500  # Internal server error due to email failure
    assert mock_smtp.called  # Check that email sending was attempted
