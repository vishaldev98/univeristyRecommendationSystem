import unittest
from unittest.mock import patch, MagicMock
from base import app

class TestComplainSystem(unittest.TestCase):
    def setUp(self):
        # Set up the test client to use with Flask
        self.app = app.test_client()
        self.app.testing = True

    # Test case for admin viewing complaints
    @patch('base.com.dao.complain_dao.ComplainDAO.admin_view_complain')
    @patch('base.com.controller.login_controller.admin_login_session', return_value='admin')
    def test_admin_view_complain(self, mock_login_session, mock_admin_view_complain):
        mock_admin_view_complain.return_value = []  # Mock empty complain list
        response = self.app.get('/admin/view_complain')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Complaints', response.data)  # Check if the complaints page is rendered

    # Test case for admin replying to a complaint
    @patch('base.com.dao.complain_dao.ComplainDAO.edit_complain')
    @patch('base.com.controller.login_controller.admin_login_session', return_value='admin')
    def test_admin_load_complain_reply(self, mock_login_session, mock_edit_complain):
        mock_edit_complain.return_value = [MagicMock()]  # Mock complain data
        response = self.app.get('/admin/load_complain_reply?complainId=1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reply', response.data)  # Check if the reply form is loaded

    # Test case for inserting a complaint reply
    @patch('base.com.dao.complain_dao.ComplainDAO.update_complain')
    @patch('base.com.dao.login_dao.LoginDAO.find_login_id', return_value=1)
    @patch('base.com.controller.login_controller.admin_login_session', return_value='admin')
    def test_admin_insert_complain_reply(self, mock_login_session, mock_find_login_id, mock_update_complain):
        response = self.app.post('/admin/insert_complain_reply', data={
            'complainId': '1',
            'complainReplyDescription': 'Your issue has been resolved.'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/view_complain', response.headers['Location'])  # Ensure redirect after reply

    # Test case for admin deleting a complaint
    @patch('base.com.dao.complain_dao.ComplainDAO.delete_complain')
    @patch('base.com.controller.login_controller.admin_login_session', return_value='admin')
    def test_admin_delete_complain(self, mock_login_session, mock_delete_complain):
        response = self.app.get('/admin/delete_complain?complainId=1')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/view_complain', response.headers['Location'])  # Ensure redirect after deletion

    # Test case for user viewing their complaints
    @patch('base.com.dao.complain_dao.ComplainDAO.user_view_complain')
    @patch('base.com.dao.login_dao.LoginDAO.find_login_id', return_value=1)
    @patch('base.com.controller.login_controller.admin_login_session', return_value='user')
    def test_user_view_complain(self, mock_login_session, mock_find_login_id, mock_user_view_complain):
        mock_user_view_complain.return_value = []  # Mock empty complain list
        response = self.app.get('/user/view_complain')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Complaints', response.data)  # Check if the complaints page for user is rendered

    # Test case for user inserting a complaint
    @patch('base.com.dao.complain_dao.ComplainDAO.insert_complain')
    @patch('base.com.dao.login_dao.LoginDAO.find_login_id', return_value=1)
    @patch('base.com.controller.login_controller.admin_login_session', return_value='user')
    def test_user_insert_complain(self, mock_login_session, mock_find_login_id, mock_insert_complain):
        response = self.app.post('/user/insert_complain', data={
            'complainSubject': 'Test Subject',
            'complainDescription': 'Test Description'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/user/view_complain', response.headers['Location'])  # Ensure redirect after insertion

    # Test case for invalid session when accessing admin routes
    @patch('base.com.controller.login_controller.admin_login_session', return_value=None)
    def test_invalid_session_admin(self, mock_login_session):
        response = self.app.get('/admin/view_complain')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/logout_session', response.headers['Location'])  # Redirect to logout if session invalid

    # Test case for invalid session when accessing user routes
    @patch('base.com.controller.login_controller.admin_login_session', return_value=None)
    def test_invalid_session_user(self, mock_login_session):
        response = self.app.get('/user/view_complain')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/logout_session', response.headers['Location'])  # Redirect to logout if session invalid

if __name__ == '__main__':
    unittest.main()
