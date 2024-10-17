import unittest
from unittest.mock import patch, MagicMock
from flask import Flask

# Import the app and functions we are testing
from base import app
from base.com.dao.country_dao import CountryDAO
from base.com.dao.login_dao import LoginDAO
from base.com.dao.user_dao import UserDAO
from base.com.vo.login_vo import LoginVO
from base.com.vo.user_vo import UserVO

class TestUserFunctions(unittest.TestCase):

    # Setup the Flask test client before each test
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    # Test user_load_user function
    @patch('base.com.dao.country_dao.CountryDAO.view_country')
    def test_user_load_user(self, mock_view_country):
        # Mock the return value for view_country
        mock_view_country.return_value = [{'country_id': 1, 'country_name': 'USA'}]

        # Simulate a GET request to the user/load_user route
        response = self.client.get('/user/load_user')

        # Verify that the function renders the correct template with the country list
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'addUser.html', response.data)
        mock_view_country.assert_called_once()

    # Test user_insert_user function
    @patch('base.com.dao.login_dao.LoginDAO.view_login')
    @patch('base.com.dao.login_dao.LoginDAO.insert_login')
    @patch('base.com.dao.user_dao.UserDAO.insert_user')
    @patch('smtplib.SMTP')
    @patch('random.choice')
    @patch('flask.request')
    def test_user_insert_user(self, mock_request, mock_random, mock_smtp, mock_insert_user, mock_insert_login, mock_view_login):
        # Mock form data
        mock_request.form = MagicMock()
        mock_request.form.get.side_effect = lambda key: {
            'loginUsername': 'testuser@example.com',
            'userFirstname': 'John',
            'userLastname': 'Doe',
            'userGender': 'Male',
            'userAddress': '123 Test Street',
            'userCountryId': '1'
        }[key]

        # Mock random string generation for password and secret key
        mock_random.side_effect = lambda seq: 'a'

        # Mock view_login to return an empty list (i.e., no duplicate login)
        mock_view_login.return_value = []

        # Mock the SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        # Simulate POST request to user/insert_user route
        response = self.client.post('/user/insert_user')

        # Check if the response redirects
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/')

        # Verify that the insert_login and insert_user methods were called
        mock_insert_login.assert_called_once()
        mock_insert_user.assert_called_once()

        # Verify that email was sent using SMTP
        mock_smtp.assert_called_once_with('smtp.gmail.com', 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("universityrecommendation6298@gmail.com", "Vi$h@l6298")
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()

    # Test user_insert_user when username already exists
    @patch('base.com.dao.login_dao.LoginDAO.view_login')
    @patch('flask.request')
    def test_user_insert_user_username_exists(self, mock_request, mock_view_login):
        # Mock form data
        mock_request.form = MagicMock()
        mock_request.form.get.side_effect = lambda key: {
            'loginUsername': 'testuser@example.com',
            'userFirstname': 'John',
            'userLastname': 'Doe',
            'userGender': 'Male',
            'userAddress': '123 Test Street',
            'userCountryId': '1'
        }[key]

        # Mock view_login to return a list containing a user with the same username
        mock_view_login.return_value = [LoginVO(login_username='testuser@example.com')]

        # Simulate POST request to user/insert_user route
        response = self.client.post('/user/insert_user')

        # Verify that the user is redirected back to the form with a flash message
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'The username is already exists !', response.data)


if __name__ == '__main__':
    unittest.main()
