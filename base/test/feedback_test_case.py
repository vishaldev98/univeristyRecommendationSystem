import unittest
from base import app
from unittest.mock import patch
from flask import request


class TestFeedbackSystem(unittest.TestCase):
    def setUp(self):
        # Set up the test client to use with Flask
        self.app = app.test_client()
        self.app.testing = True

    # Test case for admin viewing feedback
    @patch('base.com.dao.feedback_dao.FeedbackDAO.admin_view_feedback')
    @patch('base.com.controller.login_controller.admin_login_session', return_value='admin')
    def test_admin_view_feedback(self, mock_login_session, mock_admin_view_feedback):
        mock_admin_view_feedback.return_value = []  # Mock an empty feedback list
        response = self.app.get('/admin/view_feedback')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Feedback', response.data)  # Check if feedback page is rendered

    # Test case for admin deleting feedback
    @patch('base.com.dao.feedback_dao.FeedbackDAO.delete_feedback')
    @patch('base.com.controller.login_controller.admin_login_session', return_value='admin')
    def test_admin_delete_feedback(self, mock_login_session, mock_delete_feedback):
        response = self.app.get('/admin/delete_feedback?feedbackId=1')
        self.assertEqual(response.status_code, 302)  # Expect redirect after deletion
        self.assertIn('/admin/view_feedback', response.headers['Location'])  # Check for redirection to view feedback

    # Test case for user loading feedback form (redirects to view feedback page)
    @patch('base.com.controller.login_controller.admin_login_session', return_value='user')
    def test_user_load_feedback(self, mock_login_session):
        response = self.app.get('/user/load_feedback')
        self.assertEqual(response.status_code, 302)  # Expect redirect
        self.assertIn('/user/view_feedback', response.headers['Location'])  # Check redirection to user feedback page

    # Test case for user inserting feedback
    @patch('base.com.dao.feedback_dao.FeedbackDAO.insert_feedback')
    @patch('base.com.dao.login_dao.LoginDAO.find_login_id', return_value=1)
    @patch('base.com.controller.login_controller.admin_login_session', return_value='user')
    def test_user_insert_feedback(self, mock_login_session, mock_find_login_id, mock_insert_feedback):
        response = self.app.post('/user/insert_feedback', data=dict(rating='5', feedbackDescription='Great service!'))
        self.assertEqual(response.status_code, 302)  # Expect redirect after feedback submission
        self.assertIn('/user/view_feedback', response.headers['Location'])  # Check redirection to feedback page

    # Test case for user viewing feedback
    @patch('base.com.dao.feedback_dao.FeedbackDAO.user_view_feedback')
    @patch('base.com.controller.login_controller.admin_login_session', return_value='user')
    @patch('base.com.dao.login_dao.LoginDAO.find_login_id', return_value=1)
    def test_user_view_feedback(self, mock_login_session, mock_find_login_id, mock_user_view_feedback):
        mock_user_view_feedback.return_value = []  # Mock an empty feedback list for user
        response = self.app.get('/user/view_feedback')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Feedback', response.data)  # Check if feedback page is rendered for user

    # Test case for invalid session (should log out)
    @patch('base.com.controller.login_controller.admin_login_session', return_value=None)
    def test_invalid_session(self, mock_login_session):
        response = self.app.get('/admin/view_feedback')
        self.assertEqual(response.status_code, 302)  # Redirect to login due to invalid session
        self.assertIn('/admin/logout_session', response.headers['Location'])  # Ensure redirection to logout session


if __name__ == '__main__':
    unittest.main()
