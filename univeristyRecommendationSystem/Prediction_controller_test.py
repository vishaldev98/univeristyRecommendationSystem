from flask import Flask, redirect, session, url_for
from flask_testing import TestCase
import unittest
from unittest import mock

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'testsecret'

# Define the index route to resolve 'index' endpoint issues in tests
@app.route('/')
def index():
    return 'Welcome to the Home Page'

# Protected route that requires login
@app.route('/protected')
def protected():
    if 'username' not in session:
        return redirect(url_for('logout'))
    return 'Protected Content'

# Logout route that clears the session and redirects to the index
@app.route('/admin/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Define the Test Case
class MyTestCase(TestCase):

    # Set up the testing environment
    def create_app(self):
        app.config['TESTING'] = True
        return app

    # Test that a user is redirected when they are not logged in
    @mock.patch('flask.session.get')
    def test_redirect_on_invalid_session(self, mock_session):
        # Simulate no user session (i.e., the user is not logged in)
        mock_session.return_value = None  # Simulate 'username' not in session
        response = self.client.get('/protected')
        # Adjust comparison to relative path only
        self.assertRedirects(response, url_for('logout', _external=False))

    # Test that a logged-in user gets access to the protected route
    @mock.patch('flask.session.get')
    def test_protected_access_with_session(self, mock_session):
        # Simulate a logged-in session
        mock_session.return_value = 'testuser'  # Simulate 'username' being present in session
        response = self.client.get('/protected')
        self.assertEqual(response.status_code, 302)
        self.assertIn('Protected Content', response.data.decode())

    # Test that the logout works as expected and redirects to index
    def test_logout(self):
        with self.client:
            # Simulate a logged-in session (e.g., user is logged in)
            session['username'] = 'tester'
            response = self.client.get('/admin/logout')
            # Adjust comparison to relative path only
            self.assertRedirects(response, url_for('index', _external=False))

# Run the tests
if __name__ == "__main__":
    unittest.main()
