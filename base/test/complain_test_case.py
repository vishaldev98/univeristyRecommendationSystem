import unittest
from base import app
from flask import request


class TestLoginSystem(unittest.TestCase):
    def setUp(self):
        # Set up the test client to use with Flask
        self.app = app.test_client()
        self.app.testing = True

    # Test case for rendering the login page
    def test_admin_load_login(self):
        response = self.app.get('/admin/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'login', response.data)  # Check if the login form is in the rendered template

    # Test case for invalid login attempt (wrong credentials)
    def test_admin_validate_login_invalid_credentials(self):
        response = self.app.post('/admin/validate_login',
                                 data=dict(loginUsername='wronguser', loginPassword='wrongpass'))
        self.assertEqual(response.status_code, 302)  # Should redirect after failure
        # Check for error message or related feedback in response headers or cookies
        self.assertIn('username or password is incorrect', response.headers.get('Set-Cookie', ''))

    # Test case for inactive user login attempt
    def test_admin_validate_login_inactive_user(self):
        response = self.app.post('/admin/validate_login',
                                 data=dict(loginUsername='inactiveuser', loginPassword='password'))
        self.assertEqual(response.status_code, 302)
        # Check for "temporarily blocked" message in response headers or cookies
        self.assertIn('You have been temporarily blocked', response.headers.get('Set-Cookie', ''))

    # Test case for successful admin login
    def test_admin_validate_login_successful_admin(self):
        response = self.app.post('/admin/validate_login', data=dict(loginUsername='admin', loginPassword='password'))
        self.assertEqual(response.status_code, 302)
        # Check if the cookies are properly set for admin
        self.assertIn('login_role=admin', response.headers.get('Set-Cookie', ''))
        self.assertIn('login_secretkey=admin_secret_key', response.headers.get('Set-Cookie', ''))

    # Test case for successful user login
    def test_admin_validate_login_successful_user(self):
        response = self.app.post('/admin/validate_login', data=dict(loginUsername='user', loginPassword='password'))
        self.assertEqual(response.status_code, 302)
        # Check if the cookies are properly set for user
        self.assertIn('login_role=user', response.headers.get('Set-Cookie', ''))
        self.assertIn('login_secretkey=user_secret_key', response.headers.get('Set-Cookie', ''))

    # Test case for loading admin dashboard after login
    def test_admin_load_dashboard(self):
        with self.app as c:
            c.set_cookie('localhost', 'login_secretkey', 'admin_secret_key')
            response = c.get('/admin/load_dashboard')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'admin', response.data)  # Check for dashboard content

    # Test case for loading user dashboard after login
    def test_user_load_dashboard(self):
        with self.app as c:
            c.set_cookie('localhost', 'login_secretkey', 'user_secret_key')
            response = c.get('/user/load_dashboard')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'user', response.data)  # Check for user dashboard content

    # Test case for invalid session (no secret key)
    def test_invalid_session(self):
        response = self.app.get('/admin/load_dashboard')
        self.assertEqual(response.status_code, 302)  # Redirect to login due to invalid session

    # Test case for logout functionality
    def test_admin_logout_session(self):
        with self.app as c:
            c.set_cookie('localhost', 'login_secretkey', 'admin_secret_key')
            c.set_cookie('localhost', 'login_username', 'admin')
            response = c.get('/admin/logout_session')
            self.assertEqual(response.status_code, 302)  # Should redirect to login after logout
            # Ensure that cookies have been cleared after logout
            self.assertNotIn('login_secretkey', response.headers.get('Set-Cookie', ''))
            self.assertNotIn('login_username', response.headers.get('Set-Cookie', ''))


if __name__ == '__main__':
    unittest.main()
